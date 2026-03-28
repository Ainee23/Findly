import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Findly.settings")
import django
django.setup()

try:
    from qr.utils import make_qr_png
    img_bytes = make_qr_png("http://example.com")
    print("Success! Bytes:", len(img_bytes))
except Exception as e:
    import traceback
    traceback.print_exc()
