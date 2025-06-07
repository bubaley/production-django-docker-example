import json
from pathlib import Path


def get_version():
    version_path = Path(__file__).resolve().parent.parent.parent / 'version.json'
    try:
        with open(version_path) as f:
            return json.load(f)['version']
    except Exception:
        return '0.0.0'


__version__ = get_version()
