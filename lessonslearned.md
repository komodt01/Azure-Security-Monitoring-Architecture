# Lessons Learned

## Telemetry Configuration Is Not the Same as Telemetry Assurance

One of the most important lessons from this project was that configuring a monitoring destination does not prove that all expected security telemetry is reaching it.

The Terraform diagnostic setting routes supported VM metrics to Log Analytics, but guest operating-system telemetry such as Linux Syslog requires its own collection path.

For a production architecture, telemetry requirements should therefore be defined explicitly and validated independently.

---

## Identity Context Matters During Monitoring Automation

While testing programmatic Log Analytics queries, Azure authentication context became an important troubleshooting factor.

The Azure Monitor Python SDK can authenticate through mechanisms such as `DefaultAzureCredential`, while Azure CLI commands operate using the CLI's current account and tenant context.

These contexts do not always behave as expected in environments involving multiple tenants, subscriptions, or identities.

A successful:

```bash
az account show
```

does not by itself prove that an SDK-based query is using the identity, tenant, subscription, or authorization path expected by the application.

---

## Query Failures Are Not Always Data Failures

During testing, programmatic workspace queries produced errors such as:

- `PathNotFoundError`
- `WorkspaceNotFoundError`

These errors can initially appear to indicate that the Log Analytics Workspace does not exist.

Troubleshooting showed the importance of checking identity and tenant context before assuming the underlying monitoring resource is unavailable.

This distinction matters operationally because:

**Resource failure**

and

**Authorization / identity-context failure**

require different responses.

---

## Use Multiple Validation Paths

KQL queries executed through the Log Analytics interface provided an important comparison point when programmatic queries failed.

This reinforced a useful troubleshooting approach:

1. Confirm the Azure resource exists.
2. Confirm expected telemetry is present.
3. Validate the query directly.
4. Validate the identity being used by automation.
5. Validate authorization.
6. Test the programmatic query path.
7. Test downstream alerting separately.

Separating these stages makes it easier to determine where a monitoring pipeline is actually failing.

---

## Monitoring Pipelines Have Multiple Failure Domains

A security detection depends on more than the detection query itself.

The complete chain may include:

**Workload → Telemetry Generation → Collection → Ingestion → Storage → Query → Detection → Alert → Investigation**

Each stage introduces a potential failure point.

A production monitoring architecture should therefore include health checks and validation for the monitoring pipeline itself rather than assuming that an enabled configuration means the security control is functioning.

---

## Detection Thresholds Are Risk Decisions

The email-alert prototype uses a threshold for failed authentication activity.

The technical implementation of a threshold is straightforward. Choosing the correct threshold is not.

A production threshold would need to consider:

- Normal authentication behavior
- Workload sensitivity
- Expected administrative activity
- False-positive tolerance
- Detection urgency
- Escalation requirements

This makes detection tuning a security and operational decision rather than simply a coding decision.

---

## Lab Controls and Production Controls Are Different

The lab uses a public IP with SSH restricted to a configured source IP.

That provides a reasonable constraint for a controlled learning environment, but it should not automatically become the production architecture.

Production environments may require stronger administrative patterns such as private connectivity, Azure Bastion, privileged access controls, stronger authentication, or removal of direct Internet administration entirely.

The security architecture decision should be based on workload risk and operational requirements.

---

## Key Architecture Lesson

The central lesson from this project is that **security visibility is a dependency chain**.

Centralized logging is useful only when the organization can demonstrate that required telemetry is generated, collected, delivered, queryable, monitored for failure, and connected to an owned response process.

That distinction changes monitoring from a configuration task into an architecture and governance problem.
