import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os


def mainMethod():
    # Replace sender@example.com with your "From" address.
    # This address must be verified.
    SENDER = 'krutheeka.rajkumar@gmail.com'
    SENDERNAME = 'Krutheeka'

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT  = 'krutheeka.dev@gmail.com'

    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = os.environ.get("USERNAME_SMTP")

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = os.environ.get("PASSWORD_SMTP")
    # If you're using Amazon SES in an AWS Region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
    # endpoint in the appropriate region.
    HOST = "email-smtp.us-west-2.amazonaws.com"
    PORT = 587

    # The subject line of the email.
    SUBJECT = 'Amazon SES Test (Python smtplib)'
    reportTitle = "Report-{}.txt".format(datetime.date.today())
    f = open(reportTitle, "r")
    BODY_TEXT = ''
    for lines in f:
        BODY_TEXT += lines
    print(f.readline())


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)


    # Try to send the message.
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")

if __name__ == "__main__":
    mainMethod()