terraform {
  backend "s3" {
    bucket         = "terraform-597426459950"
    key            = "winners-processing/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-state-lock"
  }
}
