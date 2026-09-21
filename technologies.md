# Technologies Used

This project combines Azure infrastructure, centralized monitoring, KQL, Terraform, and Python to explore a security monitoring architecture.

The technologies below distinguish between components implemented in the lab and capabilities that would be required to extend the design into a production monitoring architecture.

---

## Azure Log Analytics Workspace

**What it is:**  
A centralized Azure Monitor data platform used to store and query monitoring data.

**Why it is used:**  
The workspace provides a central location for telemetry analysis and supports Kusto Query Language (KQL) for investigation and detection use cases.

**How it is used here:**  
Terraform provisions the Log Analytics Workspace. The VM diagnostic setting is configured to send supported VM metrics to the workspace.

The Python examples also demonstrate querying a Log Analytics workspace programmatically.

---

## Azure Linux Virtual Machine

**What it is:**  
An Ubuntu 22.04 virtual machine representing a monitored workload.

**Why it is used:**  
The VM provides a workload around which network controls, telemetry collection, security queries, and monitoring architecture can be explored.

**How it is used here:**  
Terraform provisions the VM along with its supporting network resources.

The VM is assigned a public IP for the lab, while an Azure Network Security Group restricts inbound SSH access to a configured source IP.

A production environment should evaluate stronger administrative access patterns such as private connectivity, Azure Bastion, or other privileged-access controls.

---

## Azure Virtual Network and Network Security Group

**What they are:**  
Azure networking services used to provide network segmentation and traffic filtering.

**Why they are used:**  
Administrative access to monitored workloads should not be unnecessarily exposed.

**How they are used here:**  
Terraform creates a virtual network, subnet, network interface, public IP, and Network Security Group.

The NSG permits inbound SSH only from the source IP supplied through Terraform.

---

## Azure Monitor Diagnostic Settings

**What it is:**  
An Azure capability for routing supported resource logs and metrics to destinations such as Log Analytics.

**Why it is used:**  
Centralized telemetry is required before monitoring data can be analyzed consistently.

**How it is used here:**  
Terraform creates a diagnostic setting associated with the Linux VM and routes `AllMetrics` to the Log Analytics Workspace.

This should not be confused with guest operating-system Syslog collection.

---

## Kusto Query Language (KQL)

**What it is:**  
The query language used by Azure Monitor and Log Analytics for analyzing telemetry.

**Why it is used:**  
Security teams need a way to search, filter, aggregate, and analyze monitoring data.

**How it is used here:**  
The Python examples contain KQL designed to identify authentication-related Syslog errors and summarize matching events by host.

The query demonstrates detection logic, but successful execution depends on the required Syslog data already being ingested into the workspace.

---

## Azure Monitor Query SDK for Python

**What it is:**  
A Python SDK that enables applications and automation to query Azure Monitor Logs.

**Why it is used:**  
Programmatic access allows monitoring data to support automated detection, analysis, notification, and integration workflows.

**How it is used here:**  
The Python scripts use `LogsQueryClient` to execute KQL against a Log Analytics Workspace.

One script demonstrates querying security-relevant telemetry. A second extends the concept by comparing query results against a threshold and demonstrating an email-notification workflow.

These scripts are prototypes rather than a production alert-management system.

---

## Microsoft Entra ID Authentication

**What it is:**  
Microsoft's cloud identity platform used to authenticate identities accessing Azure services.

**Why it is relevant:**  
Programmatic monitoring access should use authenticated identities rather than embedded Azure credentials.

**How it is used here:**  
The Python examples use Azure Identity credential mechanisms such as `AzureCliCredential` and `DefaultAzureCredential`.

The current Terraform configuration does not create a Log Analytics RBAC assignment.

A production architecture would require an explicit least-privilege authorization model for administrators, automation identities, monitoring services, and security operations personnel.

---

## Terraform

**What it is:**  
Infrastructure as Code used to define and provision cloud resources.

**Why it is used:**  
Terraform makes the lab infrastructure repeatable and provides a reviewable definition of the deployed architecture.

**How it is used here:**  
The `/terraform` directory defines:

- Resource Group
- Log Analytics Workspace
- Virtual Network
- Subnet
- Network Security Group
- Public IP
- Network Interface
- Ubuntu VM
- VM diagnostic setting

Production use would additionally require controls around Terraform state, deployment identity, secrets, change approval, code review, and policy validation.

---

## Azure Monitor Agent and Data Collection Rules

Azure Monitor Agent (AMA) and Data Collection Rules (DCRs) are **not deployed by the current Terraform configuration**.

They are important to the production architecture because guest operating-system telemetry such as Linux Syslog requires an appropriate collection path.

A more complete monitoring design would extend the lab with:

**Linux VM → Azure Monitor Agent → Data Collection Rule → Log Analytics Workspace**

The DCR would define the guest telemetry to collect and its destination.

This distinction is intentional: the repository separates what was implemented in the lab from the additional controls required for a production security-monitoring architecture.

---

## Architecture Perspective

The individual technologies are less important than the security control chain they support:

**Workload → Telemetry Collection → Centralized Monitoring → Detection → Alert → Investigation → Response**

A failure at any point in that chain can reduce security visibility.

For that reason, an enterprise implementation must monitor not only workloads but also the health and integrity of the monitoring pipeline itself.
