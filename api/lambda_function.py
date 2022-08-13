import base64
import boto3
from io import BytesIO
import json

import src


def lambda_handler(event, context):
    print('Event keys: ' + '; '.join(list(event.keys())))

    bucket = "autofill-template-s3b"

    res = {
        'headers': {"Content-Type": "text/html"},
        'statusCode': 200,
        'body': ''
    }

    # Save input files
    if 0:
        try:
            def save_b64_obj_to_s3(file_b64, fname, s3_client, bucket):
                print('File name to save to S3: ', fname)
                file_b64 = file_b64[file_b64.find(",")+1:]
                file = base64.b64decode(file_b64)

                s3_client.put_object(Bucket=bucket, Key=fname, Body=file)
                url = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': bucket,
                                                               'Key': fname},
                                                       ExpiresIn=(12*3600))
                print("url", json.dumps(url))
                return url

            s3_client = boto3.client('s3')
            url1 = save_b64_obj_to_s3(
                event['file1'], event['fname1'], s3_client, bucket)
            url2 = save_b64_obj_to_s3(
                event['file2'], event['fname2'], s3_client, bucket)

            res['body'] += 'input files saved'

        except Exception as e:
            print(e)
            res['body'] += 'FAILED input files saving'

    # Read presentation file

    file_b64 = event['file1']
    file_b64 = file_b64[file_b64.find(",")+1:]
    file = base64.b64decode(file_b64)
    print('file read and decoded')
    pres = src.read_presentation(file)
    print('File1 read')
    
    # Read excel file

    file_b64 = event['file2']
    file_b64 = file_b64[file_b64.find(",")+1:]
    bytes = base64.b64decode(file_b64)
    
    data = src.read_excel(bytes)
    print('File2 read')

    # Fill and save presentation with data as single file

    try:
        new_pres = src.fill_pres_with_data(pres, data)
        print('PPT filled')
        s3_client = boto3.client('s3')
        
        res_fobj = BytesIO()
        new_pres.save(res_fobj)
        res_fobj.seek(0)
        res_file_name = 'filled_pres5.pptx'
        
        s3_client.put_object(Bucket=bucket, 
                            Key=res_file_name, 
                            Body=res_fobj.read())
            
        #src.save_presentation(new_pres, 'tmp')
        print('Output PPT saved')
        res['body'] += ', output PPT saved'
    except Exception as e:
        print(e)
        res['body'] += ', FAILED output PPT'
    
    # Save presentation as separate files in zip archive

    if 0:
        tmp_dir = mkdtemp()
        preprocess_folder = os.path.join(tmp_dir, 'preprocess')
        os.makedirs(preprocess_folder, exist_ok=True)
        zip_folder = os.path.join(tmp_dir, 'zip')
        os.makedirs(zip_folder, exist_ok=True)

        try:
            src.fill_sep_pres_with_data(pres, data, preprocess_folder)
            src.save_files_as_zip(preprocess_folder, os.path.join(
                zip_folder, FILLED_SEPARATE_PPT))
        except Exception as e:
            print(e)
            res['body'] += ', FAILED output PPT'

    # Return link to result S3 file

    res_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': res_file_name},
        ExpiresIn=1200)

    res = {'statusCode': 301, 'body': res_url}

    return res
