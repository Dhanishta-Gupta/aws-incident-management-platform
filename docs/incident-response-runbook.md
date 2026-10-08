# Incident Response Runbook

## 1. Purpose

This runbook provides a standard procedure for responding to infrastructure incidents detected in the AWS environment.

The goal is to:

- Detect incidents quickly.
- Assess the severity and impact.
- Investigate the affected resource.
- Perform safe remediation.
- Verify that the service has recovered.
- Document the incident and the actions taken.

---

## 2. Incident Detection

Incidents are primarily detected through Amazon CloudWatch monitoring and alarms.

Examples include:

- High EC2 CPU utilization
- EC2 instance health problems
- Application or system errors recorded in logs
- Other configured CloudWatch alarms

When a configured threshold is exceeded, CloudWatch changes the alarm state to **ALARM**.

The alarm can publish a notification to an Amazon SNS topic, which sends an email notification to the configured recipient.

### Incident Flow

AWS Resource
     |
     v
Amazon CloudWatch
     |
     v
CloudWatch Alarm
     |
     v
Amazon SNS
     |
     v
Email Notification
     |
     v
Incident Investigation
     |
     v
Remediation
     |
     v
Verification & Documentation

---

## 3. Initial Response

When an incident notification is received:

1. Record the date and time of the alert.
2. Identify the affected AWS resource.
3. Identify which CloudWatch alarm triggered.
4. Check the current alarm state.
5. Determine the severity and potential impact.
6. Begin investigation using CloudWatch metrics and logs.

Do not immediately restart or modify production resources without first understanding the possible cause.

---

## 4. Incident Severity

### Critical

Use this severity when the incident causes or may cause major service disruption or significant impact.

Examples:

- Critical production service unavailable.
- EC2 instance is completely unresponsive.
- Major customer-facing functionality is unavailable.

### High

Use this severity when the service is degraded or a significant resource is affected.

Examples:

- Sustained high CPU utilization.
- Application performance significantly degraded.
- Important system component showing repeated failures.

### Medium

Use this severity when the issue has limited impact but requires investigation.

Examples:

- Temporary increase in resource utilization.
- Non-critical application errors.
- Intermittent warnings in system logs.

### Low

Use this severity for issues that do not currently affect service availability.

Examples:

- Isolated warning messages.
- Short-lived metric spikes.
- Informational alerts requiring monitoring.

---

## 5. Investigation Procedure

### Step 1: Check the CloudWatch Alarm

Open the relevant CloudWatch alarm and verify:

- Alarm name
- Alarm state
- Metric being monitored
- Current metric value
- Configured threshold
- Time the alarm entered the ALARM state

Determine whether the condition is still occurring.

### Step 2: Check EC2

If the incident involves an EC2 instance:

1. Open the Amazon EC2 console.
2. Locate the affected instance.
3. Check the instance state.
4. Check the instance status checks.
5. Review CPU utilization and other available metrics.
6. Confirm whether the instance is reachable.

Do not terminate an instance unless the remediation procedure explicitly requires it.

### Step 3: Connect to the EC2 Instance

If SSH access is available and investigation requires access to the operating system, connect to the instance.

Example:

ssh -i <key-file> ubuntu@<public-ip>

After connecting, verify basic system information using commands such as:

uptime

free -h

df -h

top

These commands help identify CPU, memory, disk, and system-load problems.

### Step 4: Check System Logs

Review relevant system logs when investigating operating-system-level problems.

For example:

sudo tail -n 100 /var/log/syslog

For authentication-related events:

sudo tail -n 100 /var/log/auth.log

Look for:

- Repeated errors
- Failed services
- Resource exhaustion
- Unexpected restarts
- Authentication failures
- Application failures

---

## 6. CPU Utilization Incident

If a CloudWatch alarm reports high EC2 CPU utilization:

### Investigation

1. Confirm the CloudWatch alarm is in the **ALARM** state.
2. Check the CPU utilization graph.
3. Determine whether the increase is temporary or sustained.
4. Connect to the EC2 instance if required.
5. Run the `top` command.
6. Identify processes consuming unusually high CPU.
7. Check whether the process is expected.

### Remediation

Depending on the cause:

- Stop an unnecessary process if it is safe to do so.
- Restart a failed or problematic service if appropriate.
- Investigate the application causing the high utilization.
- Consider scaling the instance if the workload consistently exceeds available capacity.

Do not terminate processes blindly. Confirm the process and its purpose before taking action.

---

## 7. Memory or Disk Incident

If memory usage is high, use:

`free -h`

Check which processes are consuming memory and investigate the cause.

If disk utilization is high, use:

`df -h`

Identify filesystems approaching capacity and investigate large or unnecessary files.

Do not delete system files or logs without understanding their purpose.

