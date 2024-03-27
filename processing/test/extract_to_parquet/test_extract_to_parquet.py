from pyspark.sql.types import StructType, StructField, StringType

from processing.extract_to_parquet.extract_to_parquet import build_s3_uri_list, explode_df, format_s3_uri

from pyspark.sql import SparkSession


def test_format_s3_uri():
    function_value = format_s3_uri("s3://test-bucket/test_dir")
    expected_value = "s3a://test-bucket/test_dir/"

    assert function_value == expected_value


def test_build_s3_uri_list():
    function_value = build_s3_uri_list("20230930", "20231002", "s3://test-bucket/test_dir/")
    expected_value = ["s3://test-bucket/test_dir/2023/09/30/", "s3://test-bucket/test_dir/2023/10/01/"]
    assert len(function_value) == len(expected_value)

    for idx in range(len(function_value)):
        print(idx)
        assert function_value[idx] == expected_value[idx]


# def test_explode_df():
#     # StructType(List(StructField(age,IntegerType,true),StructField(name,StringType,true)))
#     test_dict = get_test_dict()
#     spark = SparkSession.builder \
#         .appName("TestExtractToParquet") \
#         .getOrCreate()
#
#     df = spark.createDataFrame(test_dict)
#
#     df = explode_df(df)
#
#     assert df.count() == 6
#
#
# def get_test_dict():
#     return [
#         {
#             'file_name': 'file_name',
#             'away_team': 'away_team',
#             'home_team': 'home_team',
#             'commence_time': '2024-03-25T17:00:00',
#             'sport_key': 'sport_key',
#             'id': 'id',
#             'bookmakers': [
#                 {
#                     'key': 'book_key',
#                     'last_update': '2024-03-25T19:00:00',
#                     'markets': [
#                         {
#                             'key': 'total',
#                             'last_update': 'last',
#                             'outcomes': [
#                                 {
#                                     'name': 'over',
#                                     'point': 3.5,
#                                     'price': 2.01
#                                 },
#                                 {
#                                     'name': 'under',
#                                     'point': 3.5,
#                                     'price': 1.8
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 {
#                     'key': 'book_key_2',
#                     'last_update': '2024-03-25T19:00:00',
#                     'markets': [
#                         {
#                             'last_update': 'last_update',
#                             'key': 'h2h',
#                             'outcomes': [
#                                 {
#                                     'name': 'away_team',
#                                     'price': 1.91
#                                 },
#                                 {
#                                     'name': 'home_team',
#                                     'price': 1.91
#                                 }
#                             ]
#                         },
#                         {
#                             'key': 'total',
#                             'outcomes': [
#                                 {
#                                     'name': 'over',
#                                     'point': 3.5,
#                                     'price': 2.01
#                                 },
#                                 {
#                                     'name': 'under',
#                                     'point': 3.5,
#                                     'price': 1.8
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
#
#
# def get_test_schema():
#     outcome_schema = StructType([
#         StructField("", StringType())
#     ])
