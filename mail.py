import smtplib

gmail_user = 'your_email_address'
gmail_password = 'your_password'

sent_from = gmail_user

def send_email(email,body):
    to = [email]
    subject = 'Weather_Today'
    body = body

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as e:
        print("Something went wrong.", e)
