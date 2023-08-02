import os

base_directory = os.path.join(os.getcwd(), "self-guided-labs")

def test_env_file():
    env_path = base_directory + '/.env'
    assert os.path.exists(env_path)