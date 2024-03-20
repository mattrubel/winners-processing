resource "aws_iam_role" "extract_to_parquet_role" {
  name = "extract-to-parquet-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "emr-serverless.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "extract_to_parquet_policy" {
  name        = "extract-to-parquet-policy"
  description = "Extract to parquet policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # read and write data bucket
      {
        Effect = "Allow"
        Action = [
          "s3:DeleteObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject",
        ]
        Resource = [
          data.aws_s3_bucket.winners_v2_data_bucket.arn,
          "${data.aws_s3_bucket.winners_v2_data_bucket.arn}/*",
        ]
      },
      # read code
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
        ]
        Resource = [
          "arn:aws:s3:::winners-processing-code-${var.AWS_ACCOUNT_ID}",
          "arn:aws:s3:::winners-processing-code-${var.AWS_ACCOUNT_ID}/${var.NAME}/*",
        ]
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "extract_to_parquet_attachment" {
  name       = "extract-to-parquet-attachment"
  roles      = [aws_iam_role.extract_to_parquet_role.name, ]
  policy_arn = aws_iam_policy.extract_to_parquet_policy.arn
}
