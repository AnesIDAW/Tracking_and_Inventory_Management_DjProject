from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = "Test Redis connection"

    def handle(self, *args, **kwargs):
        cache.set('redis_test_key', 'Hello from Redis!', timeout=10)
        value = cache.get('redis_test_key')
        if value:
            self.stdout.write(self.style.SUCCESS(f"Redis is working: {value}"))
        else:
            self.stderr.write("Redis test failed")
