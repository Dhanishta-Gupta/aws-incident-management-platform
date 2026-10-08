# AWS Incident Management Platform

An AWS-based CloudOps project that detects cloud incidents, sends alerts, and automatically creates incident records for investigation and response.

## Project Objective

The goal of this project is to build a practical incident-management workflow using AWS services commonly used in cloud operations.

The platform can:

- Monitor an EC2 instance.
- Detect high CPU utilization.
- Trigger a CloudWatch alarm when a defined threshold is exceeded.
- Send incident notifications through Amazon SNS.
- Automatically process the incident using AWS Lambda.
- Store structured incident records in Amazon S3.
- Support incident investigation and recovery verification.

## Architecture

```text
EC2 Instance
     |
     | CPUUtilization
     v
Amazon CloudWatch
     |
     | Alarm: CPU > 70%
     v
CloudWatch Alarm
     |
     v
Amazon SNS
   /     \
  /       \
Email    AWS Lambda
             |
             v
          Amazon S3
             |
             v
      Incident JSON Record
