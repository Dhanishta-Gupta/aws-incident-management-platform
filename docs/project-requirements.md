# AWS Incident Management Platform

## Project Objective

Build a practical cloud-based incident management platform using AWS services to monitor an EC2 instance, detect high CPU utilization, generate incident notifications, process incident events, and store structured incident records for investigation and response.

## Project Scope

The current project focuses on infrastructure incident detection and response for an Amazon EC2 instance.

The implemented workflow covers:

- Monitoring EC2 CPU utilization using Amazon CloudWatch.
- Detecting high CPU utilization using a CloudWatch alarm.
- Sending incident notifications through Amazon SNS.
- Processing incident events using AWS Lambda.
- Storing structured incident records in Amazon S3.
- Supporting manual investigation and remediation through an incident response runbook.
- Verifying recovery through monitoring and system checks.

The project is intentionally being developed incrementally, with additional monitoring and automated remediation planned as future enhancements.

---

## Functional Requirements

The platform should provide the following capabilities:

### Monitoring

- Monitor an Amazon EC2 instance using Amazon CloudWatch.
- Collect and evaluate CPU utilization metrics.
- Detect high CPU utilization using a configured alarm threshold.

### Incident Detection

- Trigger the `Incident-High-CPU` CloudWatch alarm when CPU utilization exceeds the configured threshold.
- Identify the affected EC2 instance associated with the monitoring alarm.

### Incident Notification

- Publish incident alarm notifications through Amazon SNS.
- Deliver incident notifications through email.
- Forward the incident event to AWS Lambda for automated processing.

### Incident Processing

- Receive and process incident events using AWS Lambda.
- Extract relevant information from the incident event.
- Generate a structured incident record.

### Incident Storage

- Store structured incident records as JSON objects in Amazon S3.
- Maintain incident information that can be reviewed during investigation and response.

### Incident Response

- Provide an operational procedure for investigating incidents.
- Support investigation using CloudWatch metrics, logs, and EC2 system-level information.
- Provide steps for safe remediation and recovery verification.
- Document incidents for future reference.

---

## AWS Services

The project uses the following AWS services:

- **Amazon EC2** — Provides the compute environment monitored for infrastructure incidents.
- **Amazon CloudWatch** — Collects EC2 metrics and evaluates alarm conditions.
- **Amazon SNS** — Delivers incident notifications and forwards alarm events to AWS Lambda.
- **AWS Lambda** — Processes incident events and generates structured incident records.
- **Amazon S3** — Stores structured incident records in JSON format.
- **AWS IAM** — Provides identity and access control using roles and permissions.

## Non-Functional Requirements

### Reliability

- Monitoring and alerting should operate consistently for the configured EC2 instance.
- Incident records should be stored reliably in Amazon S3.

### Security

- AWS IAM roles should be used where possible instead of storing long-term access keys on the EC2 instance.
- Amazon S3 should remain private and protected by appropriate access controls.
- AWS resources should follow the principle of least privilege where practical.

### Observability

- CloudWatch should provide visibility into EC2 resource utilization.
- Incident events should be traceable through the monitoring, notification, processing, and storage workflow.

### Maintainability

- Project documentation should clearly describe the architecture and operational procedures.
- Infrastructure, scripts, and documentation should be organized in separate repository directories.
- Git and GitHub should be used for version control.

---

## Current Limitations

The current implementation has the following limitations:

- The primary monitoring scenario is high CPU utilization on an EC2 instance.
- Automated incident records currently represent incidents as `OPEN`.
- Automatic transition from `OPEN` to `RESOLVED` has not yet been implemented.
- Monitoring and log collection can be expanded with additional CloudWatch Agent configuration.
- Automated remediation is not currently implemented.
- The project does not yet use Infrastructure as Code.

---

## Future Requirements

Future versions of the platform may include:

- Additional EC2 and application-level monitoring metrics.
- Log-based CloudWatch alarms.
- Automatic incident resolution based on recovery events.
- AWS Systems Manager integration for operational troubleshooting.
- Automated remediation for selected incident types.
- Incident dashboards and reporting.
- Infrastructure as Code using AWS CloudFormation or Terraform.
- Additional security controls and least-privilege improvements.
- More advanced incident analysis and reporting.

---

## Project Skills

This project is intended to develop practical skills in:

- AWS infrastructure management
- Linux administration and troubleshooting
- Cloud monitoring and observability
- Incident detection and response
- IAM and cloud security fundamentals
- AWS networking fundamentals
- Automation and scripting
- Git and GitHub
- Operational documentation
- Cloud incident-management practices
