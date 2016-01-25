def setup_django_env():
    import os, django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()