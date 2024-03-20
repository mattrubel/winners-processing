module "winners-processing" {
  source = "../../../extract-to-parquet"

  AWS_ACCOUNT_ID = var.AWS_ACCOUNT_ID
}
