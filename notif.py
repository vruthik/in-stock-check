import smtplib

def send_email_notif(login_creds, recipient_emails, subject, body):
    user = login_creds['username']
    password = login_creds['password']

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (user, ", ".join(recipient_emails), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(user, password)
        smtp_server.sendmail(user, recipient_emails, email_text)
        smtp_server.close()
        print("Email sent successfully!")

    except Exception as ex:
        print(ex)
