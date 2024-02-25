import argparse
from datetime import date

from pyspark.sql import DataFrame, Row, SparkSession
from pyspark.sql import functions as F


class EtlToParquet:
    def __init__(self, file_s3_uri: str, file_type: str) -> None:
        self.file_s3_uri = file_s3_uri
        self.file_type = file_type
        self.spark = SparkSession.builder.appName("EtlToParquet").getOrCreate()

    def run(self) -> None:
        if self.file_type == "":
            pass
        df = self._fetch_data()

    def _fetch_data(self) -> DataFrame:
        # TODO
        return None
        # df = self.spark.read.json()
        # return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-s3-uri", type=str, required=True)
    parser.add_argument("--file-type", type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    etl_to_parquet = EtlToParquet(args.file_s3_uri, args.file_type)
    etl_to_parquet.run()
