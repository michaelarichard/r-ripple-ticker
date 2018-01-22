#!/bin/bash
rm lambda.py.zip
mkdir libs
cp lambda_function.py libs/.
pip3 install praw requests -t libs/.
cd libs; zip -r ../lambda.py.zip .
cd ..
rm -rf libs
