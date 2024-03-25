from typing import Optional

import boto3
import requests  # via Lambda layer

db = boto3.resource("dynamodb")
table_name = "FileResults"


def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"] == "MODIFY":
            file_id = record["dynamodb"]["Keys"]["file_id"]["S"]

            item = get_textract_results_for_callback(file_id)

            if item and "callback_url" in item:
                callback_url = item.get("callback_url")
                textract_result = item.get("textract_result", "<no text found>")
                send_callback(callback_url, file_id, textract_result)


def get_textract_results_for_callback(file_id: str) -> Optional[dict]:
    table = db.Table(table_name)

    try:
        response = table.get_item(
            Key={"file_id": file_id},
            ProjectionExpression="file_id, callback_url, #txt",
            ExpressionAttributeNames={"#txt": "text"},
        )
        item = response.get("Item")
        return item
    except Exception as e:
        print(f"Error retrieving data from DynamoDB: {e}")
        return None


def send_callback(callback_url: str, file_id: str, text: str) -> None:
    response = requests.post(callback_url, json={"file_id": file_id, "text": text})
    response.raise_for_status()
