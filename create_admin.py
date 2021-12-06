from django.contrib.auth import get_user_model
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backendland.settings")
django.setup()
User = get_user_model()
User.objects.create_superuser('admin2', 'bogi@gmail.com', 'admin2')