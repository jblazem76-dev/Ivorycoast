# IvoryCoast Advisory landing page

Static single-page site, served by nginx in a container and deployed to the
Azure Container App `ica-landing` on every push to `main`.

```
site/index.html   the page (HTML + CSS + a small inline script)
site/logo.png     crest used in the nav, hero and footer
nginx.conf        listens on 8080, /healthz endpoint, security headers
Dockerfile        nginx-unprivileged image with the two files above
.github/workflows/deploy.yml   build + smoke test on PRs, deploy on main
```

## Run locally

```bash
docker build -t ica-landing .
docker run --rm -p 8080:8080 ica-landing
# http://localhost:8080
```

## Azure setup (one time)

The deploy job logs in with OIDC (no stored passwords) and pushes the image to
Azure Container Registry. It needs three repository **secrets** and two
repository **variables** (Settings, Secrets and variables, Actions):

| Kind     | Name                       | Value                                              |
| -------- | -------------------------- | -------------------------------------------------- |
| Secret   | `AZURE_CLIENT_ID`          | App registration (client) ID, from the commands below |
| Secret   | `AZURE_TENANT_ID`          | Your Entra tenant ID                               |
| Secret   | `AZURE_SUBSCRIPTION_ID`    | Subscription that holds the Container App          |
| Variable | `AZURE_RESOURCE_GROUP`     | Resource group of the Container App                |
| Variable | `AZURE_ACR_NAME`           | Registry name, without `.azurecr.io`               |
| Variable | `AZURE_CONTAINER_APP_NAME` | Optional. Defaults to `ica-landing`                |

Run this in Azure Cloud Shell (Bash). To find the two placeholder values:

```bash
# Resource group of the Container App, and the image it currently runs
az containerapp list --query "[?name=='ica-landing'].{rg:resourceGroup, image:properties.template.containers[0].image}" -o table
# Registries you can see (the image above starts with <registry-name>.azurecr.io)
az acr list --query "[].{name:name, rg:resourceGroup}" -o table
```

Create the identity and grant it access:

```bash
RG=<resource-group>
ACR=<registry-name>
SUB=$(az account show --query id -o tsv)

APP_ID=$(az ad app create --display-name ica-landing-github --query appId -o tsv)
az ad sp create --id "$APP_ID"

az ad app federated-credential create --id "$APP_ID" --parameters '{
  "name": "github-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:jblazem76-dev/Ivorycoast:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'

az role assignment create --assignee "$APP_ID" --role Contributor \
  --scope "/subscriptions/$SUB/resourceGroups/$RG"
az role assignment create --assignee "$APP_ID" --role AcrPush \
  --scope "$(az acr show -n "$ACR" --query id -o tsv)"

echo "AZURE_CLIENT_ID=$APP_ID"
echo "AZURE_TENANT_ID=$(az account show --query tenantId -o tsv)"
echo "AZURE_SUBSCRIPTION_ID=$SUB"
```

You need permission to create app registrations in Entra ID and to assign roles
on the resource group and registry (Owner or User Access Administrator). If a
command is refused, ask whoever administers the subscription to run it.

The container listens on **8080**. Before each deploy the workflow runs
`az containerapp ingress update --target-port 8080`, so nothing needs to be
changed in the portal. (This needs the Contributor role from the commands above.)

Until those values exist, the `deploy` job fails with a message naming whatever
is missing; the `build` job (image build and smoke test) runs regardless.
