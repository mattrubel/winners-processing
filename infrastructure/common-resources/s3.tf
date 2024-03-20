# Bucket for PySpark Code
resource "aws_s3_bucket" "winners_processing_pyspark_code_bucket" {
  bucket = "winners-processing-code-${var.AWS_ACCOUNT_ID}"
}
