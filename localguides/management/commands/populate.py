from django.core.management.base import BaseCommand
from datetime import date, timedelta
from localguides.models import Guide
from tourist.models import Availability

class Command(BaseCommand):
    help = 'Populate Availability table with data'

    def handle(self, *args, **options):
        # Define the start and end dates for availability
        start_date = date(2023, 11, 22)
        end_date = date(2023, 12, 28)

        local_guides = Guide.objects.all()

        for guide in local_guides:
            current_date = start_date
            while current_date <= end_date:
                availability = Availability(
                    local_guide=guide,
                    availability_date=current_date,
                    is_booked=False  # You can set this to True if any dates are already booked
                )
                availability.save()
                current_date += timedelta(days=1)
        self.stdout.write(self.style.SUCCESS('Availability data has been populated successfully.'))



