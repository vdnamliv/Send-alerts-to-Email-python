import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import logging

class EmailAlert:
    """
    A reusable module for sending alert emails.

    Usage:
    1. Create an `email_config.ini` file with the following structure:
       [email]
       alert_email = recipient@example.com
       smtp_server = smtp.example.com
       smtp_port = 587
       smtp_user = your_email@example.com
       smtp_password = your_password

    2. Initialize the `EmailAlert` class with the path to the config file:
       email_alert = EmailAlert(config_path="email_config.ini")

    3. Use the `send_email_alert` method to send an alert:
       email_alert.send_email_alert(subject="Alert Subject", message="Your alert message here.")

    Example:
    ```
    from email_alert import EmailAlert

    email_alert = EmailAlert(config_path="email_config.ini")
    email_alert.send_email_alert("Test Alert", "This is a test message.")
    ```
    """

    def __init__(self, config_path="email_config.ini"):
        """
        Initialize the EmailAlert class with configuration from the provided file.
        
        Args:
            config_path (str): Path to the email configuration file. Default is "email_config.ini".
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        try:
            self.alert_email = self.config.get("email", "alert_email")
            self.smtp_server = self.config.get("email", "smtp_server")
            self.smtp_port = int(self.config.get("email", "smtp_port"))
            self.smtp_user = self.config.get("email", "smtp_user")
            self.smtp_password = self.config.get("email", "smtp_password")
        except configparser.Error as e:
            logging.error("Failed to load email configuration: %s", e)
            raise

    def send_email_alert(self, subject, message):
        """
        Send an alert email using the configuration.

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
