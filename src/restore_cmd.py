#! /usr/bin/python3
from setup import *
from get_users_de import *
from read_ini_file import UPDATEINIFILE
from restore_backup_wallpaper import restore_backup_wallpaper
from restore_backup_home import restore_backup_home
from restore_backup_flatpaks_applications import restore_backup_flatpaks_applications
from restore_backup_package_applications import restore_backup_package_applications
from restore_backup_flatpaks_data import restore_backup_flatpaks_data
# from restart_kde_session import restart_kde_session
from restore_kde_share_config import restore_kde_share_config
from restore_kde_config import restore_kde_config
from restore_kde_local_share import restore_kde_local_share


################################################################################
## Signal
################################################################################
# If user turn off or kill the app, update INI file
signal.signal(signal.SIGINT, signal_exit)
signal.signal(signal.SIGTERM, signal_exit)

MAIN_INI_FILE = UPDATEINIFILE()

class RESTORE:
    def __init__(self):

        asyncio.run(self.start_restoring())

    async def start_restoring(self):
        # First change the wallpaper
        if MAIN_INI_FILE.ini_system_settings():
            # Update INI file
            CONFIG = configparser.ConfigParser()
            CONFIG.read(SRC_USER_CONFIG)
            with open(SRC_USER_CONFIG, 'w') as configfile:
                CONFIG.set('INFO', 'saved_notification', "Restoring wallpaper...")
                CONFIG.write(configfile)

            await restore_backup_wallpaper()
        
        # Restore home folder
        if MAIN_INI_FILE.ini_files_and_folders():
            # Update INI file
            CONFIG = configparser.ConfigParser()
            CONFIG.read(SRC_USER_CONFIG)
            with open(SRC_USER_CONFIG, 'w') as configfile:
                CONFIG.set('INFO', 'saved_notification', "Restoring Home...")
                CONFIG.write(configfile)

            await restore_backup_home()

        # Restore applications packages (.deb, .rpm etc.)
        if  MAIN_INI_FILE.ini_applications_packages():
            # Update INI file
            CONFIG = configparser.ConfigParser()
            CONFIG.read(SRC_USER_CONFIG)
            with open(SRC_USER_CONFIG, 'w') as configfile:
                CONFIG.set('INFO', 'saved_notification', "Restoring Applications...")
                CONFIG.write(configfile)

            await restore_backup_package_applications()
       
        # Restore flatpaks
        if MAIN_INI_FILE.ini_restore_flatpaks_name():
            # Update INI file
            CONFIG = configparser.ConfigParser()
            CONFIG.read(SRC_USER_CONFIG)
            with open(SRC_USER_CONFIG, 'w') as configfile:
                CONFIG.set('INFO', 'saved_notification', "Restoring Flatpaks Applications...")
                CONFIG.write(configfile)

            await restore_backup_flatpaks_applications()
        
        # Restore flatpaks data
        if MAIN_INI_FILE.ini_restore_flatpaks_data():
            # Update INI file
            CONFIG = configparser.ConfigParser()
            CONFIG.read(SRC_USER_CONFIG)
            with open(SRC_USER_CONFIG, 'w') as configfile:
                CONFIG.set('INFO', 'saved_notification', "Restoring Flatpak Data...")
                CONFIG.write(configfile)
            
            await restore_backup_flatpaks_data()
        
        # Restore system settings
        if MAIN_INI_FILE.ini_system_settings():
            # Only for kde
            if get_user_de() == 'kde':
                # Update INI file
                CONFIG = configparser.ConfigParser()
                CONFIG.read(SRC_USER_CONFIG)
                with open(SRC_USER_CONFIG, 'w') as configfile:
                    CONFIG.set('INFO', 'saved_notification', "Restoring KDE local/share...")
                    CONFIG.write(configfile)
    
                # Restore kde local share
                await restore_kde_local_share()
                
                # Update INI file
                CONFIG = configparser.ConfigParser()
                CONFIG.read(SRC_USER_CONFIG)
                with open(SRC_USER_CONFIG, 'w') as configfile:
                    CONFIG.set('INFO', 'saved_notification', "Restoring KDE config...")
                    CONFIG.write(configfile)
     
                # Restore kde CONFIG
                await restore_kde_config()

                # Update INI file
                CONFIG = configparser.ConfigParser()
                CONFIG.read(SRC_USER_CONFIG)
                with open(SRC_USER_CONFIG, 'w') as configfile:
                    CONFIG.set('INFO', 'saved_notification', "Restoring KDE share/CONFIG...")
                    CONFIG.write(configfile)

                # Restore kde share CONFIG
                await restore_kde_share_config()
                
                # Restart KDE session
                # restart_kde_session()
        
        self.end_restoring()

    def end_restoring(self):
        print("Ending restoring...")

        # Update INI file
        CONFIG = configparser.ConfigParser()
        CONFIG.read(SRC_USER_CONFIG)
        with open(SRC_USER_CONFIG, 'w') as configfile:
            CONFIG.set('INFO', 'saved_notification', "")
            CONFIG.write(configfile)

        # After backup is done
        print("Restoring is done!")

        if MAIN_INI_FILE.ini_automatically_reboot():
            sub.run("sudo reboot", shell=True)
        else:
            exit()


if __name__ == '__main__':
    main = RESTORE()
