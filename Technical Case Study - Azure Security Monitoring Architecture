# Technical Case Study – Azure Security Monitoring Architecture

## Architecture Question

How should an organization design Azure security monitoring so that it can trust not only the detection logic, but also the telemetry pipeline supplying that detection?

This project began as a hands-on Azure monitoring lab using Terraform, Log Analytics, KQL, and Python.

The more important architecture problem became clear during implementation:

> A configured monitoring control does not necessarily mean the organization has working security visibility.

A monitoring architecture must account for telemetry generation, collection, ingestion, access, analysis, alerting, and failure detection across the entire chain.

---

## Environment

The lab provisions an Azure environment containing:

- Resource Group
- Log Analytics Workspace
- Virtual Network and Subnet
- Network Security Group
- Public IP
- Network Interface
- Ubuntu Linux Virtual Machine
- Azure Monitor diagnostic setting

Terraform provides the infrastructure definition.

Python and KQL are used to explore programmatic security-event analysis and threshold-based notification.

---

## Security Objective

The objective was to establish a foundation for centralized monitoring and evaluate how security telemetry could progress from a workload to an actionable detection.

The target security flow is:

**Workload**

↓

**Telemetry Generation**

↓

**Collection**

↓

**Log Analytics**

↓

**Detection Logic**

↓

**Alert**

↓

**Investigation / Response**

Each stage is a dependency.

If one fails, the organization may lose security visibility even when the remaining components appear healthy.

---

## Architecture Decision 1 – Centralize Monitoring Data

### Decision

Use Azure Log Analytics as the centralized monitoring platform for the lab.

### Rationale

Centralization provides a common location for querying telemetry and supports consistent investigation and detection logic.

It also separates monitoring data from the workload producing it.

### Security Benefit

Centralized monitoring can support:

- Cross-resource investigation
- Detection
- Audit evidence
- Operational troubleshooting
- Security analytics

### Tradeoff

Centralization creates a security dependency.

If ingestion, authorization, retention, or workspace availability fails, multiple monitoring capabilities may be affected simultaneously.

The monitoring platform therefore becomes part of the security control plane and requires its own protection and health monitoring.

---

## Architecture Decision 2 – Restrict Administrative Network Access

### Decision

The lab VM uses a public IP, but inbound SSH is restricted by an Azure Network Security Group to a configured source IP.

### Rationale

The lab required direct administrative access while avoiding unrestricted SSH exposure.

### Security Benefit

Source restriction reduces the network locations from which SSH connections can be initiated.

### Residual Risk

The VM still has a public administrative endpoint.

This was accepted for the controlled lab environment but would require additional evaluation for production.

Potential production alternatives include:

- Azure Bastion
- Private connectivity
- Controlled administrative networks
- Privileged access workflows
- Removal of direct Internet administration

The appropriate choice depends on workload sensitivity, operational requirements, and organizational risk tolerance.

---

## Architecture Decision 3 – Separate Platform Metrics from Guest Security Telemetry

This became one of the most important findings from the project.

### Implemented State

Terraform creates an Azure Monitor diagnostic setting associated with the VM and sends:

`AllMetrics`

to the Log Analytics Workspace.

### Detection Requirement

The Python security query searches the `Syslog` table for authentication-related errors.

These are different telemetry paths.

The diagnostic setting alone does not establish Linux guest Syslog collection.

### Architecture Implication

A production implementation requiring Linux Syslog would need a guest telemetry collection architecture such as:

**Linux VM**

↓

**Azure Monitor Agent**

↓

**Data Collection Rule**

↓

**Log Analytics Workspace**

This distinction prevents a dangerous assumption:

**Monitoring configured ≠ required security telemetry available**

The architecture must validate the telemetry required by each detection use case.

---

## Architecture Decision 4 – Externalize Configuration from Code

The original lab scripts contained environment-specific Azure information directly in source code.

During portfolio cleanup, the query scripts were changed to obtain workspace configuration through environment variables.

The Terraform provider configuration was also changed so that a specific Azure subscription identifier was not embedded in the repository.

### Security Principle

Environment-specific configuration and sensitive values should not be unnecessarily embedded in application or infrastructure source code.

### Production Consideration

Environment variables are appropriate for this demonstration but do not automatically represent enterprise secret management.

Production automation should evaluate mechanisms such as:

- Managed identities
- Workload identities
- Azure Key Vault
- CI/CD secret stores
- Controlled configuration management

The objective is to minimize static credentials and reduce unnecessary exposure of environment-specific information.

---

## Detection Design

The detection example queries authentication-related Linux Syslog events:

```kusto
Syslog
| where Facility == "authpriv"
| where SeverityLevel == "err"
| summarize FailedSSH=count() by HostName
```

A Python script executes the query against Log Analytics.

A second prototype compares the result against a threshold and demonstrates an email notification when the threshold is exceeded.

The conceptual flow is:

**Authentication Failure**

↓

**Syslog Event**

↓

**Log Analytics**

↓

**KQL Aggregation**

↓

**Threshold Evaluation**

↓

**Notification**

---

## Detection Tradeoff – Threshold Selection

The prototype uses a threshold of five failed authentication events.

The number itself should not be interpreted as an enterprise detection standard.

Threshold selection requires context.

A threshold that is too low may create excessive alerts.

