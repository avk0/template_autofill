import base64
import boto3
import json

#import src


def lambda_handler(event, context):
    print('Event keys: ' + '; '.join(list(event.keys())))

    bucket = "autofill-template-s3b"

    res = {
        'headers': {"Content-Type": "text/html"},
        'statusCode': 200
    }

    # Save input files
    if 1:
        try:
            def save_b64_obj_to_s3(file_b64, fname, s3_client, bucket):
                print('File name to save to S3: ', fname)
                file_b64 = file_b64[file_b64.find(",")+1:]
                file = base64.b64decode(file_b64)

                s3_client.put_object(Bucket=bucket, Key=fname, Body=file)
                url = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': bucket,
                                                               'Key': fname},
                                                       ExpiresIn=1200)
                print("url", json.dumps(url))
                return url

            s3_client = boto3.client('s3')
            url1 = save_b64_obj_to_s3(
                event['file1'], event['fname1'], s3_client, bucket)
            url2 = save_b64_obj_to_s3(
                event['file2'], event['fname2'], s3_client, bucket)

            res['body'] = 'input files saved'

        except Exception as e:
            print(e)
            res['body'] = 'FAILED input files saving'

    # Main
    if 0:
        try:
            pres = src.read_presentation(url1)
            data = src.read_data(url2)
            print('Files read')
            new_pres = src.fill_pres_with_data(pres, data)
            print('PPT filled')
            src.save_presentation(new_pres, save_path)
            print('Output PPT saved')
            res['body'] += ', output PPT saved'
        except Exception as e:
            print(e)
            res['body'] += ', FAILED output PPT'

    # Return link to result S3 file
    if 1:
        res_url = s3_client.generate_presigned_url('get_object',
                                                   Params={'Bucket': bucket,
                                                           # 'Key': 'static/img/exel.png',
                                                           'Key': event['fname1']},
                                                   ExpiresIn=1200)

        res = {'statusCode': 301, 'body': res_url}

    return res
