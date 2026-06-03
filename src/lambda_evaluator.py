import json

def lambda_handler(event, context):
    print("Received Compliance Event From EventBridge:")
    print(json.dumps(event, indent=2))
    
    detail = event.get('detail', {})
    compliance = detail.get('newEvaluationResult', {}).get('complianceType')
    resource_id = detail.get('resourceId')
    
    return {
        "statusCode": 200,
        "resourceId": resource_id,
        "complianceStatus": compliance,
        "executionMessage": f"Evaluated resource {resource_id}. Status: {compliance}"
    }
