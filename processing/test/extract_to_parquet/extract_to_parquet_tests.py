from processing.extract_to_parquet.extract_to_parquet import format_s3_uri


def test_format_s3_uri():
    function_value = format_s3_uri("s3://test-bucket/test_dir")
    expected_value = "s3a://test-bucket/test_dir/"

    assert function_value == expected_value
