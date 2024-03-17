module "emr_instance_group" {
  source = "terraform-aws-modules/emr/aws"

  name = "${var.CLUSTER_NAME}-instance-group"

#  release_label_filters = {
#    emr6 = {
#      prefix = "emr-6"
#    }
#  }

  release_label = "emr-6.14.0"
  applications = ["spark", "trino"]
  auto_termination_policy = {
    idle_timeout = 3600
  }

#  bootstrap_action = {
#    example = {
#      name = "Just an example",
#      path = "file:/bin/echo",
#      args = ["Hello World!"]
#    }
#  }

  configurations_json = jsonencode([
    {
      "Classification" : "spark-env",
      "Configurations" : [
        {
          "Classification" : "export",
          "Properties" : {
            "JAVA_HOME" : "/usr/lib/jvm/java-1.8.0"
          }
        }
      ],
      "Properties" : {}
    }
  ])

  master_instance_group = {
    name           = "master-group"
    instance_count = 1
    instance_type  = "m5.xlarge"
  }

  core_instance_group = {
    name           = "core-group"
    instance_count = 2
    instance_type  = "c4.large"
  }

  task_instance_group = {
    name           = "task-group"
    instance_count = 2
    instance_type  = "c5.xlarge"
    bid_price      = "0.1"

    ebs_config = {
      size                 = 64
      type                 = "gp3"
      volumes_per_instance = 1
    }
    ebs_optimized = true
  }

  ebs_root_volume_size = 64
  ec2_attributes = {
    # Instance groups only support one Subnet/AZ
    subnet_id = element(module.vpc.private_subnets, 0)
  }
  vpc_id = module.vpc.vpc_id

  keep_job_flow_alive_when_no_steps = true
  list_steps_states                 = ["PENDING", "RUNNING", "CANCEL_PENDING", "CANCELLED", "FAILED", "INTERRUPTED", "COMPLETED"]
  log_uri                           = "s3://${module.s3_bucket.s3_bucket_id}/"

  scale_down_behavior    = "TERMINATE_AT_TASK_COMPLETION"
  step_concurrency_level = 3
  termination_protection = false
  visible_to_all_users   = true

}
