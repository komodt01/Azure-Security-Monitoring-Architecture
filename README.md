# Azure Security Monitoring Architecture

## Overview

This project explores the architecture of a security monitoring capability in Microsoft Azure using centralized telemetry, Infrastructure as Code, KQL-based analysis, and Python automation.

The implemented lab provisions Azure infrastructure and a Log Analytics workspace, creates a monitored Linux workload, routes Azure VM metrics to Log Analytics, and demonstrates programmatic security-event querying and threshold-based alerting concepts.

The broader security objective is not simply to collect logs. It is to establish reliable security visibility and create a path from:

**Workload → Telemetry → Centralized Analysis → Detection → Alert → Investigation**

This repository combines a working lab foundation with security architecture analysis of what would be required to mature the design for enterprise use.

---

## Security Problem

Cloud workloads generate security-relevant activity, but that activity provides little value if organizations cannot reliably collect, centralize, query, and act on it.

Monitoring architectures must answer several security questions:

- What telemetry is required?
- How does telemetry reach the monitoring platform?
- Who can access or modify monitoring configuration?
- How do we know collection is still working?
- What activity should trigger investigation?
- How are false positives and alert thresholds managed?
- What happens when telemetry stops arriving?
- How are monitoring exceptions governed?
- How long should security telemetry be retained?
- Who owns the response when a detection fires?

This project uses a small Azure environment to explore those questions.

---

## Implemented Lab

The Terraform configuration provisions:

- Azure Resource Group
- Log Analytics Workspace
- Virtual Network
- Subnet
- Network Security Group
- Static Public IP
- Network Interface
- Ubuntu Linux Virtual Machine
- Azure Monitor diagnostic setting for VM metrics

The NSG limits inbound SSH access to a configurable source IP.

The repository also includes Python scripts that demonstrate querying Log Analytics and evaluating query results for potential alerting.

---

## Architecture Flow

The implemented components support the following monitoring concept:

**Azure VM → Azure Monitoring / Diagnostic Data → Log Analytics Workspace → KQL Query → Python Analysis → Alerting Concept**

The Python scripts query for security-relevant events and demonstrate how monitoring data can be evaluated outside the Azure portal.

A production architecture would require additional controls around telemetry collection, ingestion health, identity, alert management, response ownership, and governance.

---

## Security Detection Example

The Python query demonstrates a simple security use case involving failed SSH authentication activity.

The KQL logic searches the `Syslog` table for authentication-related errors and summarizes matching activity by host.

Conceptually:

**Authentication Event → Syslog → Log Analytics → KQL Detection → Threshold Evaluation → Alert**

The email-alert script extends this concept by evaluating the number of matching events against a threshold.

This is a detection prototype rather than a production Security Operations workflow.

A production implementation would need to address areas such as:

- Detection tuning
- False-positive management
- Alert severity
- Suppression and deduplication
- Escalation paths
- Incident ownership
- Ticketing or SIEM integration
- Detection testing
- Evidence retention

---

## Infrastructure Security Controls

### Network Access

The Linux VM is placed within a dedicated virtual network and subnet.

Inbound SSH access is restricted by the Network Security Group to the source address supplied through Terraform.

This reduces exposure compared with allowing unrestricted SSH access from the Internet.

For production environments, stronger administrative access patterns should be evaluated, including private connectivity, Azure Bastion, privileged access workflows, or other controlled administrative paths.

### Centralized Monitoring

A Log Analytics Workspace provides a centralized location for monitoring data.

Centralization supports:

- Investigation
- Detection
- Operational troubleshooting
- Audit evidence
- Security analytics

Centralization also creates a high-value security dependency. Access to the workspace, retention settings, ingestion configuration, and monitoring rules must therefore be governed.

### Infrastructure as Code

Terraform provides a repeatable definition of the Azure infrastructure used by the lab.

Infrastructure as Code can improve consistency and reviewability, but production use would also require controls around:

- Terraform state protection
- Secret handling
- Code review
- Change approval
- CI/CD security
- Policy validation
- Deployment identity
- Configuration drift

---

## Telemetry Collection Boundary

The current Terraform configuration creates an Azure Monitor diagnostic setting for VM metrics.

It does **not** currently deploy the complete Azure Monitor Agent and Data Collection Rule architecture required for managed Linux guest Syslog collection.

Therefore, the repository should not be interpreted as a complete production telemetry-ingestion implementation.

A production design would typically extend the architecture with:

**Linux VM → Azure Monitor Agent → Data Collection Rule → Log Analytics Workspace**

The Data Collection Rule would define which guest telemetry should be collected and where it should be sent.

This distinction is important because configuring a monitoring destination is not the same as proving that all required security telemetry is being collected successfully.

---

## Monitoring the Monitoring System

A security monitoring architecture must detect failures in its own telemetry pipeline.

A resource can appear operational while security visibility has degraded.

Examples include:

- Monitoring agent failure
- Data Collection Rule misconfiguration
- Workspace ingestion failure
- Authentication or authorization failure
- Query failure
- Unexpected telemetry gaps
- Retention configuration changes
- Detection logic changes
- Alert delivery failure

