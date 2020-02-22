from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC24fc9ac27dee145f04d855b99b666ab8"
# Your Auth Token from twilio.com/console
auth_token  = "08da7fc65a1b8163f17aa324ddef479d"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+17203643760", 
    from_="+14159939395",
    body="Hello from Python!")

print(message.sid)
