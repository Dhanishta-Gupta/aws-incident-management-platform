# Incident Response Runbook

## Purpose

This runbook describes the steps to investigate and respond to a high-CPU incident detected on the EC2 instance monitored by the AWS Incident Management Platform.

It provides a repeatable procedure for detecting the incident, investigating the affected resource, taking corrective action, and verifying recovery.

---

## Incident Scenario

The current platform monitors EC2 CPU utilization using Amazon CloudWatch.

The configured alarm is:

`Incident-High-CPU`

The alarm triggers when:

`CPU utilization > 70%`

for one datapoint within a five-minute evaluation period.

---

## 1. Receive the Alert

When the CPU threshold is exceeded:

```text
EC2
 ↓
CloudWatch
 ↓
Incident-High-CPU
 ↓
SNS
 ├──→ Email
 └──→ Lambda
