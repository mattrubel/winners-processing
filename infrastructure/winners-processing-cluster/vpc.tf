data "aws_availability_zones" "available" {}

locals {
  azs = slice(data.aws_availability_zones.available.names, 0, 3)

}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = var.CLUSTER_NAME
  cidr = var.VPC_CIDR


  azs             = local.azs
  public_subnets  = [for k, v in local.azs : cidrsubnet(var.VPC_CIDR, 8, k)]
  private_subnets = [for k, v in local.azs : cidrsubnet(var.VPC_CIDR, 8, k + 10)]

  enable_nat_gateway = true
  single_nat_gateway = true

  # https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-iam-policies.html#manually-tagged-resources
  # Tag if you want EMR to create the security groups for you
  # vpc_tags            = { "for-use-with-amazon-emr-managed-policies" = true }
  # Tag if you are using public subnets
  # public_subnet_tags  = { "for-use-with-amazon-emr-managed-policies" = true }
  private_subnet_tags = { "for-use-with-amazon-emr-managed-policies" = true }

}

module "vpc_endpoints" {
  source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
  version = "~> 5.0"

  vpc_id             = module.vpc.vpc_id
  security_group_ids = [module.vpc_endpoints_sg.security_group_id]

  endpoints = merge({
    s3 = {
      service         = "s3"
      service_type    = "Gateway"
      route_table_ids = module.vpc.private_route_table_ids
      tags = {
        Name = "${var.CLUSTER_NAME}-s3"
      }
    }
    },
    { for service in toset(["elasticmapreduce", "sts"]) :
      replace(service, ".", "_") =>
      {
        service             = service
        subnet_ids          = module.vpc.private_subnets
        private_dns_enabled = true
        tags                = { Name = "${var.CLUSTER_NAME}-${service}" }
      }
  })

}

module "vpc_endpoints_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.0"

  name        = "${var.CLUSTER_NAME}-vpc-endpoints"
  description = "Security group for VPC endpoint access"
  vpc_id      = module.vpc.vpc_id

  ingress_with_cidr_blocks = [
    {
      rule        = "https-443-tcp"
      description = "VPC CIDR HTTPS"
      cidr_blocks = join(",", module.vpc.private_subnets_cidr_blocks)
    },
  ]
}
