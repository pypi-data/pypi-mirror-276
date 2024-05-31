terraform {
  required_providers {
    keycloak = {
      source  = "mrparkers/keycloak"
      version = "4.3.1"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.22.0"
    }
    helm = {
      source = "hashicorp/helm"
      version = "2.10.1"
    }
  }
  required_version = ">= 1.0"
}

provider "keycloak" {
  tls_insecure_skip_verify = true
  base_path                = "/auth"
}

provider "kubernetes" {}
provider "helm" {}
