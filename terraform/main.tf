#resource "aws_iam_role" "iam_for_lambda" {
#  name = "iam_for_lambda"
#
#  assume_role_policy = <<EOF
#{
#  "Version": "2012-10-17",
#  "Statement": [
#    {
#      "Action": "sts:AssumeRole",
#      "Principal": {
#        "Service": "lambda.amazonaws.com"
#      },
#      "Effect": "Allow",
#      "Sid": ""
#    }
#  ]
#}
#EOF
#}

resource "aws_lambda_function" "ticker_lambda" {
  filename         = "lambda.py.zip"
  function_name    = "${var.function_name}"
  role             = "${data.aws_iam_role.reddit_lambda.arn}"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = "${base64sha256(file("lambda.py.zip"))}"
  runtime          = "python3.6"
  timeout          = "30"
  environment {
    variables = {
      REDDIT_CLIENT_ID       = "${var.REDDIT_CLIENT_ID}"
      REDDIT_CLIENT_SECRET   = "${var.REDDIT_CLIENT_SECRET}"
      REDDIT_CLIENT_USERNAME = "${var.REDDIT_CLIENT_USERNAME}"
      REDDIT_CLIENT_PASSWORD = "${var.REDDIT_CLIENT_PASSWORD}"
      REDDIT_SUBREDDIT       = "${var.REDDIT_SUBREDDIT}"
    }
  }
}

resource "aws_cloudwatch_event_rule" "ticker1min" {
   name = "ticker1min"
   depends_on = ["aws_lambda_function.ticker_lambda"]
   schedule_expression = "rate(1 minute)"
}

resource "aws_cloudwatch_event_target" "ticker1min" {
    target_id = "ticker1min"
    rule = "${aws_cloudwatch_event_rule.ticker1min.name}"
    arn = "${aws_lambda_function.ticker_lambda.arn}"
}

resource "aws_lambda_permission" "ticker1min" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.ticker_lambda.function_name}"
  principal = "events.amazonaws.com"
  source_arn = "${aws_cloudwatch_event_rule.ticker1min.arn}"
}
