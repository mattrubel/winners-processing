resource "aws_emrserverless_application" "warehouse_cluster" {
  name          = "warehouse-processing-cluster"
  release_label = "emr-6.14.0"
  type          = "spark"
}
