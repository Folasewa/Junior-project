# Importing the required library
import smtplib
import flask
import json
from flask import Flask, request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def send_email(sender_email_address, password, smtp_host, smtp_port, email_subject, email_body,
               list_of_receivers_email):
    """
        :param sender_email_address: email address of sender (type string)
        :param password: password of email address of sender (type string)
        :param smtp_host: SMTP host address for email address of sender. e.g for gmail it is 'smtp.gmail.com' (type string)
        :param smtp_port: SMTP port number for email address of sender. e.g for gmail it is 465 (type str)
        :param email_subject: the subject of email (type string)
        :param email_body: the content of email (type string)
        :param list_of_receivers_email: list of email addresses of intended recievers separated by commas (type str)
    """

    # Email Credentials associated with SMTP address
    EMAIL_ACCOUNT = sender_email_address
    PASSWORD = password
    list_of_receivers_email_ = list_of_receivers_email.split(',')
    for email_ in list_of_receivers_email_:
        sent_from = EMAIL_ACCOUNT
        to = [email_]
        subject = email_subject
        body = email_body
        email_text = """\
                                    From: %s\nTo: %s\nSubject: %s\n\n\n%s
                                    """ % (sent_from, ", ".join(to), subject, body)

        # Connecting the email to send email to intended receivers
        server = smtplib.SMTP_SSL(smtp_host, int(smtp_port))
        server.ehlo()
        server.login(EMAIL_ACCOUNT, PASSWORD)
        server.sendmail(sent_from, to, email_text)
        server.close()

        return {"Message": "Message sent to: {}".format(email_)}



@app.route('/send-email', methods=['POST'])
def form_to_json():
    req_ = json.loads(request.data)
    sender_email_address = req_.get("email_sender")
    password = req_["password_sender"]
    smtp_host = req_["smtp_host"]
    smtp_port = req_["smtp_port"]
    email_subject = req_["email_subject"]
    email_body = req_["email_body"]
    list_of_receivers_email =  req_["receiver_emails"]
    return send_email(sender_email_address, password, smtp_host, smtp_port, email_subject, email_body,
               list_of_receivers_email)


if __name__ == "__main__":
    app.run()