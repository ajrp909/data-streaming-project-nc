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

    API_KEY = The api key for your account when signing up on the guardian website.
    FUNC_NAME = This is the name we are using on aws when creating our lambda.
    REGION =  This is the AWS region where the Lambda function is deployed.
    ACCOUNT_ID = This is the AWS account ID that owns the Lambda function.
    AWS_PROFILE = This is the AWS profile name to use for authentication that was set in the configuration phase (step 1).

**Step 3**:
    - Create and launch a Python virtual environment and install the required dependencies from the projects root:

        python -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt

Now the infrastructure needs to be created on aws.

If using Terraform:

**Step 4**:
    Install Terraform

**Step 5**:
    Add a terraform.tfvars file in the projects root directory:

        touch terraform.tfvars

Include the following variables within the newly created terraform.tfvars file:

        aws_profile = same value as AWS_PROFILE
        aws_region  = same value as REGION

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