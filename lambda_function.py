import json
import boto3
from urllib.parse import parse_qs

def lambda_handler(event, context):
    try:
        # Log the event for debugging purposes
        print("Event: ", event)
        
        # Parse the body as URL-encoded form data
        body = parse_qs(event['body'])
        
        # Extract the email and cryptos values
        email = body.get('email', [None])[0]
        cryptos = body.get('cryptos', [])

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

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing request: {str(e)}')
        }
