variable "location" {
  description = "Azure region used for the lab resources."
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Name of the Azure resource group."
  type        = string
}

variable "workspace_name" {
  description = "Name of the Log Analytics Workspace."
  type        = string
}

variable "vm_admin_username" {
  description = "Administrative username for the Linux VM."
  type        = string
}

variable "vm_admin_password" {
  description = "Administrative password used by the lab VM."
  type        = string
  sensitive   = true
}

variable "ssh_allowed_ip" {
  description = "Source IP address permitted to connect to the lab VM over SSH."
  type        = string
}
