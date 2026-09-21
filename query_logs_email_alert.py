import os
import smtplib
from datetime import timedelta
from email.message import EmailMessage

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient


workspace_id = os.getenv("LOG_ANALYTICS_WORKSPACE_ID")

THRESHOLD = 5

EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM")
EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


query = """
Syslog
| where Facility == "authpriv"
| where SeverityLevel == "err"
| summarize FailedSSH=count() by HostName
"""


def send_email_alert(host, count):
    msg = EmailMessage()
    msg["Subject"] = f"SSH Login Anomaly on {host}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(
        f"Detected {count} failed SSH logins on {host} within the past hour."
    )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

    print(f"Alert sent for {host}")


def main():
    required_settings = {
        "LOG_ANALYTICS_WORKSPACE_ID": workspace_id,
        "ALERT_EMAIL_FROM": EMAIL_FROM,
        "ALERT_EMAIL_TO": EMAIL_TO,
        "SMTP_SERVER": SMTP_SERVER,
        "SMTP_USERNAME": SMTP_USERNAME,
        "SMTP_PASSWORD": SMTP_PASSWORD,
    }

    missing = [
        name for name, value in required_settings.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(hours=1),
    )

    if response.tables:
        for row in response.tables[0].rows:
            host, count = row[0], row[1]
            print(f"{host}: {count} failed logins")

            if count >= THRESHOLD:
                send_email_alert(host, count)
    else:
        print("No results returned.")


if __name__ == "__main__":
    main()