A threshold that is too high may delay detection.

Production tuning should consider:

- Normal authentication patterns
- Workload criticality
- Administrative behavior
- Time window
- Source address
- User or account context
- Historical activity
- False-positive tolerance
- Incident severity

The architecture therefore separates the technical ability to create a threshold from the governance decision that determines what the threshold should be.

---

## Identity Failure Discovered During Testing

Programmatic Log Analytics querying exposed another architecture consideration: authentication context.

Testing showed that Azure CLI context and SDK authentication behavior did not always produce the expected results across tenant and subscription contexts.

Errors such as:

- `PathNotFoundError`
- `WorkspaceNotFoundError`

could appear to indicate a missing workspace even when the resource existed.

The troubleshooting process required separating several possibilities:

**Resource availability**

vs.

**Telemetry availability**

vs.

**Identity context**

vs.

**Authorization**

vs.

**Query execution**

This reinforced the importance of treating identity as part of the monitoring architecture rather than as an implementation detail.

---

## Failure Analysis

A production security monitoring architecture should explicitly account for failure states.

### Failure: Workload Stops Generating Expected Telemetry

**Impact:**  
Security activity may become invisible.

**Required control:**  
Expected telemetry baselines and health validation.

---

### Failure: Collection Mechanism Fails

Examples include agent failure or Data Collection Rule misconfiguration.

**Impact:**  
The workload may continue operating while monitoring silently degrades.

**Required control:**  
Collection health monitoring and missing-telemetry detection.

---

### Failure: Log Analytics Ingestion Fails

**Impact:**  
Detections depending on centralized telemetry may stop functioning.

**Required control:**  
Ingestion monitoring and operational alerting.

---

### Failure: Automation Identity Loses Access

**Impact:**  
Programmatic queries may fail even though telemetry remains available.

**Required control:**  
Identity monitoring, least-privilege RBAC, and authentication failure alerting.

---

### Failure: Detection Logic Is Incorrect

**Impact:**  
Telemetry exists but suspicious activity may not be identified correctly.

**Required control:**  
Detection testing, peer review, version control, and lifecycle management.

---

### Failure: Notification Fails

**Impact:**  
A detection can occur without reaching the responsible team.

**Required control:**  
Alert-delivery monitoring and escalation paths.

---

## Monitoring the Monitoring Pipeline

One of the primary architecture conclusions from the project is that security monitoring itself requires monitoring.

A useful health model would evaluate:

**Telemetry Expected?**

↓

**Telemetry Arriving?**

↓

**Detection Executing?**

↓

**Alert Delivered?**

↓

**Response Owned?**

This provides stronger assurance than checking only whether a diagnostic setting, agent, or query exists.

---

## Preventive, Detective, and Response Controls

### Preventive

- Source-restricted SSH through the NSG
- Infrastructure defined through Terraform
- Externalized environment configuration

### Detective

- Centralized monitoring
- KQL security-event analysis
- Failed-authentication detection concept
- Threshold evaluation

### Response

- Email-notification prototype

A production implementation would normally integrate response with centralized alert management, SIEM, SOAR, incident management, or other operational security workflows.

---

## Exception and Risk Governance

Monitoring requirements cannot always be implemented immediately across every workload.

A mature architecture should provide a governed exception path.

An exception should identify:

- Requirement that cannot currently be met
- Business or technical justification
- Risk owner
- Compensating controls
- Security review
- Approval
- Expiration or review date

The absence of telemetry should never become an undocumented permanent condition.

---

## Production Architecture

The lab could evolve toward:

**Azure Workload**

↓

**Azure Monitor Agent**

↓

**Data Collection Rule**

↓

**Log Analytics Workspace**

↓

**KQL / Azure Monitor / Microsoft Sentinel**

↓

**Detection / Incident**

↓

**Security Operations**

↓

**Investigation and Response**

Supporting controls would include:

- Least-privilege RBAC
- Managed identity where appropriate
- Secure administrative access
- Monitoring-pipeline health checks
- Defined telemetry standards
- Detection lifecycle management
- Retention requirements
- Cost governance
- Exception management
- Incident ownership
- Audit evidence

---

## Architecture Review Board Considerations

Before approving a production version of this architecture, an Architecture Review Board should be able to answer:

1. Which security events are required from each workload?
2. How is successful telemetry collection validated?
3. Who can change monitoring configuration?
4. How is monitoring configuration protected?
5. How are telemetry gaps detected?
6. How are detection rules tested and approved?
7. Who owns each detection?
8. How are alerts escalated?
9. What retention period is required?
10. How are monitoring costs governed?
11. What happens when a workload cannot meet the monitoring baseline?
12. Who accepts the residual risk?

These questions shift the discussion from whether logging is enabled to whether the organization can depend on the monitoring capability as a security control.

---

## Outcome

The lab demonstrated the mechanics of Azure infrastructure deployment, centralized monitoring, KQL analysis, Python-based querying, and threshold-based notification.

More importantly, it exposed the architectural dependencies behind those capabilities.

The key outcome was recognizing that reliable security monitoring requires assurance across the complete chain:

**Generation → Collection → Ingestion → Analysis → Detection → Alert → Response**

A security architecture should be able to demonstrate that each link is functioning, identify when it is not, and assign ownership for the resulting risk.
