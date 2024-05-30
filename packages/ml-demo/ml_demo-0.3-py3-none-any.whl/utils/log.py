import os


def get_path():
    env_path = os.environ.get("path")
    print(f'env path = {env_path}')