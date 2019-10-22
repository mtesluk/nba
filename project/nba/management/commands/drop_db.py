from django.core.management.base import BaseCommand
import MySQLdb
from project.settings import DATABASES


class Command(BaseCommand):
    help = 'Clear all data in database'

    def handle(self, *args, **options):
        try:
            db = MySQLdb.connect(host=DATABASES["default"]["HOST"],
                                 user=DATABASES["default"]["USER"],
                                 passwd=DATABASES["default"]["PASSWORD"])
            cur = db.cursor()
            cur.execute("DROP DATABASE %s;" % DATABASES["default"]["NAME"])
            db.close()
            self.stdout.write(self.style.SUCCESS("Database dropped!"))
        except:
            self.stdout.write(self.style.ERROR("Something went wrong during droping database!"))