A mature architecture therefore needs both:

**Security monitoring**

and

**Monitoring of the security-monitoring pipeline**

This is a critical control distinction.

---

## Identity and Access Considerations

Monitoring infrastructure contains sensitive operational and security information.

Production access should follow least privilege and separation of duties.

Typical responsibilities may include:

**Cloud / Platform Team**
- Maintains workload and monitoring infrastructure

**Security Operations**
- Investigates detections and security telemetry

**Security Architecture**
- Defines monitoring requirements and control expectations

**Application / Resource Owners**
- Provide workload context and support remediation

Access to Log Analytics, monitoring configuration, detection rules, and alert workflows should be limited to identities that require those capabilities.

---

## Failure and Response States

A production monitoring capability should distinguish between different operational states rather than treating monitoring as simply enabled or disabled.

Examples include:

**Healthy**
Required telemetry is arriving and expected detections are operational.

**Telemetry Gap**
Expected security data is no longer arriving.

**Detection Failure**
Telemetry exists, but a query or detection mechanism fails.

**Alert Delivery Failure**
Detection occurs, but notification or downstream workflow fails.

**Exception**
A monitoring requirement cannot currently be satisfied and has been formally reviewed.

Each state requires different ownership and response.

---

## Exception Governance

Not every workload can always meet a standard monitoring baseline immediately.

A production architecture should provide a controlled exception process including:

- Business or technical justification
- Identified owner
- Risk assessment
- Compensating controls where appropriate
- Approval
- Expiration or review date
- Audit evidence

An exception should represent an explicit risk decision rather than an undocumented monitoring gap.

---

## Architecture Tradeoffs

### Telemetry Coverage vs Cost

Collecting more telemetry improves investigative depth but increases ingestion, retention, and operational costs.

The objective should be security-relevant telemetry rather than indiscriminate collection.

### Detection Sensitivity vs Alert Noise

Lower thresholds may detect suspicious activity earlier but can increase false positives.

Higher thresholds reduce alert volume but may delay detection.

Thresholds should therefore reflect workload context and risk.

### Public Administration vs Private Access

A public IP with source-restricted SSH is appropriate for a controlled lab.

Production environments may justify stronger administrative isolation depending on workload sensitivity and organizational requirements.

### Custom Automation vs Native Security Platforms

Python automation provides flexibility and demonstrates how security telemetry can drive programmatic actions.

Enterprise environments may instead integrate detection and response with Azure Monitor alerts, Microsoft Sentinel, SOAR platforms, ticketing systems, or other centralized operational workflows.

---

## Implemented Lab vs Production Architecture

### Implemented in This Repository

- Azure infrastructure deployed with Terraform
- Log Analytics Workspace
- Linux VM
- VNet and subnet
- Network Security Group
- Source-restricted SSH rule
- Public IP and network interface
- VM metric diagnostic setting
- KQL-based security query concept
- Python Log Analytics query
- Python threshold-based email-alert prototype

### Production Architecture Would Require Additional Controls

- Azure Monitor Agent deployment
- Data Collection Rules and associations
- Defined security telemetry baseline
- Telemetry-ingestion health monitoring
- Production identity and RBAC model
- Secure administrative access
- Native alerting or SIEM integration
- Detection lifecycle management
- Incident escalation and ownership
- Exception governance
- Retention requirements
- Cost governance
- Monitoring configuration protection
- Evidence and audit requirements

---

## Repository Components

### `main.tf`

Defines the Azure infrastructure used by the lab.

### `outputs.tf`

Provides Terraform outputs associated with the deployed environment.

### `query_logs.py`

Demonstrates programmatic Log Analytics querying using the Azure Monitor Query SDK.

### `query_logs_email_alert.py`

Extends the query concept with threshold evaluation and an example email-notification workflow.

The email configuration contains placeholders and represents a prototype rather than production credential or notification management.

### `technologies.md`

Documents the Azure services and technologies associated with the project.

### `compliance_mapping.md`

Describes how centralized logging and monitoring concepts relate to broader security-control objectives.

### `lessonslearned.md`

Captures implementation observations and Azure authentication/query troubleshooting lessons.

### `teardown.md`

Documents lab cleanup considerations.

---

## Production Architecture Direction

A mature version of this architecture could evolve toward:

**Azure Workloads**

↓

**Azure Monitor Agent + Data Collection Rules**

↓

**Log Analytics Workspace**

↓

**KQL Detection / Azure Monitor / Microsoft Sentinel**

↓

**Alert or Incident**

↓

**Security Operations Investigation**

↓

**Response / Remediation**

↓

**Evidence and Continuous Improvement**

The key architectural requirement is maintaining confidence that the telemetry and detection pipeline itself remains healthy.

---

## Key Security Architecture Takeaway

Security monitoring is not achieved simply by enabling logging.

The architecture must provide confidence that the right telemetry is collected, protected, delivered, analyzed, and acted upon — and that failures anywhere in that chain are detectable.

This project provides a lab implementation for exploring that monitoring lifecycle while identifying the additional controls required for enterprise deployment.
