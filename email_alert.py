import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

class EmailAlert:
    """
    A reusable module for sending alert emails.

    Usage:
    1. Initialize the `EmailAlert` class with email parameters:
       email_alert = EmailAlert(
           alert_email="recipient@example.com",
           smtp_user="your_email@example.com",
           smtp_password="your_password",
           smtp_server="smtp.example.com",  # Optional, default is smtp.example.com
           smtp_port=587  # Optional, default is 587
       )

    2. Use the `send_email_alert` method to send an alert:
       email_alert.send_email_alert(subject="Alert Subject", message="Your alert message here.")

    Example:
    ```
    from email_alert import EmailAlert

    email_alert = EmailAlert(
        alert_email="recipient@example.com",
        smtp_user="your_email@example.com",
        smtp_password="your_password"
    )
    email_alert.send_email_alert("Test Alert", "This is a test message.")
    ```
    """

    def __init__(
        self, 
        alert_email,
        smtp_user,
        smtp_password,
        smtp_server="smtp.example.com",
        smtp_port=587
    ):
        """
        Initialize the EmailAlert class with provided email parameters.

        Args:
            alert_email (str): Recipient's email address.
            smtp_user (str): SMTP username (sender's email address).
            smtp_password (str): SMTP password.
            smtp_server (str): SMTP server address. Default is "smtp.example.com".
            smtp_port (int): SMTP server port. Default is 587.
        """
        self.alert_email = alert_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_email_alert(self, subject, message):
        """
        Send an alert email using the provided configuration.

        Args:
            subject (str): Subject line of the email.
            message (str): Body of the email.

        Raises:
            Exception: If the email fails to send.
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = self.alert_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, self.alert_email, msg.as_string())

            logging.info(f"Alert email sent to {self.alert_email}.")
        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")
            raise
