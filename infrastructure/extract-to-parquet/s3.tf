data "aws_s3_bucket" "winners_v2_data_bucket" {
  bucket = "winners-v2-data" # in future move data to bucket stamped with acct id
}
