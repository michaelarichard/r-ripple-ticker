terraform {
  backend "s3" {
    bucket = "stormpath-terraform-state"
    region = "us-west-2"
    key = "rripple/ticker/us-west-2/prod/terraform.tfstate"
  }
}
