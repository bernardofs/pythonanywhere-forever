# pythonanywhere-forever

Renews the 3 months free period of a pythonanywhere account automatically. It doesn't use any browser to do it, it uses only requests.

## Behavior

The app simulates the following user flow:

This bot was created to work on the AWS cloud periodically. It will be provided steps in the next section explaining how to do that. However, this can be adapted to work on other platforms.

Email integration (Optional): After the execution of the program, an email is sent using the [SendGrid API](https://docs.sendgrid.com/pt-br/for-developers/sending-email/api-getting-started). This email contains a success or error message, depending on the result returned by the program. The email integration can be disabled by commenting some lines in the `main.py` file.

## How to deploy on AWS

### Deploy a docker image on Amazon ECR

#### Option 1 (The easiest, it uses the public image generated via GitHub Actions)

- Create a **private** repository on Amazon ECR.

- Pull the public image

  `docker pull public.ecr.aws/p6v5m7k5/pythonanywhere-forever:latest`

- Go to `Amazon ECR > Repositories > MY_REPOSITORY_NAME`. After that, click on "View push commands". That will be useful for the next steps.

- Tag the version downloaded on the previous step, executing the following command:

  `docker tag IMAGE_ID AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/MY_REPOSITORY_NAME:TAG`

  The value `IMAGE_ID` can be found by executing: `docker images`, after pulling the data. The `REPOSITORY` value will be equal to `pythonanywhere-forever`. The URL from the repository can be found on the page opened in step 3 (in "View push commands").

- Authenticate the Docker client by executing the following command present in "View push commands":

  `aws ecr get-login-password --region AWS_REGION | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com`

- Push the AWS image downloaded in the beginning in your private repository.

  `docker push AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/MY_REPOSITORY_NAME:TAG`

#### Option 2 (generates a custom Docker image)

- The following content can also be seen in the following video: https://www.youtube.com/watch?v=yv8-Si5AB3U.

- Create a **private** repository on Amazon ECR.

- Clone this repository locally (with `git clone`)

- Create and set up a new user, using "IAM" on AWS.
  - Add "Access Key" as a type of AWS credential.
  - Click on "Attach existing policies directly" and the following policies:
    - AmazonEC2ContainerRegistryFullAccess
    - AdministratorAccess
    - AmazonEC2ContainerRegistryPowerUser
    - AmazonEC2ContainerRegistryReadOnly
  - Go next and create the user.
  - Store the "Access key ID" e the "Secret access key"
- In `Your repository on GitHub > Settings > Secrets > Actions > New repository secret`, add the following variables:

  - Name: `AWS_ACCESS_KEY_ID`, Secret: Value showed on the previous step on "Access key ID".
  - Name: `AWS_SECRET_ACCESS_KEY`, Secret: Value showed in the previous step on "Secret access key".
  - Name: `AWS_REGION`, Secret: Value present on the top right side of the AWS page. Ex: us-east-
  - Name: `FUNCTION_ARN_NAME`, Secret: Value chosen on the next step, after creating the lambda function.
  - Name: `REPOSITORY`, Secret: Name of the lambda repository chosen on the next step, after creating the lambda function.

- In `.github/workflows/aws.yml`, remove the following "steps":

  - Login to Amazon ECR Public
  - Build, tag, and push docker image to Amazon ECR Public
  - Delete untagged images

- After doing all the previous steps, if anything is pushed to the repository, the GitHub Actions will execute the following steps:
  - Build and push the Docker Image in the ECR repository.
  - Update the Docker Image URL to the one generated in the previous step.
  - Erase all old Docker images (without any tags) from the ECR repository to keep only one there.

### Setup an AWS Lambda function

- Create an AWS Lambda function.

  - Select: "Container Image".
  - Name the function.
  - Select the image created in the previous step.
  - Architecture: x86_64.

- Select the tab Settings.

  - Select the tab General Settings.
    - Increase the limits of memory, storage and timeout up to the limit.
  - Select the tab Environment Variables
    - See the file `.secret_example.env` e and add all Environment Variables and their values. If you chose option 1 in the last section, you will not need to work on this file. This file is only for local testing purposes.

- To test the function, you can click on the Test tab and create a test event to execute the function.

### Create periodic events to run the function on specific periods.

- On AWS, go to: "EventBridge".

- Click on: "Create rule".

- Create a rule of type "Schedule".

- Define a [cron](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html) expression.

- Select "Lambda Function" and choose the function created in the last step.

- Confirm the event.

- After doing the steps above, the function will be executed regularly according to the cron expression.

### Extra

#### How to test the Docker image locally? (If you chose option 2 to deploy the image)

- Rename the file `.secret_example.env` to `.secret.env` and fill in the empty values.
- Build the image: `docker compose build`
- Run the image: `docker run -p 9000:8080 --env-file .secret.env MY_REPOSITORY_NAME:latest`
- Run the function by executing the following command on another terminal:

  `curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`

  See [this tutorial](https://docs.aws.amazon.com/lambda/latest/dg/images-test.html) for more details.
