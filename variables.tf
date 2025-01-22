variable "aws_profile" {
  description = "The AWS profile to use"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "func_name" {
  description = "name given to Lambda function that will appear in aws console"
  type        = string
}

variable "iam_role_name" {
  description = "Name given to iam policy that will appear in aws console"
  type = string
}

variable "sqs_queue_name" {
  description = "Name given to sqs queue that will appear in aws console"
  type = string
}