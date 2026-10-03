# AWS Services

## 1. Amazon CloudWatch

Purpose:
Monitor AWS resources, applications, metrics, logs, and system health.

Role in this project:
CloudWatch will be used to detect conditions that may indicate an incident and trigger alarms.

---

## 2. Amazon SNS

Purpose:
Send notifications to subscribers or other systems.

Role in this project:
SNS will deliver incident notifications when a CloudWatch alarm is triggered.

---

## 3. AWS Lambda

Purpose:
Run code without managing servers.

Role in this project:
Lambda will perform automated incident-handling actions when required.

---

## 4. Amazon S3

Purpose:
Store objects such as files, logs, reports, and other data.

Role in this project:
S3 will be used to store incident-related data and reports where required.

---

## 5. AWS IAM

Purpose:
Manage authentication and authorization for AWS resources.

Role in this project:
IAM will control who or what can access the resources used by the platform.

---

## Service Interaction

CloudWatch
    ↓
CloudWatch Alarm
    ↓
SNS
    ↓
Notification

Lambda will support automated response actions.

S3 will provide storage for incident-related data.

IAM will control permissions for the AWS resources.
