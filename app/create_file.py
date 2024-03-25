from uuid import uuid4

import boto3

s3_client = boto3.client("s3")
db = boto3.resource("dynamodb")
table_name = "FileResults"
bucket_name = "images-extract-text"


def lambda_handler(event, context):
    callback_url = event["callback_url"]
    file_id = str(uuid4())

    upload_url = generate_upload_url(file_id)

    if upload_url:
        db.Table(table_name).put_item(Item={"file_id": file_id, "callback_url": callback_url, "upload_url": upload_url})
    else:
        return {"statusCode": 500, "body": {"detail": "upload_url hasn't been created."}}

    return {
        "statusCode": 200,
        "body": {"file_id": file_id, "callback_url": callback_url, "upload_url": upload_url},
    }


def generate_upload_url(file_id: str) -> str:
    return s3_client.generate_presigned_url(
        "put_object", Params={"Bucket": bucket_name, "Key": file_id}, ExpiresIn=3600
    )
