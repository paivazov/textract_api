import json
from typing import Optional

import boto3

db = boto3.resource("dynamodb")
s3 = boto3.client("s3")
table_name = "FileResults"


def lambda_handler(event, context):
    file_id = event["pathParameters"]["file_id"]

    textract_results = get_textract_results(file_id)

    if textract_results:
        response = {"statusCode": 200, "body": json.dumps(textract_results)}
    else:
        response = {"statusCode": 404, "body": json.dumps({"detail": "File not found."})}

    return response


def get_textract_results(file_id: str) -> Optional[dict]:
    table = db.Table(table_name)

    try:
        response = table.get_item(
            Key={"file_id": file_id}, ProjectionExpression="file_id, #txt", ExpressionAttributeNames={"#txt": "text"}
        )
        item = response.get("Item")

        print(f"item {response}")
        return item
    except Exception as e:
        print(f"Error retrieving data from DynamoDB: {e}")
        return None
