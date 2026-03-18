import os

from google.oauth2 import credentials as oauth2_credentials
from testframework.util.assertion import assert_not_null


def get_gcp_project_id():
    project_id = os.environ["GCP_PROJECT_ID"]
    assert_not_null(project_id)
    return project_id


def get_gcp_backup_project_id():
    backup_project_id = os.environ["GCP_BACKUP_PROJECT"]
    assert_not_null(backup_project_id)
    return backup_project_id


def get_bigtable_project_id():
    bigtable_project_id = os.environ["BIGTABLE_PROJECT_ID"]
    assert_not_null(bigtable_project_id)
    return bigtable_project_id


def get_credentials():
    """
    Get credentials from GOOGLE_OAUTH_ACCESS_TOKEN env var if available,
    otherwise fall back to Application Default Credentials.

    Returns:
        google.oauth2.credentials.Credentials if token is set, None for ADC fallback
    """
    token = os.environ.get('GOOGLE_OAUTH_ACCESS_TOKEN')

    if token:
        # Create credentials from access token
        # Note: This creates a credential without refresh capability
        return oauth2_credentials.Credentials(token=token)

    # Return None to use Application Default Credentials (current behavior)
    return None


