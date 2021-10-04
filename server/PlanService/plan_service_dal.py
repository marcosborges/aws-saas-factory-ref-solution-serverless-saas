# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from pprint import pprint
import os
import boto3
from botocore.exceptions import ClientError
import uuid
import json
import logger
import random
import threading

from plan_models import Plan
from types import SimpleNamespace
from boto3.dynamodb.conditions import Key


is_pooled_deploy = os.environ['IS_POOLED_DEPLOY']
table_name = os.environ['PLAN_TABLE_NAME']
dynamodb = None

suffix_start = 1 
suffix_end = 10

def get_plan(event, key):
    table = __get_dynamodb_table(event, dynamodb)
    
    try:
        shardId = key.split(":")[0]
        planId = key.split(":")[1] 
        logger.log_with_tenant_context(event, shardId)
        logger.log_with_tenant_context(event, planId)
        response = table.get_item(Key={'shardId': shardId, 'planId': planId})
        item = response['Item']
        
        plan = Plan(item['shardId'], item['planId'], item['name'], item['description'], item['duration'], item['avgRequestsPerUser'], item['totalUsers'])
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise Exception('Error getting a plan', e)
    else:
        logger.info("GetItem succeeded:"+ str(plan))
        return plan

def deleplan(event, key):
    table = __get_dynamodb_table(event, dynamodb)
    
    try:
        shardId = key.split(":")[0]
        planId = key.split(":")[1] 
        response = table.delete_item(Key={'shardId':shardId, 'planId': planId})
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise Exception('Error deleting a plan', e)
    else:
        logger.info("DeleteItem succeeded:")
        return response


def creaplan(event, payload):
    tenantId = event['requestContext']['authorizer']['tenantId']    
    table = __get_dynamodb_table(event, dynamodb)

    
    suffix = random.randrange(suffix_start, suffix_end)
    shardId = tenantId+"-"+str(suffix)

    plan = Plan(shardId, str(uuid.uuid4()), payload.name, payload.description, payload.duration, payload.avgRequestsPerUser, payload.totalUsers)
    
    try:
        response = table.put_item(
            Item=
                {
                    'shardId': shardId,  
                    'planId': plan.planId,
                    'name': plan.name,
                    'description': plan.description,
                    'duration': plan.duration,
                    'avgRequestsPerUser': plan.avgRequestsPerUser,
                    'totalUsers': plan.totalUsers
                }
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise Exception('Error adding a plan', e)
    else:
        logger.info("PutItem succeeded:")
        return plan

def updaplan(event, payload, key):
    table = __get_dynamodb_table(event, dynamodb)
    
    try:
        shardId = key.split(":")[0]
        planId = key.split(":")[1] 
        logger.log_with_tenant_context(event, shardId)
        logger.log_with_tenant_context(event, planId)
        plan = Plan(shardId, planId, payload.name, payload.description, payload.duration, payload.avgRequestsPerUser, payload.totalUsers)
        response = table.update_item(Key={'shardId':plan.shardId, 'planId': plan.planId},
        UpdateExpression="set description=:description, #n=:planName, duration=:duration, avgRequestsPerUser=:avgRequestsPerUser, totalUsers=:totalUsers",
        ExpressionAttributeNames= {'#n':'name'},
        ExpressionAttributeValues={
            ':planName': plan.name,
            ':description': plan.description,
            ':duration': plan.duration,
            ':avgRequestsPerUser': plan.avgRequestsPerUser,
            ':totalUsers': plan.totalUsers
        },
        ReturnValues="UPDATED_NEW")
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise Exception('Error updating a plan', e)
    else:
        logger.info("UpdateItem succeeded:")
        return plan        

def get_plans(event, tenantId):    
    table = __get_dynamodb_table(event, dynamodb)
    get_all_plans_response =[]
    try:
        __query_all_partitions(tenantId,get_all_plans_response, table)
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        raise Exception('Error getting all plans', e)
    else:
        logger.info("Get plans succeeded")
        return get_all_plans_response

def __query_all_partitions(tenantId,get_all_plans_response, table):
    threads = []    
    
    for suffix in range(suffix_start, suffix_end):
        partition_id = tenantId+'-'+str(suffix)
        
        thread = threading.Thread(target=__get_tenant_data, args=[partition_id, get_all_plans_response, table])
        threads.append(thread)
        
    # Start threads
    for thread in threads:
        thread.start()
    # Ensure all threads are finished
    for thread in threads:
        thread.join()
           
def __get_tenant_data(partition_id, get_all_plans_response, table):    
    logger.info(partition_id)
    response = table.query(KeyConditionExpression=Key('shardId').eq(partition_id))    
    if (len(response['Items']) > 0):
        for item in response['Items']:
            plan = Plan(item['shardId'], item['planId'], item['name'], item['description'], item['duration'], item['avgRequestsPerUser'], item['totalUsers'])
            get_all_plans_response.append(plan)

def __get_dynamodb_table(event, dynamodb):    
    if (is_pooled_deploy=='true'):
        accesskey = event['requestContext']['authorizer']['accesskey']
        secretkey = event['requestContext']['authorizer']['secretkey']
        sessiontoken = event['requestContext']['authorizer']['sessiontoken']    
        dynamodb = boto3.resource('dynamodb',
                aws_access_key_id=accesskey,
                aws_secret_access_key=secretkey,
                aws_session_token=sessiontoken
                )       
    else:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')
        
    return dynamodb.Table(table_name)
