import json
import boto3
from urllib.parse import parse_qs

def lambda_handler(event, context):
    # Check if body is URL-encoded
    if event['headers']['Content-Type'] == 'application/x-www-form-urlencoded':
        body = parse_qs(event['body'])
        email = body.get('email', [None])[0]
        cryptos = body.get('cryptos', [])
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported content type')
        }

    if not email or not cryptos:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required fields')
        }

    # Store user data in DynamoDB (or any other database)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CryptoWatcherSubscribers')
    table.put_item(
        Item={
            'email': email,
            'cryptos': cryptos
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Subscription successful!')
    }
