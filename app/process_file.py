import json
import urllib.parse

import boto3

s3 = boto3.client("s3")
db = boto3.resource("dynamodb")
textract = boto3.client("textract")


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    try:
        detected_text = get_textract_data(bucket, key)
        write_text_to_db(key, detected_text)

        return {"statusCode": 200, "body": json.dumps({"detected_text": detected_text, "file_id": key})}

    except Exception as e:
        print(str(e))
        detail = f"Error getting object {key} from bucket {bucket}."
        return {"statusCode": 400, "body": json.dumps({"detail": detail})}


def get_textract_data(bucket_name: str, document_key: str) -> str:
    response = textract.detect_document_text(Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}})

    detected_text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            detected_text += item["Text"] + "\n"
    return detected_text


def write_text_to_db(file_id: str, textract_data: str) -> None:
    table_name = "FileResults"

    db.Table(table_name).update_item(
        Key={"file_id": file_id},
        UpdateExpression="SET #txt = :t",
        ExpressionAttributeValues={":t": textract_data},
        ExpressionAttributeNames={"#txt": "text"},
    )
