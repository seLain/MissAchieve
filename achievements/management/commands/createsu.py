from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
	def handle(self, *args, **options):
		try:
			from achievements import secret_settings as settings
			if not User.objects.filter(username=settings.DEFAULT_ADMIN).exists():
				User.objects.create_superuser(settings.DEFAULT_ADMIN, settings.DEFAULT_ADMIN_PASSWORD, settings.DEFAULT_ADMIN_MAIL)
		except ImportError:
			# [todo] add log to this exception and give instrucitons
			print('Oops. Can not import achievements.secret_settings')
			print('Please check if achievements.settings.py exists.')
			print('No admin superuser created.')
			pass
		except AttributeError:
			# [todo] add log to this exception and give instrucitons
			print('Oops. Can not find needed settings in achievements.secret_settings.py')
			print('Please refer to achievements.settings.example.py')
			print('No admin superuser created.')
			pass