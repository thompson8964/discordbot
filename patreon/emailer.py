import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import toml
from hash import hashGen
import time

def emailSender(recipient):

    with open('../config.toml', 'r') as f:
         data = toml.load(f)
    # Sender's email credentials
    sender_email = data["email"]
    sender_password = data["email_pswd"]

    # Recipient's email address
    recipient_email = recipient

    # Email content
    subject = 'Verification Code'

    # Generate the unique hash

    verification_code = hashGen()

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
    
    </head>
    <body>
        <h2 style="text-align:center; ">Thank you for supporting us!</h2>
        <p style="text-align:center; font-size: 18px;">Your verification code is:</h2>
        <div class="verification-code">
            <h3 style="text-align:center; ">{verification_code}</h3>
        </div>
        <p style="text-align: center;">To verify, you need to private message "/verify {verification_code}" to ChatGPT bot#1012 on Discord.</p>
        <p style="text-align: center;">Do not share this code. Once you verify, we will not ask for this code.</p>
    </body>
    </html>
    '''

    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add the message body

        msg.attach(MIMEText(html_content, 'html'))
        # Connect to the SMTP server (Gmail SMTP server in this case)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print('Email sent successfully!')

        # Disconnect from the server
        server.quit()
        return verification_code
    except Exception as e:
        print(f'Error: {str(e)}')
