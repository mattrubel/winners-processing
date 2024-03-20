provider "aws" {
  region = var.AWS_REGION
}

module "common-resources" {
  source         = "../../../common-resources"
  AWS_ACCOUNT_ID = var.AWS_ACCOUNT_ID
}
