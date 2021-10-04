# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import utils
import logger
import metrics_manager
import plan_service_dal
from aws_lambda_powertools import Tracer
from types import SimpleNamespace
tracer = Tracer()

@tracer.capture_lambda_handler
def get_plan(event, context):
    tenantId = event['requestContext']['authorizer']['tenantId']
    tracer.put_annotation(key="TenantId", value=tenantId)
    
    logger.log_with_tenant_context(event, "Request received to get a plan")
    params = event['pathParameters']
    logger.log_with_tenant_context(event, params)
    key = params['id']
    logger.log_with_tenant_context(event, key)
    plan = plan_service_dal.get_plan(event, key)

    logger.log_with_tenant_context(event, "Request completed to get a plan")
    metrics_manager.record_metric(event, "SingleplanRequested", "Count", 1)
    return utils.generate_response(plan)
    
@tracer.capture_lambda_handler
def create_plan(event, context):    
    tenantId = event['requestContext']['authorizer']['tenantId']
    tracer.put_annotation(key="TenantId", value=tenantId)

    logger.log_with_tenant_context(event, "Request received to create a plan")
    payload = json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d))
    plan = plan_service_dal.create_plan(event, payload)
    logger.log_with_tenant_context(event, "Request completed to create a plan")
    metrics_manager.record_metric(event, "PlanCreated", "Count", 1)
    return utils.generate_response(plan)
    
@tracer.capture_lambda_handler
def update_plan(event, context):
    tenantId = event['requestContext']['authorizer']['tenantId']
    tracer.put_annotation(key="TenantId", value=tenantId)

    logger.log_with_tenant_context(event, "Request received to update a plan")
    payload = json.loads(event['body'], object_hook=lambda d: SimpleNamespace(**d))
    params = event['pathParameters']
    key = params['id']
    plan = plan_service_dal.update_plan(event, payload, key)
    logger.log_with_tenant_context(event, "Request completed to update a plan") 
    metrics_manager.record_metric(event, "PlanUpdated", "Count", 1)   
    return utils.generate_response(plan)

@tracer.capture_lambda_handler
def delete_plan(event, context):
    tenantId = event['requestContext']['authorizer']['tenantId']
    tracer.put_annotation(key="TenantId", value=tenantId)

    logger.log_with_tenant_context(event, "Request received to delete a plan")
    params = event['pathParameters']
    key = params['id']
    response = plan_service_dal.delete_plan(event, key)
    logger.log_with_tenant_context(event, "Request completed to delete a plan")
    metrics_manager.record_metric(event, "PlanDeleted", "Count", 1)
    return utils.create_success_response("Successfully deleted the plan")

@tracer.capture_lambda_handler
def get_plans(event, context):
    tenantId = event['requestContext']['authorizer']['tenantId']
    tracer.put_annotation(key="TenantId", value=tenantId)
    
    logger.log_with_tenant_context(event, "Request received to get all plans")
    response = plan_service_dal.get_plans(event, tenantId)
    metrics_manager.record_metric(event, "PlansRetrieved", "Count", len(response))
    logger.log_with_tenant_context(event, "Request completed to get all plans")
    return utils.generate_response(response)

  