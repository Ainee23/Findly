import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Findly.settings")
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

if not user:
    user = User.objects.create_user(email='test@example.com', password='password')

c = Client()
print(f"Testing for user pk: {user.pk}")
response = c.get(f'/qr/user_image/{user.pk}/')

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print(f"Content Type: {response['Content-Type']}")
    print(f"Response content length: {len(response.content)}")
else:
    print("Error content:")
    print(response.content.decode('utf-8')[:1000])

