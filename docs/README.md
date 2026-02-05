# data-streaming-project-nc

The IaC element in this application is independant from any of the python code. This means that there are two approaches that can be taken in order for a successful request being pushed into aws.

This guide assumes the user is using a UNIX based system, and has aws cli and Terraform installed.

In this example setup, consider an IAM user being setup with the name *"NC-1234"* that only requieres programmatic access and does not require access to the AWS console:

## Step 1 - Creating the IAM user in the console ##

Log in to the the AWS console with an IAM user that has full admin access or one that can setup and configure a new IAM user.

Navigate to **IAM > Users > Create User**.

Enter username of *"NC-1234"* and click next.

On the set permissions screen, leave everything as is and click next again.

On Review and create, check the username is correct and click create user.

## Step 2 - Add Permissions to the IAM user ##

You should be back at the **IAM > Users** screen, click on the newly created *"NC-1234"* IAM user.

This brings you to the permissions screen. Click on add permissions and in the dropdown select create inline policy.

Click on JSON on the policy editor toggle.

The JSON permissions required for an IAM user to run the program successfully are as follows, copy and paste this into the policy editor:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "NCPermissions",
                "Effect": "Allow",
                "Action": [
                    "sqs:CreateQueue",
                    "sqs:getqueueattributes",
                    "sqs:listqueuetags",
                    "sqs:deletequeue",
                    "iam:CreateRole",
                    "iam:GetRole",
                    "iam:ListRolePolicies",
                    "iam:ListAttachedRolePolicies",
                    "iam:ListInstanceProfilesForRole",
                    "iam:DeleteRole",
                    "iam:AttachRolePolicy",
                    "iam:DetachRolePolicy",
                    "iam:PassRole",
                    "lambda:CreateFunction",
                    "lambda:GetFunction",
                    "lambda:ListVersionsByFunction",
                    "lambda:GetFunctionCodeSigningConfig",
                    "lambda:DeleteFunction",
                    "lambda:InvokeFunction"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }

Click next.

In the policy name field, enter *"NCPermissions"* and click create policy.

## Step 3 - Set up AWS CLI ##

You should now be in **IAM > USERS > *"NC-1234"***

Click on **Security Credentials**, scroll down to access keys, click on create access key, then select command line interface (CLI), click the checkbox for confirmation then click next.

Click create access key.

This creates an access key and a secret access key, which are both needed for the CLI setup. Either download as a CSV or note them down.

Click done.

Navigate to a terminal window and Install the AWS CLI.

Then run the following command to set the profile name in the CLI as NC-1234:

        aws configure --profile NC-1234

Follow the instructions in the terminal:

        enter access key just obtained
        enter secret access key just obtained
        enter your default region exactly how it appears in the aws console, for example - us-east-1
        ignore default output format - Just press enter to ignore this step

The CLI is now configured.

## Step 4 - Add Enviroment Variables ##

All environment variables need to be added into a .env file at the root of the project. While in the projects root in the terminal, run the command:

        touch .env

Navigate to this .env file and add the following as constants:

    API_KEY = Obtain an api key for your account when signing up on the guardian open platform website found at this URL - https://open-platform.theguardian.com

    REGION =  This is the AWS region where the Lambda function is deployed.

    ACCOUNT_ID = This is the AWS account ID that owns the Lambda function.

    FUNC_NAME = This is the name we are using on aws when creating our lambda.

    AWS_PROFILE = This is the AWS profile name we just set up in the CLI - "NC-1234"

Current example:

        API_KEY = "0123456789-abcdefgh-fakeapikey"
        REGION = "us-east-1"
        ACCOUNT_ID = "0123456789"
        FUNC_NAME = "Nc-Lambda-1"
        AWS_PROFILE = "NC-1234"

## Step 5 - Install Terraform and add tfvars file ##

Add a terraform.tfvars file in the projects root directory with the following command:

        touch terraform.tfvars

Include the following variables within the newly created terraform.tfvars file:

    aws_profile = same as AWS_PROFILE variable in .env file.

    aws_region  = same as REGION variable in .env file.

    func_name = same as FUNC_NAME in .env file.

    iam_role_name = The name of the iam policy that is wanted to be set in the aws console.

    sqs_queue_name = The name of the sqs queue that will be used to recieve the messages in the AWS console.

Current example:

        aws_profile = "NC-1234"
        aws_region  = "us-east-1"
        func_name = "Nc-Lambda-1"
        iam_role_name = "Nc-Sqs-Role-1"
        sqs_queue_name = "Nc-Sqs-Queue-1"

## Step 6 - Launch Python Virtual environment and Install dependencies

Create and launch a Python virtual environment and install the required dependencies from the projects root:

        python -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        export PYTHONPATH=$(pwd)

Now the infrastructure needs to be created on aws.       

## Step 7 - Build the infrastructure ##

when in the projects root, run the following commands one after another:

        make init

        make plan

        make apply

## Step 8 - Load messages into the queue ##

Now the program is ready - run the penultimate command:
    
        make main

Follow instructions in the terminal, you should see messages from your search terms populating in the aws console.

## Step 9 - Clean up infrastructure ##
When you want to destroy all the infrastructure (which will also destroy the sqs queue and all the messages populated):

        make destroy

## Troubleshooting suggestions ##

If there are issues with the deployment or push into SQS, try to deploy everything manually first to see if it is perhaps a permissions problem.

Ensure the venv is setup correctly, and that the PYTHONPATH is correct.

Check the region is consistent for your instance.

Ensure the lambda function name is consistent.