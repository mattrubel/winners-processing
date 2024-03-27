import argparse
import datetime
from datetime import timedelta

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, input_file_name


def format_s3_uri(uri: str) -> str:
    # change s3 to s3a
    if 's3a' not in uri:
        uri = uri.replace("s3", "s3a")

    # ensure trailing slash
    if uri[-1] != "/":
        uri = uri + "/"

    return uri


def build_s3_uri_list(
        start_date_: str,
        end_date_: str,
        s3_prefix: str
) -> list:

    # expect dates to be in yyyymmdd
    start_dt = datetime.date(
        int(start_date_[0:4]),
        int(start_date_[4:6]),
        int(start_date_[6:8]),
    )
    end_dt = datetime.date(
        int(end_date_[0:4]),
        int(end_date_[4:6]),
        int(end_date_[6:8]),
    )

    date_list = [start_dt + timedelta(days=x) for x in range((end_dt - start_dt).days)]

    return [f"{s3_prefix}{str(x.year)}/{str(x.month).zfill(2)}/{str(x.day).zfill(2)}/" for x in date_list]


def extract_files(spark: SparkSession, json_dirs: list, output_dir: str):
    # Read JSON directory into DataFrame
    df = spark.read.json(json_dirs)
    df = df.withColumn('file_name', input_file_name())

    df_by_outcome = explode_df(df)

    df_by_outcome.write.parquet(output_dir, mode="overwrite")


def explode_df(df):
    # explode books
    df_by_book = df.select(
        df.away_team,
        df.home_team,
        df.commence_time,
        df.sport_key,
        df.id,
        df.file_name,
        explode(df.bookmakers).alias("book")
    )

    # unpack books, explode markets
    df_by_market = df_by_book.select(
        df_by_book.file_name,
        df_by_book.away_team,
        df_by_book.home_team,
        df_by_book.commence_time,
        df_by_book.id.alias("game_id"),
        df_by_book.sport_key,
        df_by_book.book.key.alias("book_key"),
        df_by_book.book.last_update.alias("last_updated"),
        explode(df_by_book.book.markets).alias("market"),
    )

    # explode outcomes
    df_by_outcome = df_by_market.select(
        df_by_market.file_name,
        df_by_market.away_team,
        df_by_market.home_team,
        df_by_market.commence_time,
        df_by_market.game_id,
        df_by_market.sport_key,
        df_by_market.book_key,
        df_by_market.last_updated,
        df_by_market.market.key.alias("market_key"),
        explode(df_by_market.market.outcomes).alias("outcome"),
    )

    # unpack outcomes
    df_by_outcome = df_by_outcome.select(
        df_by_outcome.file_name,
        df_by_outcome.away_team,
        df_by_outcome.home_team,
        df_by_outcome.commence_time,
        df_by_outcome.game_id,
        df_by_outcome.sport_key,
        df_by_outcome.book_key,
        df_by_outcome.last_updated,
        df_by_outcome.market_key,
        df_by_outcome.outcome['name'].alias("name"),
        df_by_outcome.outcome.point.alias("point"),
        df_by_outcome.outcome.price.alias("price")
    )

    return df_by_outcome


if __name__ == "__main__":
    # Create a SparkSession
    spark_session = SparkSession.builder \
        .appName("ExtractToParquet") \
        .getOrCreate()

    parser = argparse.ArgumentParser()

    parser.add_argument("--input-prefix", help="S3 URI prefix for input files - excluding date.")
    parser.add_argument("--output-prefix", help="Output S3 URI prefix for process to write to")
    parser.add_argument("--environment", help="p for prod, d for dev, l for local")
    parser.add_argument("--start-date", help="Analysis start date yyyymmdd")
    parser.add_argument("--end-date", help="Analysis end date yyyymmdd")
    parser.add_argument("--aws-access-key", required=False)
    parser.add_argument("--aws-secret-access-key", required=False)

    args = parser.parse_args()
    env = args.environment
    output_prefix = args.output_prefix
    start_date = args.start_date
    end_date = args.end_date
    input_prefix = args.input_prefix

    if env == "l":
        access_key = args.aws_access_key
        secret_key = args.aws_secret_access_key
        spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
        spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)

    input_prefix = format_s3_uri(input_prefix)
    output_prefix = format_s3_uri(output_prefix)

    json_uris = build_s3_uri_list(start_date, end_date, input_prefix)

    extract_files(spark_session, json_uris, output_prefix)

    spark_session.stop()
