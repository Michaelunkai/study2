# send_sms.py
from twilio.rest import Client

# Your Twilio account SID and Auth Token from twilio.com/console
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)

# Send an SMS message
message = client.messages.create(
    body='Hello, this is a test message from Twilio!',
    from_='+12345678901',  # Your Twilio phone number
    to='+972123456789'     # Recipient's phone number in Israel, correctly formatted
)

print(f"Message sent with SID: {message.sid}")
