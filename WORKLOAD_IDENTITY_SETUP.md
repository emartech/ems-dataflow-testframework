# Workload Identity Federation Setup

## Overview

This framework has been modified to support authentication via OAuth access tokens through the `GOOGLE_OAUTH_ACCESS_TOKEN` environment variable, while maintaining backward compatibility with Application Default Credentials (ADC).

## Changes Made

### 1. Updated Dependencies
- `google-auth` upgraded from `1.6.3` to `>=1.10.0,<2.0.0` to support OAuth2 token credentials

### 2. Added Credential Helper
- New function `get_credentials()` in `testframework/config/environment.py`
- Checks for `GOOGLE_OAUTH_ACCESS_TOKEN` environment variable
- Falls back to ADC if not set (maintains existing behavior)

### 3. Updated Client Creation
All GCP client creation functions now support credentials:
- `publisher_client()` - Pub/Sub Publisher
- `subscriber_client()` - Pub/Sub Subscriber
- `bigquery_client()` - BigQuery
- `bigquery_backup_client()` - BigQuery backup
- `bigtable_table()` - Bigtable
- `bigtable_table_inserter()` - Bigtable inserter
- `bt_table()` - Bigtable table fixture
- `bt_instance()` - Bigtable instance fixture

## Usage

### Option 1: With Access Token (Workload Identity)

Set the `GOOGLE_OAUTH_ACCESS_TOKEN` environment variable with a valid OAuth2 access token:

```bash
export GOOGLE_OAUTH_ACCESS_TOKEN="ya29.a0AfH6SMB..."
pytest
```

Or inline:

```bash
GOOGLE_OAUTH_ACCESS_TOKEN="ya29.a0AfH6SMB..." pytest
```

### Option 2: Application Default Credentials (Default)

If `GOOGLE_OAUTH_ACCESS_TOKEN` is not set, the framework uses ADC as before:

```bash
gcloud auth application-default login
pytest
```

## Obtaining Access Tokens for Workload Identity

You'll need to obtain access tokens from your workload identity provider. Common approaches:

### 1. Using gcloud (for testing)
```bash
export GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token)
pytest
```

### 2. From CI/CD Pipeline
Your CI/CD system should provide access tokens through workload identity federation. Example for GitHub Actions:

```yaml
- id: 'auth'
  uses: 'google-github-actions/auth@v1'
  with:
    workload_identity_provider: 'projects/.../locations/.../workloadIdentityPools/.../providers/...'
    service_account: 'sa@project.iam.gserviceaccount.com'
    token_format: 'access_token'

- name: 'Run tests'
  env:
    GOOGLE_OAUTH_ACCESS_TOKEN: ${{ steps.auth.outputs.access_token }}
  run: pytest
```

### 3. External Token Service
If you have an external service that provides tokens:

```bash
TOKEN=$(curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token | jq -r .access_token)
export GOOGLE_OAUTH_ACCESS_TOKEN=$TOKEN
pytest
```

## Important Limitations

⚠️ **Token Expiry**: Access tokens are short-lived (typically 1 hour). The framework does NOT automatically refresh tokens. You must:
- Obtain fresh tokens before they expire
- Handle token refresh externally
- Re-run tests with new tokens if they expire mid-execution

⚠️ **No Refresh Capability**: Since we're using older client libraries, automatic token refresh is not supported. For long-running test suites, consider upgrading to modern GCP client libraries that support full Workload Identity Federation.

## Testing

Run the included test script to verify credential handling:

```bash
python test_credentials.py
```

## Migration Path

This solution is a temporary bridge to support workload identity with old libraries. For production use, plan to:

1. Upgrade to modern GCP client libraries:
   - `google-auth >= 2.3.0`
   - `google-cloud-bigtable >= 2.0.0`
   - `google-cloud-bigquery >= 3.0.0`
   - `google-cloud-pubsub >= 2.0.0`

2. Use Workload Identity Federation configuration files:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/workload-identity-config.json
   ```

3. Remove the `GOOGLE_OAUTH_ACCESS_TOKEN` handling and rely on native WIF support

## Troubleshooting

### "Invalid credentials" errors
- Verify your token is valid: `echo $GOOGLE_OAUTH_ACCESS_TOKEN`
- Check token hasn't expired (tokens typically last 1 hour)
- Obtain a fresh token: `export GOOGLE_OAUTH_ACCESS_TOKEN=$(gcloud auth print-access-token)`

### "Permission denied" errors
- Verify the service account associated with the token has required permissions
- Check IAM roles in GCP console

### Tests fail after running for a while
- Token likely expired mid-execution
- Obtain a fresh token and re-run tests
