
## Textract api
___


### To generate pre-signed url, use this link:
```shell
https://ru5u8dgc22.execute-api.eu-central-1.amazonaws.com/dev/files
```
with next request body:
```json
{
    "callback_url": "some_url.com"
}
```
After proceeding text extraction, API will send resulted text and id of uploaded file on callback_url 

### To get text using file_id:
```shell
https://ru5u8dgc22.execute-api.eu-central-1.amazonaws.com/dev/files/{file_id}
```
___

#### NOTE
[serverless.yml](serverless.yml) file can be reviewed only as a sample of infrastructure. It doesn't work because I need a little more time to deal with serverless framework.
