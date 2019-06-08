from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')
    
    # Create reply
    resp = MessagingResponse()
    file=fetch_reply(msg,sender)
    if type(file)=="class 'dict'":
        resp.message(file[1]).media(file[2])
    else :
        resp.message(file)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

