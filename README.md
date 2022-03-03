# SURROUND Prez Theme
This repo is used for customising & deploying Prez instances.

## Installing
Install using Poetry (optional), which you can install [here](https://python-poetry.org/docs/#installation) (recommended), or by running:

```bash
pip install poetry 
```

Then run `poetry install` in the root directory.

Otherwise install using `pip` as normal:

```bash
pip install -r requirements.txt 
```

## Configuration
`config.yaml` contains all necessary options for configuring, theming & deploying an instance of Prez.

Below is a minimal example of the config file for a VocPrez instance:

```yaml
themeVolume: theme
sidenav: true
enabledPrezs:
  - VocPrez
sparqlCreds:
  VocPrez:
    SPARQL_ENDPOINT: #{VOCPREZ_SPARQL_ENDPOINT}#
    SPARQL_USERNAME: #{VOCPREZ_SPARQL_USERNAME}#
    SPARQL_PASSWORD: #{VOCPREZ_SPARQL_PASSWORD}#
port: 8000
demo: true
debug: true
allowPartialResults: true
searchEndpoints:
  - name: GA VocPrez
    url: http://ga.surroundaustralia.com/sparql/
systemUri: http://prez.surroundaustralia.com
systemInfo:
  Prez:
    title: SURROUND Prez
    desc: Prez demo instance for SURROUND Australia
  VocPrez:
    title: SURROUND Vocabularies
    desc: Demo vocabularies
    data_uri: http://exampledata.org
appName: surround
deploymentMethod: kubernetes
storageClass: ebs-sc
version: 0.2.0
```
### Config Options
Key|Description
-|-
`themeVolume`|The name of the local theme folder to be mounted as a volume
`sidenav`|Enables a sidebar when true
`enabledPrezs`|A list of *Prezs to enable. List up to one of each: "VocPrez", "SpacePrez", "CatPrez" (not available yet), "TimePrez" (not available yet)
`sparqlCreds`|The credentials for the SPARQL endpoint for each *Prez type. To use the built-in GitHub actions for deployment, store these credentials (e.g. `VOCPREZ_SPARQL_ENDPOINT`) as repository secrets, following the provided naming convention. The `{*Prez}_SPARQL_ENDPOINT` variable for a *Prez type must be included at the very least if that *Prez is listed in `enabledPrezs`
`port`|The local port to run Prez.
`demo`|Flags the instance as a "demo" in the UI when true (not yet implemented)
`debug`|Enables enhanced error messages when true
`allowPartialResults`|When true, prevents erroring when not all triplestores return successful responses when queries across multiple *Prez triplestores. Essentially allows for some results to appear if some but not all requests succeed.
`searchEndpoints`|A list of other VocPrez instances to query across with the VocPrez federated search.
`systemUri`|The URI of this Prez instance
`systemInfo`|Details for each *Prez type as well as the top-level Prez instance. Used for display and profile data.
`appName`|The name of this deployment. Used in naming Kubernetes resources. Ensure this name is unique to other Prez deployments if in the same infrastructure.
`deploymentMethod`|Selects the method of deployment. Available choices are: "kubernetes", "docker", "ecs" (not yet implemented). Each corresponds to a template file in `deploy/`. The docker option uses docker-compose.
`storageClass`|For use in the kubernetes deployment method. Specifies the StorageClass to use for mounting the theme volume. The `ebs-sc` StorageClass is provided in `deploy/kube/kube-ebs-storage-class.yaml`, which uses AWS EBS as the volume storage. The StorageClass to be used must be created separately in kubernetes before deploying Prez.
`version`|The version of the Prez Docker image to be used

## Theming
The `theme/` folder contains the HTML, CSS, JavaScript & image files to be mounted as a volume in a container deployment. Ensure to follow the provided folder structure.

### Jinja2 Templates
Jinja2 HTML templates go under `templates/`, (which can include `fonts.html`, which can contain `<link>` elements for fonts). These files override the default templates in [Prez](https://github.com/surroundaustralia/Prez/tree/main/prez/templates).

### CSS
Several CSS variables have been exposed for easy customisation, see the available variables [here](https://github.com/surroundaustralia/Prez/blob/main/prez/static/sass/_variables.scss). Note that only CSS variables (e.g. `--primary`) can be overridden. Prez only accepts CSS styling from `{themeVolume}/static/css/theme.css`.

## Deployment
Prez is designed to be deployed in a containerised environment. `pipeline_script.py` will perform token replacement from values in `config.yaml` to the deployment file chosen in the `deploymentMethod` field in `config.yaml`. Currently, three deployment types are supported: Docker (docker-compose), Kubernetes & ECS.

Note: Only the Kubernetes option is fully implemented.

### Docker Container
Use `docker-compose.yml`, otherwise a simple shell script `docker-run.sh` is provided to run a docker container locally.

### Kubernetes

- Volume
    - Persistent volume claim
- ConfigMap contains env vars for container
- Deployment
- Service
- Ingress

For AWS, a StorageClass with an EBS provisioner is recommended, provided in `deploy/kube/kube-ebs-storage-class.yaml`.

### ECS
Not yet implemented.

## Pipelines
This repo contains pipeline definitions for GitHub actions, BitBucket Pipelines & Azure Pipelines.

The SPARQL credentials (`{*Prez}_SPARQL_ENDPOINT` (required), `{*Prez}_SPARQL_USERNAME` & `{*Prez}_SPARQL_PASSWORD`) should be set as repository secrets.

All pipeline methods follow the same steps:

- Run `pipeline_script.py` for token replacement
- Depending on `deploymentMethod` value, deploy as necessary

### GitHub Actions

Currently, only the Kubernetes deployment option is supported, where EKS is used.

The required repository secrets are:

- `KUBE_CONFIG`
    - Obtained by locally running (if kubectl is installed locally & context has been set):
        ```bash
        cat $HOME/.kube/config | base64 
        ```
        - Note that any AWS_PROFILEs in this config should be removed beforehand
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Along with the required secrets for Prez itself (`{*Prez}_SPARQL_ENDPOINT` (required), `{*Prez}_SPARQL_USERNAME` & `{*Prez}_SPARQL_PASSWORD`).

### BitBucket Pipelines
Not yet implemented.

### Azure Pipelines
Not yet implemented.
