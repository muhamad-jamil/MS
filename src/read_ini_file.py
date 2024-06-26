from setup import *
from create_directory import create_directory, create_file


NOW = datetime.now()

class UPDATEINIFILE:
    def report_error(self, e):
        from get_sizes import get_item_size
        
        # TODO
        # Max 1M size
        if get_item_size(LOG_LOCATION) >= 192:
            if os.path.exists(LOG_LOCATION):
                os.remove(LOG_LOCATION)

                # Check if the directory exists, and create it if necessary
                create_directory(LOG_LOCATION)
                # Check if the file exists, and create it if necessary
                create_file(LOG_LOCATION)

                # # Re create it
                # sub.run(
                #     ['touch', LOG_LOCATION],
                #     stdout=sub.PIPE,
                #     stderr=sub.PIPE)
                
        # Capture the current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Get the exception traceback as a string
        traceback_str = traceback.format_exc()
        
        # Write the timestamp, exception message, and traceback to the log file
        with open(LOG_LOCATION, 'a') as writer:
            writer.write(f"Timestamp: {timestamp}\n")
            writer.write(f"Exception: {str(e)}\n")
            writer.write(f"Traceback:\n{traceback_str}\n")
        
    def get_database_value(self, table, key):
        # Connect to the SQLite database
        # conn = sqlite3.connect(SRC_USER_CONFIG_DB)
        
        try:
            with sqlite3.connect(SRC_USER_CONFIG_DB) as conn:
                cursor = conn.cursor()

                # Query the value from the specified table and key
                cursor.execute(f"SELECT value FROM {table} WHERE key = ?", (f'{key}',))
                result = cursor.fetchone()

            # Close the connection
            # conn.close()

            if result:
                if result[0] == 'True' or result[0] == 'Yes':
                    return True
                
                elif result[0] == 'False' or result[0] == 'No':
                    return False
      
                elif result[0] == 'None':
                   return None
                   
                else:
                    return result[0]  # The value is the first element in the result tuple
            else:
                return None  # Return None if the key doesn't exist

        except Exception as e:
            pass

    def set_database_value(self, table, key, value):
        try:
            with sqlite3.connect(SRC_USER_CONFIG_DB) as conn:
                cursor = conn.cursor()
                    
                cursor.execute(f'''
                    INSERT OR REPLACE INTO {table} (key, value)
                    VALUES (?, ?)
                ''', (f'{key}', f'{value}'))

                conn.commit()

            # conn.close()
        
        except Exception as e:
            pass
            
    def ini_info_wallpaper(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['wallpaper']

    def ini_info_icon(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['icon']

    def ini_info_cursor(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['cursor']

    def ini_info_font(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['font']

    def ini_info_colortheme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['colortheme']

    def ini_info_gtktheme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['gtktheme']

    def ini_info_theme(self):
        CONFIG = configparser.ConfigParser()
        CONFIG.read(f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}")
        return CONFIG['INFO']['theme']

    ####################################################################
    # Date/time
    ####################################################################
    def day_name(self):
        NOW = datetime.now()
        return str(NOW.strftime("%a"))

    def current_date(self):
        NOW = datetime.now()
        return NOW.strftime("%d")

    def current_month(self):
        NOW = datetime.now()
        return NOW.strftime("%m")

    def current_year(self):
        NOW = datetime.now()
        return NOW.strftime("%y")

    def current_hour(self):
        # With 'now', current time will update by each hour
        NOW = datetime.now()
        return NOW.strftime("%H")

    def current_minute(self):
        # With 'now', current time will update by each minute
        NOW = datetime.now()
        return NOW.strftime("%M")

    def current_second(self):
        NOW = datetime.now()
        return int(NOW.strftime("%S"))

    def date_folder_format(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}"

    def current_full_date(self):
        return f'{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}'

    def current_full_date_plus_time_str(self):
        return f'{str(self.current_date())}-{str(self.current_month())}-{str(self.current_year())}, {str(self.current_hour())}:{str(self.current_minute())}'
    
    def time_folder_format(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/{str(self.backup_date())}-{str(self.backup_month())}-{str(self.backup_year())}/{str(self.backup_hour())}-{str(self.backup_minute())}"

    def current_time(self):
        NOW = datetime.now()
        return NOW.strftime("%H%M")

    def oldest_backup_date(self):
        # Get current date to 'oldest_backup_date'
        return str(self.get_database_value(
                'INFO', 'oldest_backup_date'))
    
    # def latest_backup_date(self):
    #     # Get current date to 'oldest_backup_date'
    #     return str(self.get_database_value(
    #             'INFO', 'latest_backup_date'))
    
    def latest_backup_date(self):
        dates = []
        for i in os.listdir(self.backup_folder_name()):
            # Exclude hidden files
            if '.' not in i:
                dates.append(i)
        dates.sort()

        try:
            return dates[0]
        except IndexError:
            return None
            
    def latest_backup_date_time_str(self):
        dates = []
        # times = []

        for i in os.listdir(self.backup_folder_name()):
            # Exclude hidden files
            if '.' not in i:
                dates.append(i)
        dates.sort()
    
        # # Search in dates[0]
        # for i in os.listdir(os.path.join(self.backup_dates_location(), dates[0])):
        #     times.append(i)
        #     print(i)
            
        try:
            return dates[0] # + ', ' + times[0]
        except IndexError:
            return None
        
    def backup_year(self):
        return NOW.strftime("%y")

    def backup_month(self):
        return NOW.strftime("%m")

    def backup_date(self):
        return NOW.strftime("%d")

    def backup_hour(self):
        return NOW.strftime("%H")

    def backup_minute(self):
        return NOW.strftime("%M")

    def backup_time_military(self):
        return int(f"{self.get_database_value('SCHEDULE', 'hours')}{self.get_database_value('SCHEDULE', 'minutes')}")
    
    def backup_dates_location(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}" 
    
    ####################################################################
    # HD
    ####################################################################
    def hd_name(self):
        return self.get_database_value('EXTERNAL', 'name')
    
    def hd_hd(self):
        return self.get_database_value('EXTERNAL', 'hd')

    ####################################################################
    # SCHEDULE
    ####################################################################
    def next_backup_hour(self):
        return int(self.get_database_value('SCHEDULE', 'hours')) 
    
    def next_backup_minutes(self):
        return self.get_database_value('SCHEDULE', 'minutes') 

    ####################################################################
    # STATUS
    ####################################################################
    def last_checked_time(self):
        return self.get_database_value('STATUS', 'latest_backup_date') 
    
    def automatically_backup(self):
        return self.get_database_value('STATUS', 'automatically_backup') 
    
    def current_backing_up(self):
        return self.get_database_value('STATUS', 'backing_up_now') 
    
    def current_restoring(self):
        return self.get_database_value('STATUS', 'is_restoring') 

    ####################################################################
    # MODE
    ####################################################################
    def one_time_mode(self):
        return self.get_database_value('MODE', 'one_time_mode') 
            
    ####################################################################
    # Folder creation
    ####################################################################
    def create_base_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}"

    def backup_folder_name(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}"

    # Wallpaper
    def wallpaper_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{WALLPAPER_FOLDER_NAME}"

    def application_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}"

    def main_backup_folder(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/.main_backup"

    ####################################################################
    # File creation
    ####################################################################
    def include_to_backup(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/.include_to_backup.txt"

    ####################################################################
    # System settings
    ####################################################################
    def icon_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{ICONS_FOLDER_NAME}"

    def cursor_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{CURSORS_FOLDER_NAME}"

    def fonts_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FONTS_FOLDER_NAME}"

    def gtk_theme_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GTK_THEME_FOLDER_NAME}"

    def theme_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{THEMES_FOLDER_NAME}"

    ####################################################################
    # KDE
    ####################################################################
    # Create kde folder
    def kde_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}"

    # KDE configurration folder
    def kde_configurations_folder_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}"

    # KDE CONFIG folder
    def kde_config_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{CONFIG_FOLDER_NAME}"

    # KDE .local/share
    def kde_local_share_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_FOLDER_NAME}"

    # KDE .kde/share
    def kde_share_config_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{KDE_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_CONFIG_FOLDER_NAME}"

    ####################################################################
    # GNOME
    ####################################################################
    # Create gnome folder
    def gnome_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}"

    def gnome_configurations_folder_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}"

    # GNOME CONFIG folder
    def gnome_config_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{CONFIG_FOLDER_NAME}"

    # GNOME share folder
    def gnome_local_share_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{GNOME_FOLDER_NAME}/{CONFIGURATIONS_FOLDER_NAME}/{SHARE_FOLDER_NAME}"

    ####################################################################
    # Packages managers
    ####################################################################
    # .rpm
    def rpm_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{RPM_FOLDER_NAME}"

    # .deb
    def deb_main_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{DEB_FOLDER_NAME}"

    ####################################################################
    # Flatpak
    ####################################################################
    def flatpak_txt_location(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{FLATPAK_TXT}"
    
    def flatpak_var_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{VAR_FOLDER_NAME}"

    def flatpak_local_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}/{SHARE_FOLDER_NAME}"
    
    def create_flatpak_folder(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{FLATPAK_FOLDER_NAME}"
    
    ####################################################################
    # Pip
    ####################################################################
    def pip_packages_txt_location(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/pip/pip_packages.txt"

    ####################################################################
    # Exclude
    ####################################################################
    def exclude_applications_location(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{SRC_EXCLUDE_APPLICATIONS}"

    def exclude_pip_location(self):
        return f"{self.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/{APPLICATIONS_FOLDER_NAME}/{SRC_EXCLUDE_PIP}"

    def restore_settings_location(self):
        return f"{str(self.get_database_value('EXTERNAL', 'hd'))}/{BASE_FOLDER_NAME}/{RESTORE_SETTINGS_INI}"

    def get_backup_home_folders(self):
        from get_latest_backup_date import latest_backup_date
        return f"{self.backup_folder_name()}/{latest_backup_date()}"


if __name__ == '__main__':
    MAIN_INI_FILE = UPDATEINIFILE()
    # MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
    print(MAIN_INI_FILE.latest_backup_date_time_str())
    pass
