provider "aws" {
  region = var.AWS_REGION
}

module "winners-processing" {
  source = "../../../winners-processing-cluster"
}
