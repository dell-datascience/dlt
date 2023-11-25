# Provision google cloud storage and BigQuery database via Terraform

## 1. GCP Setup

### Project infrastructure requirements:
* Google Cloud Storage (GCS): Data Lake
* BigQuery: Data Warehouse


### Initial Setup

1. Create an account with your Google email ID 

2. Setup your first [project](https://console.cloud.google.com/) if you haven't already
    * eg. "Data_engineering_project", and note down the "Project ID" (we'll use this later when deploying infra with TF)

3. Setup [service account & authentication](https://cloud.google.com/docs/authentication/getting-started) for this project
    * Grant `Viewer` role to begin with.
    * Download service-account-keys (.json) for auth.

4. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
5. Set environment variable to point to your downloaded GCP keys:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   
   # Refresh token/session, and verify authentication
   gcloud auth application-default login
   ```
   
### Setup for Access
 
1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
   * Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
   * Click the *Edit principal* icon for your service account.
   * Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin**
   
2. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
   
3. Please ensure `GOOGLE_APPLICATION_CREDENTIALS` env-var is set.
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
   ```
 
## 2. Execution steps

#### Required files

* `main.tf`
* `variables.tf`
* Optional: `resources.tf`, `output.tf`
* `.tfstate`

## Run in terminal

1. Initialize & configures the backend, install plugins/providers, & check out an existing configuration from a version control 

        terraform init 
    
2. Matche/preview local changes against a remote state, and proposes an Execution Plan

        terraform plan
 
3.  Asks for approval to the proposed plan, and applies changes to cloud

            terraform apply

4.  Removes your stack from the Cloud

        terraform destroy


#### Nice to know
* `terraform`: configure basic Terraform settings to provision your infrastructure
   * `required_version`: minimum Terraform version to apply to your configuration
   * `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
      * `local`: stores state file locally as `terraform.tfstate`
   * `required_providers`: specifies the providers required by the current module
* `provider`:
   * adds a set of resource types and/or data sources that Terraform can manage
   * The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
* `resource`
  * blocks to define components of your infrastructure
  * Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
* `variable` & `locals`
  * runtime arguments and constants

### References
https://learn.hashicorp.com/collections/terraform/gcp-get-started
