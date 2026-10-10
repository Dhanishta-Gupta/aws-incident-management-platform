import json
import re
import boto3
import hashlib
from datetime import datetime, timezone

s3 = boto3.client("s3", region_name="ap-southeast-2")

BUCKET = "incident-platform-dhanishta-469465347904-ap-southeast-2-an"


def lambda_handler(event, context):
    sns_message = event["Records"][0]["Sns"]
    raw_message = sns_message.get("Message", "")
    alarm_data = {}

    try:
        parsed_message = json.loads(raw_message)
        if isinstance(parsed_message, dict):
            alarm_data = parsed_message
    except (json.JSONDecodeError, TypeError):
        pass

    alarm_name = alarm_data.get("AlarmName")
    alarm_arn = alarm_data.get("AlarmArn", alarm_name)
    alarm_state = alarm_data.get("NewStateValue")
    state_reason = alarm_data.get("NewStateReason", "")
    trigger = alarm_data.get("Trigger", {})
    dimensions = trigger.get("Dimensions", [])

    instance_id = next(
        (
            dimension.get("value")
            for dimension in dimensions
            if dimension.get("name") == "InstanceId"
        ),
        None,
    )

    # We need an alarm name and state to process the notification.
    if not alarm_name or alarm_state not in ("ALARM", "OK"):
        print(f"Ignoring unsupported notification: {alarm_state}")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Notification ignored"}),
        }

    # Build a stable key for this alarm and instance.
    identity = f"{alarm_arn}|{instance_id or 'no-instance-id'}"
    reference_id = hashlib.sha256(identity.encode()).hexdigest()
    reference_key = f"active-incidents/{reference_id}.json"

    if alarm_state == "ALARM":
        # Check whether an incident is already active.
        try:
            response = s3.get_object(
                Bucket=BUCKET,
                Key=reference_key,
            )
            active_reference = json.loads(
                response["Body"].read().decode("utf-8")
            )

            print(
                "An active incident already exists: "
                f"{active_reference['incident_id']}"
            )
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Active incident already exists",
                    "incident_id": active_reference["incident_id"],
                }),
            }

        except s3.exceptions.NoSuchKey:
            pass

        observed_match = re.search(
            r"datapoints?\s+\[([0-9.eE+-]+)",
            state_reason,
            re.IGNORECASE,
        )
        observed_value = (
            float(observed_match.group(1))
            if observed_match
            else None
        )

        incident_id = context.aws_request_id
        incident_key = f"incidents/{incident_id}.json"

        incident = {
            "incident_id": incident_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": "HIGH",
            "source": "CloudWatch",
            "alert": alarm_name,
            "alarm_arn": alarm_arn,
            "alarm_state": "ALARM",
            "old_alarm_state": alarm_data.get("OldStateValue"),
            "metric_name": trigger.get("MetricName"),
            "threshold": trigger.get("Threshold"),
            "observed_value": observed_value,
            "instance_id": instance_id,
            "region": alarm_data.get("Region"),
            "message": state_reason or raw_message,
            "status": "OPEN",
        }

        # Save the incident's historical record.
        s3.put_object(
            Bucket=BUCKET,
            Key=incident_key,
            Body=json.dumps(incident, indent=2),
            ContentType="application/json",
        )

        # Save a reference to the active incident.
        active_reference = {
            "incident_id": incident_id,
            "incident_key": incident_key,
            "alarm_name": alarm_name,
            "alarm_arn": alarm_arn,
            "instance_id": instance_id,
        }

        s3.put_object(
            Bucket=BUCKET,
            Key=reference_key,
            Body=json.dumps(active_reference, indent=2),
            ContentType="application/json",
        )

        print(f"Incident created: s3://{BUCKET}/{incident_key}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Incident created",
                "incident_id": incident_id,
                "s3_key": incident_key,
            }),
        }

    # Handle recovery: the alarm has returned to OK.
    try:
        response = s3.get_object(
            Bucket=BUCKET,
            Key=reference_key,
        )
        active_reference = json.loads(
            response["Body"].read().decode("utf-8")
        )
    except s3.exceptions.NoSuchKey:
        print("Recovery received, but no active incident was found.")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "No active incident to resolve",
            }),
        }

    incident_key = active_reference["incident_key"]

    response = s3.get_object(
        Bucket=BUCKET,
        Key=incident_key,
    )
    incident = json.loads(response["Body"].read().decode("utf-8"))

    incident["status"] = "RESOLVED"
    incident["resolved_at"] = datetime.now(timezone.utc).isoformat()
    incident["resolution_alarm_state"] = "OK"
    incident["resolution_message"] = state_reason or raw_message

    # Update the same incident record; don't create a new one.
    s3.put_object(
        Bucket=BUCKET,
        Key=incident_key,
        Body=json.dumps(incident, indent=2),
        ContentType="application/json",
    )

    # Remove the active reference after resolving the incident.
    s3.delete_object(
        Bucket=BUCKET,
        Key=reference_key,
    )

    print(f"Incident resolved: s3://{BUCKET}/{incident_key}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Incident resolved",
            "incident_id": incident["incident_id"],
            "s3_key": incident_key,
        }),
    }
