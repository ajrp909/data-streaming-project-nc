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
  name                      = var.sqs_queue_name
  message_retention_seconds = 259200
}

output "queue_url" {
    value = aws_sqs_queue.terraform_queue.id
}

resource "aws_iam_role" "lambda_role" {
    name = var.iam_role_name
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

data "archive_file" "zip_python_code" {
    type = "zip"
    source_file = "${path.module}/aws/lambda_function.py"
    output_path = "${path.module}/aws/lambda_function.zip"
}

resource "aws_lambda_function" "terraform_lambda_func" {
    filename = "${path.module}/aws/lambda_function.zip"
    function_name = var.func_name
    role = aws_iam_role.lambda_role.arn
    handler = "lambda_function.lambda_handler"
    runtime = "python3.9"
    depends_on = [ aws_iam_role_policy_attachment.lambda_sqs_policy ]
    environment {
        variables = {
            SQS_URL = "${aws_sqs_queue.terraform_queue.id}"
        }
    }
}