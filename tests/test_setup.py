import os
from dotenv import load_dotenv

base_directory = os.path.join(os.getcwd(), "self-guided-labs")

def test_env_file_exists():
    env_path = base_directory + '/.env'
    assert os.path.exists(env_path)


def test_env_file_filled():
    env_path = base_directory + '/.env'
    load_dotenv(env_path)

    api_key = os.getenv("API_KEY", None)
    ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
    project_id = os.getenv("PROJECT_ID", None)

    assert api_key is not None, f"No api_key found in {env_path}"
    assert ibm_cloud_url is not None, f"No ibm_cloud_url found in {env_path}"
    assert project_id is not None, f"No project_id found in {env_path}"
