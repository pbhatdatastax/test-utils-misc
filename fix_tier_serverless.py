# login using command "aws sso login --profile dmc-prod"
# Edit line 19 and line 21 to specify the profile and environment.
# Edit line 57 to specify file name which contains DB ID in 2nd column after a tab.
from multiprocessing import Pool
import string
import boto3
import botocore
import json

def object_exists(bucket: str, key: str) -> bool:
    boto3.setup_default_session(profile_name='dmc-prod')
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except:
        return False

def process_item(itemname):
    boto3.setup_default_session(profile_name='dmc-prod')
    s3_obj = boto3.client('s3')
    env = "prod"
    bucketname = "datastax-cluster-config-"+env
    object_key = itemname + "/metadata"
    object_key1 = itemname + "-1/metadata"
    #print(itemname)
    
    if object_exists(bucketname, object_key):
        #object_dc = s3_obj.Object(bucketname, object_key)
        body = json.loads(s3_obj.get_object(Bucket=bucketname, Key=object_key)['Body'].read())
        if "tier" in body:
            print("tier exists", body["clusterUUID"])
        else:
            body['tier'] = "serverless"
            #print(body)
            s3_obj.put_object(Body=json.dumps(body), Bucket=bucketname, Key=object_key)
            print("updated key", body["clusterUUID"])


    elif object_exists(bucketname, object_key1):
        body = json.loads(s3_obj.get_object(Bucket=bucketname, Key=object_key1)['Body'].read())
        if "tier" in body:
             print("tier exists", body["clusterUUID"])
        else:
            body['tier'] = "serverless"
            #print(body)
            s3_obj.put_object(Body=json.dumps(body), Bucket=bucketname, Key=object_key1)
            print("updated key1", body["clusterUUID"])
            
    else:
        object_dc = None
        print("no DB UUID %s in s3", object_key1)
        
             

if __name__ == '__main__':
    filename = 'us-east1_astra-serverless-prod-22'  # replace with your filename
    block = []  
    with open(filename, 'r') as file:
        for line in file:
            # strip newline character and any leading/trailing whitespaces
            stripped_line = line.strip()
            #print(stripped_line)
            db_uuid = stripped_line.split("\t")[1]
            block.append(db_uuid)
    
    #print(block)
    with Pool(processes=25) as pool:  # Adjust the number of processes as needed
           pool.map(process_item, block)     

