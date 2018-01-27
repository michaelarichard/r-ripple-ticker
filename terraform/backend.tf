terraform {
  backend "s3" {
    bucket = "stormpath-terraform-state"
    region = "us-west-2"
    key = "rripple/ticker/us-west-2/prod/terraform.tfstate"
#    profile = "personal_aws"
#    role_arn = "arn:aws:iam::00000000000:role/path/blah/blah/blah""
  }
}

provider "aws" {
  region = "${ var.region }"
#  assume_role {
#    role_arn = "arn:aws:iam::00000000000:role/path/blah/blah/blah"
#  }
}

