import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Read JSON from S3") \
    .getOrCreate()

# Define S3 credentials and JSON file path
access_key = os.environ["ACCESS_KEY"]
secret_key = os.environ["SECRET_ACCESS_KEY"]
json_file_path = os.environ["JSON_PATH"]

# Configure AWS credentials
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)

# Read JSON file into DataFrame
df = spark.read.json(json_file_path)

# explode books
df_by_book = df.select(
    df.away_team,
    df.home_team,
    df.commence_time,
    df.sport_key,
    df.id,
    explode(df.bookmakers).alias("book")
)

# explode markets
df_by_market = df_by_book.select(
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

df_by_outcome = df_by_outcome.select(
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

print(df_by_outcome)
df_by_outcome.show()
print(df_by_outcome.schema)
print(df_by_outcome.count())
