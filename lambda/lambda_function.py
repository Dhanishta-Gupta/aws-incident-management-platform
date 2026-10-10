import json
import re
import boto3
from datetime import datetime, timezone

s3 = boto3.client("s3", region_name="ap-southeast-2")

BUCKET = "incident-platform-dhanishta-469465347904-ap-southeast-2-an"


def lambda_handler(event, context):
    sns_message = event["Records"][0]["Sns"]

    raw_message = sns_message.get("Message", "")
    alarm_data = {}

    # CloudWatch sends its alarm details as JSON inside the SNS message.
    try:
        parsed_message = json.loads(raw_message)

        if isinstance(parsed_message, dict):
            alarm_data = parsed_message
    except (json.JSONDecodeError, TypeError):
        # Ordinary text messages are still handled safely.
        pass

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

    state_reason = alarm_data.get("NewStateReason", "")
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

    incident = {
        "incident_id": context.aws_request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "severity": "HIGH",
        "source": "CloudWatch" if alarm_data.get("AlarmName") else "SNS",
        "alert": alarm_data.get(
            "AlarmName",
            sns_message.get("Subject", "CloudWatch Alert"),
        ),
        "alarm_state": alarm_data.get("NewStateValue"),
        "old_alarm_state": alarm_data.get("OldStateValue"),
        "metric_name": trigger.get("MetricName"),
        "threshold": trigger.get("Threshold"),
        "observed_value": observed_value,
        "instance_id": instance_id,
        "region": alarm_data.get("Region"),
        "message": state_reason or raw_message,
        "status": "OPEN",
    }

    key = f"incidents/{incident['incident_id']}.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(incident, indent=2),
        ContentType="application/json",
    )

    print(f"Incident record created: s3://{BUCKET}/{key}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Incident record created",
            "s3_key": key,
        }),
    }
