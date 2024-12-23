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
  name                      = "terraform-example-queue"
  message_retention_seconds = 259200
}