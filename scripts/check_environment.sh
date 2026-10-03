#!/bin/bash

echo "=== AWS Incident Management Platform ==="
echo "Checking Linux environment..."
echo

echo "User: $(whoami)"
echo "Current directory: $(pwd)"
echo "Linux version:"
uname -a

echo
echo "Git version:"
git --version

echo
echo "AWS CLI version:"
if command -v aws >/dev/null 2>&1; then
    aws --version
else
    echo "AWS CLI is not installed."
fi

echo
echo "Environment check complete."
