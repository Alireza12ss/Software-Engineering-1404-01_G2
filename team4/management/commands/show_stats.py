from django.core.management.base import BaseCommand
from team4.models import Facility, City, Province, Category, Amenity, Village

class Command(BaseCommand):
    help = 'Displays statistics for all imported data'

    def add_arguments(self, parser):
        parser.add_argument('--database', type=str, default='team4')

    def handle(self, *args, **options):
        db = options['database']

        self.stdout.write(self.style.MIGRATE_HEADING('\n📊 --- Database Statistics ---'))

        # Define the models to count
        stats = [
            ('Provinces', Province),
            ('Cities', City),
            ('Villages', Village),
            ('Categories', Category),
            ('Amenities', Amenity),
        ]

        # 1. Show Infrastructure Stats
        for label, model in stats:
            count = model.objects.using(db).count()
            self.stdout.write(f'{label:12}: {count}')

        self.stdout.write(self.style.MIGRATE_HEADING('\n🏥 --- Facilities Breakdown ---'))

        # 2. Show Facility breakdown by Category
        facilities = Facility.objects.using(db).all()
        total_facilities = facilities.count()

        # Breakdown by categories found in the database
        facility_types = Category.objects.using(db).all()
        
        for cat in facility_types:
            count = facilities.filter(category=cat).count()
            if count > 0:
                self.stdout.write(f'{cat.name_fa:12}: {count} ({cat.name_en})')

        self.stdout.write(self.style.SUCCESS(f'\nTotal Facilities: {total_facilities}'))
        self.stdout.write(self.style.MIGRATE_HEADING('-----------------------------\n'))