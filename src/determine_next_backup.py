from setup import *
from read_ini_file import UPDATEINIFILE
from get_days_name import get_days_name
from backup_was_already_made import backup_was_already_made
import datetime


MAIN_INI_FILE = UPDATEINIFILE()


def get_next_backup():
   # print(MAIN_INI_FILE.day_name())
   # print(get_days_name())
   # print(get_day_index())
   # print(MAIN_INI_FILE.get_database_value('DAYS', 'mon'))
   # print(int(MAIN_INI_FILE.current_time()))
   # print(int(MAIN_INI_FILE.backup_time_military()))
   
   # Check if today is the day to backup
   if MAIN_INI_FILE.day_name() == get_days_name():  # Will return ex. Mon == Mon, so is today
      # Had yet not backup today # 1000 1030
      if int(MAIN_INI_FILE.current_hour()) <= int(MAIN_INI_FILE.get_database_value('SCHEDULE', 'hours')) and int(MAIN_INI_FILE.current_minute()) > int(MAIN_INI_FILE.get_database_value('SCHEDULE', 'minutes')):
         # Check if a backup was made today
         if not backup_was_already_made():      
            return "Today"
         else:
            return check_days()
      # Has already made a backup
      else:
         return check_days()
   else:
      return check_days()

def check_days():
   # If todays day's index is:

   # SUN
   if get_day_index() == 0:
      if MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
         return get_locale_settings_language(1)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
         return get_locale_settings_language(2)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
         return get_locale_settings_language(3)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
         return get_locale_settings_language(4)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
         return get_locale_settings_language(5)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
         return get_locale_settings_language(6)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
         return get_locale_settings_language(0)
      
      else:
         return "None"
      
   # MON
   elif get_day_index() == 1:
      if MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
         return get_locale_settings_language(1)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
         return get_locale_settings_language(2)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
         return get_locale_settings_language(3)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
         return get_locale_settings_language(4)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
         return get_locale_settings_language(5)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
         return get_locale_settings_language(6)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
         return get_locale_settings_language(7)
      
      else:
         return "None"

   # TUE
   elif get_day_index() == 2:
      if MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
         return get_locale_settings_language(1)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
         return get_locale_settings_language(2)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
         return get_locale_settings_language(3)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
         return get_locale_settings_language(4)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
         return get_locale_settings_language(5)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
         return get_locale_settings_language(6)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
         return get_locale_settings_language(7)

      else:
         return "None"
   # WED
   elif get_day_index() == 3:
      if MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
         return get_locale_settings_language(1)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
         return get_locale_settings_language(2)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
         return get_locale_settings_language(3)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
         return get_locale_settings_language(4)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
         return get_locale_settings_language(5)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
         return get_locale_settings_language(6)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
         return get_locale_settings_language(7)

      else:
         return "None"

   # THU
   elif get_day_index() == 4:
      if MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
         return get_locale_settings_language(1)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
         return get_locale_settings_language(2)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
         return get_locale_settings_language(3)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
         return get_locale_settings_language(4)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
         return get_locale_settings_language(5)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
         return get_locale_settings_language(6)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
         return get_locale_settings_language(7)
      
      else:
         return "None"
   
   # FRI
   elif get_day_index() == 5:
      if MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
         return get_locale_settings_language(1)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
         return get_locale_settings_language(2)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
         return get_locale_settings_language(3)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
         return get_locale_settings_language(4)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
         return get_locale_settings_language(5)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
         return get_locale_settings_language(6)
      
      if MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
         return get_locale_settings_language(7)
      
      else:
         return "None"
   # SAT   
   elif get_day_index() == 6:
      if MAIN_INI_FILE.get_database_value('DAYS', 'sun'):
         return get_locale_settings_language(1)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'mon'):
         return get_locale_settings_language(2)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'tue'):
         return get_locale_settings_language(3)

      elif MAIN_INI_FILE.get_database_value('DAYS', 'wed'):
         return get_locale_settings_language(4)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'thu'):
         return get_locale_settings_language(5)
      
      if MAIN_INI_FILE.get_database_value('DAYS', 'fri'):
         return get_locale_settings_language(6)
      
      elif MAIN_INI_FILE.get_database_value('DAYS', 'sat'):
         return get_locale_settings_language(7)

      else:
         return "None"
      
def get_locale_settings_language(day_number):
   # print("NUMBER:", day_number)

   # Get users locale settings language
   user_locale = locale.getdefaultlocale()
   user_locale_str = f"{user_locale[0]}.{user_locale[1].lower()}"
   # print("user_locale:", user_locale_str)

   # Set the locale for the current session to English (United States)
   locale.setlocale(locale.LC_TIME, user_locale_str)
   # Get the current date
   current_date = datetime.datetime.today()
   # Add one day to the current date
   next_backup_date = current_date + datetime.timedelta(days=day_number)
   # Get the day of the week for the next backup date
   return next_backup_date.strftime('%a')

def get_day_index():
   # Get the current date
   today = datetime.date.today()

   # Get the day index number (0 for Sunday, 1 for Monday, ..., 6 for Saturday)
   day_index = today.weekday()

   # Adjust the day index to represent Sunday as 0
   adjusted_day_index = (day_index + 1) % 7

   return adjusted_day_index


if __name__ == '__main__':
   pass