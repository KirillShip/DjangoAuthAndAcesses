import threading
import time
from .models import Session
from django.utils import timezone


def cleanup(seconds):
    while True:
        time.sleep(seconds)
        try:
            Session.objects.filter(expires_at__lt = timezone.now()).delete()
        except Session.DoesNotExist:
            pass

thread = threading.Thread(target = cleanup, args = (12*60*60,), daemon = True)

def start_timer():
    thread.start()
