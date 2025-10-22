import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    """
    Lambda handler for REST API
    """
    table_name = os.environ.get('TABLE_NAME', 'items-table')
    table = dynamodb.Table(table_name)
    
    http_method = event.get('httpMethod', 'GET')
    
    try:
        if http_method == 'GET':
            response = table.scan()
            items = response.get('Items', [])
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'items': items,
                    'count': len(items)
                })
            }
        
        elif http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            
            item = {
                'id': str(uuid.uuid4()),
                'name': body.get('name', 'Unnamed Item'),
                'description': body.get('description', ''),
                'created_at': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=item)
            
            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Item created successfully',
                    'item': item
                })
            }
        
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal server error'})
        }
