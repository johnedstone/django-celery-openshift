from django.core.management.base import BaseCommand, CommandError

from dashboard.views import _populate_build_config_objects

class Command(BaseCommand):
    help = 'Populates database with BuildConfigs'

    def handle(self, *args, **options):
        result = _populate_build_config_objects()
        if result:
            self.stdout.write(self.style.SUCCESS('{}'.format(result)))
        self.stdout.write(self.style.SUCCESS('Finished trying to populate database with the Build Configs'))

# vim: ai et ts=4 sts=4 sw=4 nu
