# SURROUND Prez Theme
This repo is used for deploying Prez instances.

## Configuration
`config.yaml` contains all necessary options for configuring, theming & deploying an instance of Prez.

## Theming
The `theme/` folder contains the HTML, CSS, JavaScript & image files to be mounted as a volume in a container deployment.

Jinja2 HTML templates go under `templates/`, (which can include `fonts.html`, which can contain `<link>` elements for fonts).

## Deployment
Prez is designed to be deployed in a containerised environment. `pipeline_script.py` will perform token replacement from values in `config.yaml` to the deployment file chosen in the `deploymentMethod` field in `config.yaml`. Currently, three deployment types are supported: Docker (docker-compose), Kubernetes & ECS.

Note: Only the Kubernetes option is fully implemented.

### Docker Container
Use `docker-compose.yml`, otherwise a simple shell script `docker-run.sh` is provided to run a docker container locally.

### Kubernetes

- Volume
    - Persistent volume claim
- ConfigMap contains env vars for container
- Ingress

For AWS, a StorageClass with an EBS provisioner is recommended, provided in `deploy/kube/kube-ebs-storage-class.yaml`.

### ECS
Not yet implemented.

## Pipelines
This repo contains pipeline definitions for GitHub actions, BitBucket Pipelines & Azure Pipelines.

The SPARQL credentials (`SPARQL_ENDPOINT` (required), `SPARQL_USERNAME` & `SPARQL_PASSWORD`) should be set as repository secrets.

All pipeline methods follow the same steps:

- Run `pipeline_script.py` for token replacement
- Depending on `deploymentMethod` value, deploy as necessary

### GitHub Actions

Currently, only the Kubernetes deployment option is supported, where EKS is used.

The required repository secrets are:

- `KUBE_CONFIG`
    - Obtained by locally running:
        ```bash
        cat $HOME/.kube/config | base64 
        ```
        - Note that any AWS_PROFILEs in this config should be removed beforehand
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Along with the required secrets for Prez itself (`SPARQL_ENDPOINT` (required), `SPARQL_USERNAME` & `SPARQL_PASSWORD`).

### BitBucket Pipelines
Not yet implemented.

### Azure Pipelines
Not yet implemented.
