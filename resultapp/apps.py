from django.apps import AppConfig

class ResultappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resultapp'

    def ready(self):
        import os
        from django.contrib.auth import get_user_model

        if os.environ.get("CREATE_SUPERUSER") != "True":
            return

        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if username and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    password=password
                )