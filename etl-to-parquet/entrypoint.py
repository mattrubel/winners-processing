import sys
from datetime import date

from jobs.etl_to_parquet import EtlToParquet

if __name__ == "__main__":
    # """
    # Usage: extreme-weather s3 file pat
    # Displays extreme weather stats (highest temperature, wind, precipitation) for the given, or latest, year.
    # """

    file_s3_uri = sys.argv[1]
    file_type = sys.argv[2]

    etl_to_parquet = EtlToParquet(file_s3_uri, file_type)
    etl_to_parquet.run()
