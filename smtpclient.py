import smtplib
import ssl
import logging
from datetime import datetime

# ---------- Logging Setup ----------
logging.basicConfig(
    filename="smtp_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------- SMTP Settings ----------
smtp_server = "smtp.gmail.com"   # For Gmail
port = 587                       # TLS port
sender_email = "mohit2301mc47@gmail.com"    # Replace with your email
password = "vzir rbeh qvsq ucnk"           # Use App Password (not normal password)
receiver_email = "krishsinha0918@gmail.com"

# ---------- Email Content ----------
subject = "Test Email from Python SMTP Client"
body = "Hello!\n\nThis is a test email sent using Python and SMTP.\n\nRegards,\nSMTP Client"
message = f"Subject: {subject}\n\n{body}"

# ---------- Sending Process ----------
try:
    logging.info("Starting SMTP connection...")
    context = ssl.create_default_context()

    # Connect to server
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    logging.info("Connected to server and sent EHLO.")

    # Start TLS
    server.starttls(context=context)
    logging.info("Started TLS encryption.")

    # Login
    server.login(sender_email, password)
    logging.info(f"Logged in as {sender_email}")

    # Send email
    server.sendmail(sender_email, receiver_email, message)
    logging.info(f"Email sent successfully to {receiver_email}")

    # Quit connection
    server.quit()
    logging.info("SMTP session terminated successfully.")

except Exception as e:
    logging.error("Error occurred: " + str(e))
    print("An error occurred. Check smtp_log.txt for details.")
else:
    print("Email sent successfully! Check smtp_log.txt for logs.")


