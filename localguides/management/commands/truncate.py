from django.core.management.base import BaseCommand
from tourist.models import Availability  # Import the model you want to work with
from localguides.models import Booking

class Command(BaseCommand):
    """
    A management command to delete all data from MyModel.
    """

    help = 'Delete all data from MyModel'

    def handle(self, *args, **options):
        """
        Deletes all data from MyModel.

        This method deletes all data from the `Availability` and `Booking` models.
        It then prints a success message to the console.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        Returns:
            None
        """
        Availability.objects.all().delete()
        Booking.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All data from MyModel deleted successfully'))
