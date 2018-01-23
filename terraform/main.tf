resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "test_lambda" {
  filename         = "lambda_function.zip"
  function_name    = "${var.function_name}"
  role             = "${aws_iam_role.iam_for_lambda.arn}"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = "${base64sha256(file("lambda_function.zip"))}"
#  runtime          = "nodejs4.3"
  runtime          = "python3.6"
  environment {
    variables = {
      REDDIT_CLIENT_ID = "${var.REDDIT_CLIENT_ID}"
      REDDIT_CLIENT_SECRET = "${var.REDDIT_CLIENT_SECRET}"
      REDDIT_CLIENT_USERNAME = "${var.REDDIT_CLIENT_USERNAME}"
      REDDIT_CLIENT_PASSWORD = "${var.REDDIT_CLIENT_PASSWORD}"
    }
  }
}
