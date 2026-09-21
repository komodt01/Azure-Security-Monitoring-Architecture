# Teardown Guide

This lab creates Azure resources that may continue to incur charges until they are removed.

## Destroy the Lab Infrastructure

Run Terraform from the `/terraform` directory:

```bash
cd terraform
terraform destroy
```

If a variable file was used during deployment:

```bash
terraform destroy -var-file="terraform.tfvars"
```

Review the Terraform destroy plan before confirming the operation.

---

## Validate Resource Removal

After Terraform completes, verify that the lab resources have been removed.

Expected resources include:

- Resource Group
- Linux Virtual Machine
- Network Interface
- Public IP
- Network Security Group
- Virtual Network and Subnet
- Log Analytics Workspace
- Diagnostic Setting

The Azure portal or Azure CLI can be used as an independent validation path.

---

## Terraform State

Terraform state should not be deleted automatically as part of normal teardown.

State records the relationship between Terraform configuration and deployed infrastructure and may be needed for troubleshooting or validation.

For an enterprise implementation, Terraform state should be stored in a secured remote backend with appropriate access control, encryption, locking, and lifecycle management.

---

## Security and Cost Consideration

Teardown is part of the security lifecycle.

Unused lab resources can create:

- Unnecessary cloud cost
- Forgotten public exposure
- Stale administrative access
- Unmonitored resources
- Configuration drift

Successful teardown should therefore include both infrastructure destruction and verification that expected cloud resources no longer remain.
