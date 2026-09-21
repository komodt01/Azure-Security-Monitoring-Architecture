import os
from datetime import timedelta

from azure.identity import AzureCliCredential
from azure.monitor.query import LogsQueryClient


# Log Analytics Workspace ID supplied through an environment variable.
workspace_id = os.getenv("LOG_ANALYTICS_WORKSPACE_ID")

# KQL query for authentication-related Syslog errors.
query = """
Syslog
| where Facility == "authpriv"
| where SeverityLevel == "err"
| summarize FailedSSH=count() by HostName
"""


def main():
    if not workspace_id:
        raise ValueError(
            "LOG_ANALYTICS_WORKSPACE_ID environment variable is not set."
        )

    credential = AzureCliCredential()
    client = LogsQueryClient(credential)

    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(hours=1),
    )

    if response.tables:
        for table in response.tables:
            for row in table.rows:
                print(row)
    else:
        print("No results returned.")


if __name__ == "__main__":
    main()
