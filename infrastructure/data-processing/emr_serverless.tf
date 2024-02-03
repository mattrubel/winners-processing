resource "aws_emrserverless_application" "warehouse_cluster" {
  name          = "warehouse-cluster"
  release_label = "emr-6.13.0"
  type          = "spark"
}
