import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def validate_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None


class EmailSender:
    def send_email(
        self,
        sender_email,
        sender_password,
        recipient_emails,
        subject,
        body,
        smtp_server="smtp.gmail.com",
        smtp_port=587,
    ):
        """
        Send an email using SMTP.

        """

        invalid_emails = [
            email for email in recipient_emails if not validate_email(email)
        ]
        if invalid_emails:
            raise ValueError(
                f"Invalid email addresses: {', '.join(invalid_emails)}"
            )

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ", ".join(recipient_emails)
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

        except Exception as e:
            print(f"An error occurred: {e}")
