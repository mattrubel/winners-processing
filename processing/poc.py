import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, input_file_name


def extract_files(spark: SparkSession, json_dir: str, output_dir: str):
    # Read JSON directory into DataFrame
    df = spark.read.json(json_dir)
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
        df_by_market.market.key.alias("outcome_key"),
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
        df_by_outcome.outcome_key,
        df_by_outcome.outcome['name'].alias("name"),
        df_by_outcome.outcome.point.alias("point"),
        df_by_outcome.outcome.price.alias("price")
    )

    return df_by_outcome


if __name__ == "__main__":
    # Create a SparkSession
    spark_session = SparkSession.builder \
        .appName("Read JSON from S3") \
        .getOrCreate()

    # QUESTION: can I omit access keys when running on EMR? if so, then use environment logic to bypass in emr
    # Define S3 credentials and JSON file path
    access_key = os.environ["ACCESS_KEY"]
    secret_key = os.environ["SECRET_ACCESS_KEY"]
    json_uri = os.environ["JSON_DIRECTORY"]

    output_uri = os.environ["OUTPUT_DIRECTORY"]

    # Configure AWS credentials
    spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
    spark_session.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)

    extract_files(spark_session, json_uri, output_uri)

    spark_session.stop()
