import os
from django.core.management import BaseCommand, call_command
from team4.models import Facility # Adjust if your model name is different

class Command(BaseCommand):
    help = 'Cleans the database and runs all load commands in order'

    def handle(self, *args, **options):
        db = 'team4' # Default database based on your previous logs

        # 1. Clear existing Facility data
        # We clear Facilities first because they have Foreign Keys to Cities/Categories
        self.stdout.write(self.style.WARNING('🗑️  Clearing all existing Facility records...'))
        Facility.objects.using(db).all().delete()

        # 2. Execution Order
        # We run dependencies first, then the main data
        commands_to_run = [
            # Infrastructure (Run these first)
            'load_provinces',
            'load_cities',
            'load_villages',
            'load_category',
            'load_amenity',
            
            # Facilities (Run these last)
            'load_hospitals',
            'load_hotels',
            'load_restaurants',
        ]

        for cmd in commands_to_run:
            self.stdout.write(self.style.SUCCESS(f'\n🚀 Running: python manage.py {cmd}'))
            try:
                # call_command runs your existing scripts automatically
                call_command(cmd, database=db)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error in {cmd}: {e}'))

        self.stdout.write(self.style.SUCCESS('\n✨ All data has been successfully reloaded!'))
        
        # Optional: Show final stats
        call_command('show_stats')