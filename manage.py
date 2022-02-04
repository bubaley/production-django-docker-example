#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ


def main():
    root = environ.Path(__file__) - 1
    env = environ.Env()
    environ.Env.read_env(root('core', 'settings', '.env'))
    debug = env.bool('DEBUG', default=True)
    current_env = 'core.settings.dev' if debug else 'core.settings.prod'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', current_env)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