---

## 8. CloudWatch Logs

When logs are configured for the EC2 instance, use Amazon CloudWatch Logs to investigate application and system events.

Check:

- Log group
- Log stream
- Timestamp of the incident
- Error messages
- Repeated failures
- Events immediately before the incident

Correlate log events with the time at which the CloudWatch alarm was triggered.

---

## 9. SNS Notification

Amazon SNS is responsible for distributing the CloudWatch alarm notification.

When an alarm enters the **ALARM** state:

CloudWatch Alarm
       |
       v
SNS Topic
       |
       v
Email Subscription

Verify that:

- The SNS topic exists.
- The CloudWatch alarm has the correct SNS action.
- The email subscription is confirmed.
- The notification was delivered.

SNS is used for notification and does not itself determine the root cause of the incident.

---

## 10. Remediation

After identifying the probable cause:

1. Select the least disruptive remediation.
2. Perform the required corrective action.
3. Monitor the affected resource.
4. Confirm that the problem has stopped.
5. Avoid making unnecessary infrastructure changes.

Examples of remediation include:

- Restarting an affected service.
- Stopping an unnecessary process.
- Freeing disk space.
- Correcting a configuration issue.
- Scaling resources when capacity is insufficient.
- Escalating the incident when the root cause cannot be safely resolved.

---

## 11. Recovery Verification

After remediation, verify that the system has recovered.

Check:

- CloudWatch alarm state
- EC2 instance status
- CPU utilization
- Memory utilization
- Disk utilization
- Relevant system and application logs
- Service availability

The CloudWatch alarm should return to the **OK** state once the monitored condition remains below the configured threshold for the required evaluation period.

Do not close the incident solely because the alarm returned to OK. Confirm that the underlying service is functioning correctly.

---

## 12. Incident Documentation

For every significant incident, record:

- Incident ID
- Date and time
- Affected resource
- Alarm name
- Severity
- Symptoms
- Initial investigation
- Root cause, if identified
- Remediation performed
- Recovery time
- Final status
- Lessons learned

Example:

Incident ID: INC-001  
Date: YYYY-MM-DD  
Time: HH:MM  
Severity: High  
Resource: EC2 instance  
Alarm: High CPU Utilization  
Symptom: CPU exceeded configured threshold  
Investigation: Identified high CPU-consuming process  
Remediation: Investigated and stopped the unnecessary process  
Recovery: CPU returned below threshold  
Status: Resolved

---

## 13. Escalation

Escalate the incident when:

- The root cause cannot be identified.
- The issue continues after remediation.
- The affected service is critical.
- Infrastructure changes require additional authorization.
- There is a risk of data loss.
- The incident has significant customer impact.

Provide the next responder with:

- Incident summary
- Relevant CloudWatch alarms
- Metrics
- Logs
- Actions already performed
- Current system state

---

## 14. Post-Incident Review

After a significant incident:

1. Confirm the incident is fully resolved.
2. Identify the root cause.
3. Review whether monitoring detected the problem quickly enough.
4. Determine whether the alert threshold was appropriate.
5. Document corrective and preventive actions.
6. Update the runbook if the incident revealed a missing procedure.

The objective of the post-incident review is to reduce the likelihood and impact of future incidents.

---

## 15. Quick Response Checklist

- [ ] Receive and acknowledge alert.
- [ ] Identify affected resource.
- [ ] Check CloudWatch alarm.
- [ ] Determine incident severity.
- [ ] Check EC2 status and metrics.
- [ ] Review relevant logs.
- [ ] Investigate the probable cause.
- [ ] Perform safe remediation.
- [ ] Monitor recovery.
- [ ] Confirm CloudWatch alarm returns to OK.
- [ ] Verify service functionality.
- [ ] Document the incident.
- [ ] Escalate if required.
- [ ] Perform post-incident review for significant incidents.

---

## 16. Project Architecture Reference

The current incident-management workflow is based on the following AWS components:

- **Amazon EC2** — compute resource being monitored.
- **Amazon CloudWatch** — collects metrics and evaluates alarms.
- **Amazon SNS** — distributes incident notifications.
- **Amazon CloudWatch Logs** — stores and provides access to collected logs.
- **AWS IAM** — controls access to AWS resources.

The architecture can be expanded later with additional automation such as AWS Lambda, AWS Systems Manager, and automated remediation workflows.

---

## 17. Important Safety Notes

- Do not expose AWS access keys or secret credentials in the repository.
- Do not commit private SSH keys.
- Do not make infrastructure changes without understanding their impact.
- Use IAM roles instead of hard-coded credentials wherever possible.
- Follow the principle of least privilege.
- Preserve relevant logs before deleting or modifying resources.
- Prefer reversible remediation actions when possible.
