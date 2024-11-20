from twilio.rest import Client

def send_sms(to_number, body):
    try:
        # Twilio Account SID and Auth Token (Replace with your Twilio credentials)
        account_sid = 'your_account_sid'
        auth_token = 'your_auth_token'

        # Create a client to interact with Twilio
        client = Client(account_sid, auth_token)

        # Send the SMS
        message = client.messages.create(
            body=body,
            from_='+1234567890',  # Replace with your Twilio phone number
            to=to_number
        )

        print(f"SMS sent to {to_number}: {message.sid}")
    except Exception as e:
        print(f"Error: {e}")
