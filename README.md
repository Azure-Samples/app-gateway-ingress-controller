---
page_type: sample
languages:
- python
- yaml
- bash
products:
- azure
- azure-kubernetes-service
- github
name: App Gateway Ingress Controller
description: Using App Gateway Ingress Controller with Azure Kubernetes
urlFragment: app-gateway-ingress-controller
---

# Using Application Gateway Ingress Controller (AGIC) with Azure Kubernetes

## Overview

This repo is a walkthrough to simplify the deployment of a greenfield [App Gateway Ingress Controller](https://docs.microsoft.com/en-us/azure/application-gateway/ingress-controller-install-new) by providing scripts with automated Github Actions workflow. 


Application Gateway Ingress Controller setup helps eliminate the need to have another load balancer/public IP in front of AKS cluster and avoids multiple requests to reach the AKS cluster. Application Gateway talks to pods directly using their private IP and does not require NodePort or KubeProxy services which improves deployment’s performance.

![agic with aks flow](./assets/aks-agic.png)

AGIC currently uses the Standard_v2 and WAF_v2 SKUs, and provide benefits such as; URL routing, Cookie-based affinity, Secure Sockets Layer (SSL) termination, End-to-end SSL, Support for public, private, and hybrid web sites, and Integrated web application firewall. AGIC is configured via the Kubernetes Ingress resource, along with Service and Deployments/Pods.

In this repo you can find a containerized Python "Hello World"sample app (deployed with [Helm](https://helm.sh/)) running in an AKS cluster inside a network infrastructure with vnet, public ip, subnets, app gateway, and managed identity (provisioned with ARM templates), all setup with a Github Actions workflow. The [workflow](.github\workflows\devops-workflow.yml) includes steps to:

- Provision vNet, Public ip, Subnet, App Gateway, Managed Identity, App Insights, and an AKS Cluster
- Install the [AAD Pod Identity & Kubernetes CRDs](https://docs.microsoft.com/en-us/azure/aks/use-azure-ad-pod-identity) using `kubectl`
- Install [Application Gateway Ingress Controller ](https://docs.microsoft.com/en-us/azure/application-gateway/ingress-controller-overview) using Helm
- Deploy a containerized sample Python "Hello message" app to the AKS cluster using Helm. The [deployment yaml is configured](Application\charts\sampleapp\templates\deployment.yaml).



Here is the folder structure:

- `.github\workflows`
  - `devops-workflow.yml` - Github Actions Pipelines yaml file
- `Application`
  - `charts`
    - `sampleapp` - Helm chart for sample app
  - `fastapi-app` - Python sample app
  - `dockerfile` - Dockerfile for the sample app
- `ArmTemplates` - Arm Templates for provisioning vnet, subnet, public ip, aks, acr and application insights


## Getting Started

### Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest): Create and manage Azure resources.
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/): Kubernetes command-line tool which allows you to run commands against Kubernetes clusters.
- [GitHub](https://github.com/) account

### Set up

1. Fork the repo to your github account and git clone.
2. Create a service principal with 'User Access Adminstrator' role for aks to manage and access network resources

    ```bash
    # Create a service principal with User Access Adminstrator role
    az ad sp create-for-rbac --name http://$SERVICEPRINCIPALNAME --role 'User Access Adminstrator' --output json
    ```

3. Use the json output of the last command as a secret named `AZURE_CREDENTIALS` in the repository settings (Settings -> Secrets -> Add New Secret).

    Also add a secret named `SUBSCRIPTIONID` for the subscription id and a secret named `OBJECTID` for the service principle object id. 
    
    The object id can be obtained as below:
    ```bash
    APP_ID=$(az ad sp show --id http://$SERVICEPRINCIPALNAME --query appId --output tsv)
    OBJECT_ID=$(az ad sp show --id $APP_ID --query objectId -o tsv)

    # Output to Service principle object ID
    echo "Service principle Object ID: $OBJECT_ID"
    ```

    ![action-secrets](./assets/action-secrets.png)

    For more details on generating the deployment credentials please see [this guide](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/deploy-github-actions#generate-deployment-credentials).


4. [Github Actions](https://docs.github.com/en/actions) will be used to automate the workflow and deploy all the necessary resources to Azure. Open the [.github\workflows\devops-workflow.yml](.github\workflows\devops-workflow.yml) and change the environment variables accordingly. Update the `RESOURCEGROUPNAME` variable and set the values that you created above.

5. Commit your changes. The commit will trigger the jobs within the workflow and will provision all the resources.

## Validate the Results

1. When the deployment is successful, all the Kubernetes components will be in a running state:
```bash
# Get pods
kubectl get pods
```
![app gateway ingress controller](./assets/appgwyingress.png)


2. Login to [Azure Portal](https://portal.azure.com) to check the application gateway front end and backend health probes.

![Frontend health probes](./assets/healthprobes.png)

![Backend health probes](./assets/backendhealthprobes.png)

3. Get the Public IP Address of the Aplication Gateway and curl the IP Address:

```bash
# #Get the ip address of the app gateway
az network public-ip show -n $APPGWYPUBIPNAME -g $RESOURCEGROUPNAME --query ipAddress -o tsv
```

![app gateway ingress controller](./assets/result.png)

