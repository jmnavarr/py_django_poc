from django.core.management.base import BaseCommand, CommandError
from social.models import Keyword
from social.libraries import keywordlib

class Command(BaseCommand):
    help = 'Cron to pull search content from social media sites'

    def handle(self, *args, **options):
        keywords = Keyword.objects.all()

        for keyword in keywords:
            try:
                keywordlib.search(keyword.id)
            except:
                CommandError("Exception occurred. Please verify")

        self.stdout.write(self.style.SUCCESS('Successfully pulled content'))