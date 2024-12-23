terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
    profile = var.aws_profile
  region = var.aws_region
}

resource "aws_sqs_queue" "terraform_queue" {
  name                      = "Nc-Sqs-Queue-2"
  message_retention_seconds = 259200
}

resource "aws_iam_role" "lambda_role" {
    name = "Nc-Sqs-Role-2"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect    = "Allow"
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
                Action    = "sts:AssumeRole"
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "lambda_sqs_policy" {
    role = aws_iam_role.lambda_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}