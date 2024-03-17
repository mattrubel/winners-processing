variable "AWS_REGION" {
  default = "us-east-1"
}

variable "VPC_CIDR" {
  default = "10.0.0.0/16"
}

variable "CLUSTER_NAME" {
  default = "winners"
  # can't be winners-processing because
  # the module will create names that are too long
}
