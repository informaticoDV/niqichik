# create_superuser.py
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "david.valenzuela.oyaneder@gmail.com", "Admin.1991")