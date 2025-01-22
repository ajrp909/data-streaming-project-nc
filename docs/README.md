# data-streaming-project-nc

The IaC element in this application is independant from any of the python code. This means that there are two approaches that can be taken in order for a successful request being pushed into aws.

The following outlines the intended and recommended approach, using IaC:

**Step 1**:
    - Install the aws cli and run the following command:

        aws configure

**Step 2**:
    - All environment variables need to be added into a .env file at the root of the project, while in the projects root in the terminal:

        touch .env

Navigate to this .env file and add the following as constants:

    API_KEY = The api key for your account when signing up on the guardian open platform website found at this URL - https://open-platform.theguardian.com

    FUNC_NAME = This is the name we are using on aws when creating our lambda.

    REGION =  This is the AWS region where the Lambda function is deployed.

    ACCOUNT_ID = This is the AWS account ID that owns the Lambda function.

    AWS_PROFILE = This is the AWS profile name to use for authentication that was set in the configuration phase (step 1).

For example:

        API_KEY = "0123456789-abcdefgh-fakeapikey"
        REGION = "us-east-1"
        ACCOUNT_ID = "0123456789"
        FUNC_NAME = "Nc-Lambda"
        AWS_PROFILE = "iamadmin"

**Step 3**:
    - Create and launch a Python virtual environment and install the required dependencies from the projects root:

        python -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        export PYTHONPATH=$(pwd)

Now the infrastructure needs to be created on aws.

If using Terraform:

**Step 4**:
    Install Terraform

**Step 5**:
    Add a terraform.tfvars file in the projects root directory:

        touch terraform.tfvars

Include the following variables within the newly created terraform.tfvars file:

        aws_profile = same as AWS_PROFILE variable in .env file.

        aws_region  = same as REGION variable in .env file.

        func_name = same as FUNC_NAME in .env file.

        iam_role_name = The name of the iam policy that is wanted to be set in the aws console.

        sqs_queue_name = The name of the sqs queue that will be used to recieve the messages in the AWS console.

For example:

        aws_profile = "iamadmin"
        aws_region  = "us-east-1"
        func_name = "Nc-Lambda"
        iam_role_name = "Nc-Sqs-Role"
        sqs_queue_name = "Nc-Sqs-Queue"
        

**Step 6**:
    Build the infrastructure - when in the projects root, run the following commands:

        make init

        make plan

        make apply

**Step 7**:
    Now the program is ready:
    
        make main

**Step 8**:
    Follow instructions in the terminal, you should see messages from your search terms populating in the aws console.

**Step 9**:
    When you want to destroy all the infrastructure (which will also destroy the sqs queue and all the messages populated):

        make destroy