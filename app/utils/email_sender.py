import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
