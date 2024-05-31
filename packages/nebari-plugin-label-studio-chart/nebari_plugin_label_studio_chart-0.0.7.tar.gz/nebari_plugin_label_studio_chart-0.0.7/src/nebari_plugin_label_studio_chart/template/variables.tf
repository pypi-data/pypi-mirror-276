variable "name" {
  description = "Chart name"
  type        = string
}

variable "domain" {
  description = "Domain"
  type        = string
}

variable "realm_id" {
  description = "Keycloak realm_id"
  type        = string
}

variable "client_id" {
  description = "OpenID Client ID"
  type        = string
}

variable "base_url" {
  description = "Default URL to use when the auth server needs to redirect or link back to the client"
  type        = string
}

variable "external_url" {
  description = "External url for keycloak auth endpoint"
  type        = string
}

variable "valid_redirect_uris" {
  description = "A list of valid URIs a browser is permitted to redirect to after a successful login or logout"
  type        = list(string)
}

variable "signing_key_ref" {
  description = ""
  type = object({
    name      = string
    kind      = string # nebari uses an old terraform version, can't use optional
    namespace = string
  })
  default = null
}

variable "create_namespace" {
  type = bool
}

variable "namespace" {
  type = string
}

variable "affinity" {
  type = object({
    enabled  = optional(bool, true)
    selector = optional(any, "general")
  })

  default = {
    enabled  = false
    selector = "general"
  }

  validation {
    condition     = can(tostring(var.affinity.selector)) || (can(var.affinity.selector.default) && length(try(var.affinity.selector.default, "")) > 0)
    error_message = "\"affinity.selector\" argument must be a string or object { default, worker, db, auth }"
  }
}

variable "overrides" {
  type    = map(any)
  default = {}
}

variable "auth_enabled" {
  type = bool
}
