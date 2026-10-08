# AWS Incident Management Platform — Architecture

## Overview

The AWS Incident Management Platform is designed to detect cloud incidents, notify operators, automatically record incident information, and support incident investigation and recovery verification.

The current implementation monitors an Amazon EC2 instance for high CPU utilization and processes the resulting incident through Amazon CloudWatch, Amazon SNS, AWS Lambda, and Amazon S3.

## Architecture

```text
                         +------------------+
                         |   Amazon EC2     |
                         | Monitoring Server|
                         +--------+---------+
                                  |
                                  | CPUUtilization
                                  v
                         +------------------+
                         | Amazon CloudWatch|
                         +--------+---------+
                                  |
                                  | CPU > 70%
                                  v
                         +------------------+
                         | CloudWatch Alarm |
                         | Incident-High-CPU|
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         |   Amazon SNS     |
                         | incident-alerts  |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             +-------------+             +-------------+
             |    Email    |             | AWS Lambda  |
             | Notification|             | Incident   |
             +-------------+             | Handler    |
                                          +------+------+
                                                 |
                                                 | PutObject
                                                 v
                                          +-------------+
                                          | Amazon S3   |
                                          | Incident    |
                                          | JSON Records|
                                          +-------------+
