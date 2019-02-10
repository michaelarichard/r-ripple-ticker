terraform {
  backend "s3" {
    bucket = "stormpath-terraform-state"
    region = "us-west-2"
    key = "rripple/ticker/us-west-2/${var.REDDIT_SUBREDDIT}/terraform.tfstate"
  }
}
