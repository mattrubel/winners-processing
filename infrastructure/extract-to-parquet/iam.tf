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
  name = "extract-to-parquet-policy"
  description = "Extract to parquet policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # read json bucket
      {
        Effect = "Allow"
        Action = [
          "s3:*",
          # "s3:GetObject",
        ]
        Resource = [
          "arn:aws:s3:::winners-v2-data",
          "arn:aws:s3:::winners-v2-data/*",
        ]
      },
      # write to destination bucket
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
        ]
        Resource = [
          "arn:aws:s3:::junk-597426459950",
          "arn:aws:s3:::junk-597426459950/*",
        ]
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "extract_to_parquet_attachment" {
  name = "extract-to-parquet-attachment"
  roles = [aws_iam_role.extract_to_parquet_role.name, ]
  policy_arn = aws_iam_policy.extract_to_parquet_policy.arn
}
