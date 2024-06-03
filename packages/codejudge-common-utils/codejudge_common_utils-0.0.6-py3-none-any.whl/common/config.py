import importlib
import os


def get_config_module():
    repo_context = os.getenv('REPO_CONTEXT')
    if repo_context == 'CODEJUDGE':
        return importlib.import_module('dev.config')
    elif repo_context == 'RECRUIT':
        return importlib.import_module('recruit.config')
    else:
        raise ImportError("Unsupported or missing REPO_CONTEXT environment variable")