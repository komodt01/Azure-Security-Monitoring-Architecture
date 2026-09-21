# Security Control Alignment

## Purpose

This project demonstrates technical concepts that can support enterprise logging, monitoring, detection, and audit requirements.

It does **not** claim compliance with any security framework.

Compliance requires organizational policies, defined control ownership, operating procedures, evidence, testing, governance, and validation beyond the scope of this lab.

The mappings below show how the architecture relates to common security-control objectives.

---

## NIST SP 800-53

### AU-2 – Event Logging

**Control objective:**  
Organizations identify which events should be logged to support security, operational, and audit requirements.

**Project alignment:**  
The architecture establishes a centralized Log Analytics Workspace and explores security-relevant telemetry such as authentication activity.

The current Terraform implementation routes VM metrics to Log Analytics. Complete Linux Syslog collection would require additional guest telemetry configuration such as Azure Monitor Agent and Data Collection Rules.

**Production consideration:**  
An organization would need a defined telemetry baseline specifying required events, systems, retention, ownership, and monitoring expectations.

---

### AU-6 – Audit Record Review, Analysis, and Reporting

**Control objective:**  
Collected audit information should be reviewed and analyzed for indications of inappropriate or unusual activity.

**Project alignment:**  
KQL and Python examples demonstrate analysis of authentication-related Syslog events and aggregation of failed-login activity by host.

A threshold-based Python prototype demonstrates how query results could initiate notification logic.

**Production consideration:**  
Detection logic would require validation, tuning, severity classification, escalation procedures, and ongoing lifecycle management.

---

### AU-12 – Audit Record Generation

**Control objective:**  
Systems should generate audit records for defined security-relevant events.

**Project alignment:**  
The project examines the architecture required to move workload telemetry into a centralized monitoring platform.

The lab does not implement a complete guest operating-system audit collection baseline.

**Production consideration:**  
Required audit sources and event categories should be explicitly defined and validated to ensure expected telemetry is actually being generated and collected.

---

### SI-4 – System Monitoring

**Control objective:**  
Organizations monitor systems to identify attacks, unauthorized activity, and other security-relevant conditions.

**Project alignment:**  
The failed-SSH query demonstrates a basic detection use case in which authentication errors can be analyzed for potentially suspicious patterns.

**Production consideration:**  
Enterprise monitoring would require broader detection coverage, alert routing, telemetry-health monitoring, incident ownership, and integration with operational security processes.

---

## CIS Controls v8

### Control 8 – Audit Log Management

The project supports several concepts associated with audit-log management:

- Centralized monitoring
- Security-event analysis
- Defined retention
- Detection logic
- Programmatic telemetry queries

The Log Analytics Workspace is configured with a 30-day retention period for the lab.

A production retention period should instead be based on organizational, regulatory, investigative, and cost requirements.

---

### Control 13 – Network Monitoring and Defense

The project demonstrates how centralized telemetry and query-based analysis can contribute to monitoring for suspicious activity.

The Linux VM also uses an Azure Network Security Group that restricts inbound SSH to a configured source IP.

This represents a preventive network control working alongside the monitoring and detection concepts demonstrated by the project.

---

## Control Layers

The architecture illustrates several different types of security controls.

### Preventive

- Network Security Group restricts inbound SSH source access.
- Infrastructure as Code provides a repeatable infrastructure definition.

### Detective

- Centralized monitoring through Log Analytics.
- KQL-based security-event analysis.
- Failed-authentication detection concept.
- Threshold evaluation through Python.

### Corrective / Response

The repository demonstrates an email-notification prototype but does not implement automated remediation.

A production architecture could integrate detections with incident management, SOAR, ticketing, or controlled remediation workflows.

---

## Control Dependencies

A monitoring control is only effective when its dependencies remain operational.

For example:

**Workload generates event**

↓

**Telemetry is collected**

↓

**Telemetry reaches Log Analytics**

↓

**Detection query executes**

↓

**Threshold or rule evaluates**

↓

**Alert reaches the responsible team**

↓

**Investigation occurs**

A failure anywhere in this chain can weaken the control even when the monitoring configuration appears to exist.

For that reason, enterprise monitoring should include validation of telemetry health and detection effectiveness rather than relying only on configuration state.

---

## Governance Considerations

Production adoption would require additional governance including:

- Defined logging standards
- Required telemetry sources
- Retention requirements
- Access control and separation of duties
- Detection ownership
- Alert severity definitions
- Escalation procedures
- Exception management
- Periodic control testing
- Evidence retention
- Configuration-change governance

---

## Architecture Takeaway

Security frameworks define control objectives, but architecture determines how those objectives are implemented and validated.

This project demonstrates several technical building blocks that can support logging and monitoring requirements while also identifying the additional operational and governance controls required before those capabilities could be considered part of an enterprise compliance program.
