from setup import *
from ui.ui_mainwindow import Ui_MainWindow
from read_ini_file import UPDATEINIFILE

from ui.ui_dialog import Ui_Dialog
from ui.ui_options import Ui_Options

from stylesheet import *
from check_connection import is_connected
from device_location import device_location
from get_home_folders import get_home_folders
from handle_spaces import handle_spaces

from get_sizes import (
    get_all_max_backup_device_space,
    get_external_device_used_size,
    get_all_used_backup_device_space,
    get_used_backup_space)

from calculate_time_left_to_backup import calculate_time_left_to_backup
from update import backup_db_file
from save_info import save_info
from next_backup_label import next_backup_label
from create_backup_checker_desktop import create_backup_checker_desktop
from prepare_backup import PREPAREBACKUP


MAIN_INI_FILE = UPDATEINIFILE()

choose_device = []
capture_devices  = []


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the process name
        setproctitle.setproctitle("Time Machine")
        
        # Set application name
        self.setWindowTitle(APP_NAME)

        print(MAIN_INI_FILE.hd_hd())

        # Set application logo image
        logo_image = QPixmap(SRC_BACKUP_ICON)
        resized_logo_image = logo_image.scaledToWidth(32, Qt.SmoothTransformation)
        self.ui.app_logo_image.setPixmap(resized_logo_image)

        # Hide update button
        self.ui.update_available_button.hide()
        self.ui.progressbar_main_window.hide()

        ######################################################################
        # Connection
        #######################################################################
        # Browser backup device
        self.ui.browser_backup_device.clicked.connect(
            lambda: sub.Popen(
                ["xdg-open", MAIN_INI_FILE.create_base_folder()]))

        # Use select disk button
        self.ui.select_disk_button.clicked.connect(
            self.on_selected_disk_button_clicked)
        
        # Options button
        self.ui.options_button.clicked.connect(self.on_options_button_clicked)

        # Help button
        self.ui.help_button.clicked.connect(
            lambda: sub.Popen(["xdg-open", GITHUB_HOME]))

        # Update button
        self.ui.update_available_button.clicked.connect(self.on_update_button_clicked)
        
        # Remove device
        self.ui.remove_backup_device.clicked.connect(
            self.on_remove_device_clicked)

        ######################################################################
        # Add images 
        ######################################################################
        # Logo image
        logo_image = QPixmap(SRC_BACKUP_ICON)
        resized_logo_image = logo_image.scaledToWidth(28, Qt.SmoothTransformation)
        self.ui.app_logo_image.setPixmap(resized_logo_image)

        self.center_main_window()

    def center_main_window(self):
        centerPoint = QtGui.QScreen.availableGeometry(
            QtWidgets.QApplication.primaryScreen()).center()
        
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        # Check for update
        self.check_for_updates()

        # # Create essential folders, if a backup device was registered
        # if self.is_device_registered():
        #     if not os.path.exists(MAIN_INI_FILE.backup_folder_name()):
        #         # Create essensial folder exists in backup device
        #         create_base_folders()

        timer.timeout.connect(self.running)
        timer.start(1000)
        self.running()

    def running(self):
        # Check if a backup device was registered
        if self.is_device_registered():
            # Device was registered
            self.registered_action_to_take()
            
            # Check connection to it
            if is_connected(MAIN_INI_FILE.hd_hd()):
                ################################################
                # Clean notification massage
                ################################################
                # notification_message("")

                ################################################
                # Get backup devices size informations
                ################################################
                try:
                    ##########################
                    total = get_external_device_used_size()
                    minimum = get_used_backup_space()

                    # Filter total space
                    filter1 = []
                    for i in total:
                        if i.isdigit():
                            filter1.append(i)

                    # Filter total devices space
                    x = int(''.join(filter1))

                    ##########################
                    # Filter total space
                    filter2 = []
                    for i in minimum:
                        if i.isdigit():
                            filter2.append(i)

                    # Filter total devices space
                    y = int(''.join(filter2))

                    self.ui.external_size_label.setText(
                        # f'{get_all_used_backup_device_space(device=)} of {get_external_device_used_size()} used')
                        f' {minimum} of {get_all_max_backup_device_space()} used')
                    
                    # Update process bar space
                    self.ui.processbar_space.setMaximum(x)
                    self.ui.processbar_space.setValue(y)
                except:
                    self.ui.external_size_label.setText('')

                ################################################
                # Check if is current busy doing something
                ################################################
                # If is backing up right now
                if MAIN_INI_FILE.get_database_value('STATUS', 'backing_up_now'):
                    # Show 
                    # self.ui.progressbar_main_window.show()

                    # TODO
                    # Notification information
                    # self.ui.backups_label.setText(
                    #     MAIN_INI_FILE.get_database_value('INFO', 'current_backing_up'))
            
                    # TODO
                    # Show backing up labe
                    # self.ui.backing_up_label.show()

                    # Show current backing up
                    # self.ui.backing_up_label.setText(
                    #     f"{MAIN_INI_FILE.get_database_value('INFO', 'current_backing_up')}")
                    
                    # Disable select disk
                    self.ui.select_disk_button.setEnabled(False)
                    # Disable remove this disk
                    self.ui.remove_backup_device.setEnabled(False)

                    # UPDATE
                    # Update progress bar value
                    # pb_bar_value = MAIN_INI_FILE.get_database_value(
                    #                     'STATUS', 'progress_bar')
                    
                    # if pb_bar_value is not None:
                    #     # self.ui.progressbar_main_window.setValue(
                    #         int(pb_bar_value))

                else:
                    # Show
                    self.ui.next_backup_label.show()

                    # Enable select disk
                    self.ui.select_disk_button.setEnabled(True)

                    # Enable remove this disk
                    self.ui.remove_backup_device.setEnabled(True)

                # Automatically backup
                if MAIN_INI_FILE.automatically_backup():
                    if (59 - int(MAIN_INI_FILE.current_minute())) <= TIME_LEFT_WINDOW:
                        self.ui.next_backup_label.setText(
                            f'Next Backup: {calculate_time_left_to_backup()}')
                    else:
                        # Next backup label
                        self.ui.next_backup_label.setText(f'Next Backup: {next_backup_label()}')
                else:
                    self.ui.next_backup_label.setText(
                        'Next Backup: Automatic backups off')
                    
            ################################################
            # Has no connection to it
            ################################################
            else:
                self.ui.external_size_label.setText("No information available")

        else:
            # No device was registered yet
            self.not_registered_action_to_take()
            
    def is_device_registered(self):
        # Check if a backup device was registered
        if MAIN_INI_FILE.hd_name() is not None:
            return True
    
    ################################################################################
    # STATIC
    ################################################################################
    def check_for_updates(self):
        print('Checking for updates...')
        
        try:
            # Check for git updates
            git_update_command = os.popen(
                'git remote update && git status -uno').read()

            # Updates found
            if "Your branch is behind" in git_update_command:
                # Show update button
                self.ui.update_available_button.show()
            else:
                print("No new updates available...")
        except:
            pass

    def on_update_button_clicked(self):
        # Delete old log files
        if os.path.exists(LOG_LOCATION):
            try:
                os.remove(LOG_LOCATION)
                print(f"File '{LOG_LOCATION}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting file: {e}")

        # # Set system tray to False
        # MAIN_INI_FILE.set_database_value(
        #     'SYSTEMTRAY', 'system_tray', 'False')

        # # Set automatically backupt to False
        # MAIN_INI_FILE.set_database_value(
        #     'STATUS', 'automatically_backup', 'False')

        # Update and make save the DB
        backup_db_file(True)

        # Re-start few features
        if MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
            # Re-open system tray
            sub.Popen(['python3', SRC_SYSTEM_TRAY_PY])
        
        if MAIN_INI_FILE.get_database_value('STATUS', 'automatically_backup'):
            # Re-open backup checker
            sub.Popen(['python3', SRC_BACKUP_CHECKER_PY])

    def connected_action_to_take(self):
        self.ui.select_disk_button.setEnabled(True)

    def registered_action_to_take(self):
        try:
            # Show devices name
            self.ui.external_name_label.setText(f"{MAIN_INI_FILE.hd_name()}")
            
            # TODO
            # Show oldest backup label
            if MAIN_INI_FILE.latest_backup_date() is not None:
                self.ui.last_backup_label.setText(f'Last Backup: {MAIN_INI_FILE.latest_backup_date_time_str()}')
            else:
                self.ui.last_backup_label.setText(f'Last Backup: Only New Backup Dates Will Appear Here')
                 
            self.ui.next_backup_label.setText(f'Next Backup: None')

            # Show
            self.ui.frame_1.show()
            self.ui.frame_2.show()

            # Hide
            self.ui.select_disk_button.hide()
            
            # Show informations UI
            # self.ui.progressbar_main_window.show()
            self.ui.remove_backup_device.show()
        except FileNotFoundError:
            pass

    def not_registered_action_to_take(self):
            # Hide
            self.ui.frame_1.hide()
            self.ui.frame_2.hide()
            self.ui.remove_backup_device.hide()

            # Show
            self.ui.select_disk_button.show()
            
    def on_options_button_clicked(self):
        # options_window_class = OptionsWindow()

        # Show options window
        options_window_class.get_folders()

    def on_selected_disk_button_clicked(self):
        select_disk_class = SelectDisk()

        # Show dialog window
        select_disk_class.show_disk_dialog()
    
    def on_remove_device_clicked(self):
        reset_confirmation = QMessageBox.question(
            self,
            'Remove Device as Backup Storage',
            'Are you sure you want to remove this device as backup storage?',
            QMessageBox.Yes
            |
            QMessageBox.No,
            QMessageBox.No)

        if reset_confirmation == QMessageBox.Yes:            
            MAIN.ui.last_backup_label.setText("Last Backup:")
            MAIN.ui.next_backup_label.setText("Next Backup:")
            
            # Reset settings
            # Backup section
            MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'No')
            # MAIN_INI_FILE.set_database_value('STATUS', 'automatically_backup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'first_startup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_names', 'True')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'False')
            # MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')

            # INFO
            MAIN_INI_FILE.set_database_value('INFO', 'latest_backup_date', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'oldest_backup_date', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'latest_backup_to_main', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'latest_backup_time_check', 'None')

            # EXTERNAL  
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'hd', 'None')
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'name', 'None')
            
            # SYSTEMTRAY 
            # MAIN_INI_FILE.set_database_value('SYSTEMTRAY', 'system_tray', 'False')
            
            MAIN_INI_FILE.set_database_value('INFO', 'language', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'os', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'packageManager', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'theme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'icon', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'cursor', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'colortheme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', 'None')
            
            # Remove all keys first
            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Execute the DELETE statement to remove all rows from a table
            table_name = 'FOLDER'
            cursor.execute(f"DELETE FROM {table_name}")

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            MAIN_INI_FILE.set_database_value('FOLDER', 'pictures', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'documents', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'music', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'videos', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'desktop', 'True')

            print("All settings was reset!")

            # Hide informations UI
            # self.ui.progressbar_main_window.hide()
            self.ui.remove_backup_device.hide()

            # Show add backup devices button
            MAIN.ui.select_disk_button.show()
            # Enable at
            MAIN.ui.select_disk_button.setEnabled(True)

            # Hide
            self.ui.frame_1.hide()
            self.ui.frame_2.hide()
        else:
            QMessageBox.Close


class SelectDisk(QDialog):
    def __init__(self, parent=True):
        super().__init__()
        self.dialog_ui = Ui_Dialog()
        self.dialog_ui.setupUi(self)
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool)

        # Colors
        self.dialog_ui.use_disk_button_dialog.setStyleSheet('color: gray')

    def show_disk_dialog(self):
        ######################################################################
        # Connection
        ######################################################################
        # Cancel button dialog
        self.dialog_ui.cancel_button_dialog.clicked.connect(self.on_cancel_dialog_button_clicked)
        
        # Use disk button dialog
        self.dialog_ui.use_disk_button_dialog.clicked.connect(self.on_use_disk_dialog_button_clicked)
        
        ######################################################################
        # Hide or disable
        ######################################################################
        # Use disk button
        self.dialog_ui.use_disk_button_dialog.setEnabled(False)
        
        self.check_connection()

    def check_connection(self):
        ################################################################################
        # Search external inside /Media
        ################################################################################
        if device_location():
            try:
                # Add buttons and images for each external
                for backup_device in os.listdir(f'{MEDIA}/{USERNAME}'):
                    # No spaces and special characters allowed
                    if backup_device not in capture_devices  and "'" not in backup_device and " " not in backup_device:
                        self.devices_location = f'{MEDIA}/{USERNAME}/{backup_device}'
                        print("     Devices :", backup_device)
                        print(f"     Location:", self.devices_location)
                        
                        # Add to capture list
                        capture_devices.append(backup_device)

                        # Avaliables external  devices
                        self.available_devices = QPushButton()
                        self.available_devices.setFont(
                            QFont(MAIN_FONT, FONT_SIZE_11PX))
                        self.available_devices.setText(backup_device)
                        self.available_devices.setFixedHeight(52)
                        self.available_devices.setCheckable(True)
                        self.available_devices.setAutoExclusive(True)

                        # if MAIN_INI_FILE.hd_name() != "None":
                        #     self.available_devices.setAutoExclusive(True)
       
                        # Load the system icon 'audio-headset'
                        drive_media_icon = QIcon.fromTheme(
                            'drive-removable-media')

                        # Convert the QIcon to a QPixmap
                        audio_headset_pixmap = drive_media_icon.pixmap(32, 31)

                        from_image = QLabel(self.available_devices)
                        from_image.setPixmap(audio_headset_pixmap)
                        from_image.setScaledContents(True)
                        from_image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        from_image.move(10, (self.available_devices.height()) / 4)

                        # # Free Space Label
                        # free_space_label = QLabel(self.available_devices)
                        # free_space_label.setText(
                        #     f'<b>Storage Space: {get_all_max_backup_device_space()}</b>')
                        # free_space_label.setFont(QFont(MAIN_FONT, 8))
                        # free_space_label.move(
                        #     (self.available_devices.width() - 294), 22)
                        
                        text = self.available_devices.text()
                        self.available_devices.toggled.connect(
                            lambda *args, text=text: self.on_device_clicked(text))

                        ################################################################################
                        # Add widgets and Layouts
                        ################################################################################
                        self.dialog_ui.available_disk_dialog_layout.addWidget(self.available_devices, Qt.AlignLeft | Qt.AlignTop)
            except FileNotFoundError:
                pass

        # If backup devices found inside /Run
        else:
            try:
                # If x device is removed or unmounted, remove from screen
                for backup_device in os.listdir(f'{RUN}/{USERNAME}'):
                    # No spaces and special characters allowed
                    if backup_device not in capture_devices  and "'" not in backup_device and " " not in backup_device:
                        self.devices_location = f'{RUN}/{USERNAME}/{backup_device}'
                        print("     Devices :", backup_device)
                        print(f"     Location:", self.devices_location)

                        capture_devices .append(backup_device)

                        # Avaliables external  devices
                        self.available_devices = QPushButton()
                        self.available_devices.setFont(QFont(MAIN_FONT,FONT_SIZE_11PX))
                        self.available_devices.setText(backup_device)
                        self.available_devices.setCheckable(True)
                        self.available_devices.setAutoExclusive(True)
                        self.available_devices.setFixedHeight(52)
                        # self.available_devices.setStyleSheet(availableDeviceButtonStylesheet)
                        device = self.available_devices.text()

                        # Connect the device
                        self.available_devices.toggled.connect(lambda *args, device=device: self.on_device_clicked(device))

                        # Image
                        icon = QLabel(self.available_devices)
                        image = QPixmap(f"{SRC_RESTORE_ICON}")
                        image = image.scaled(46, 46, Qt.KeepAspectRatio)
                        icon.move(7, 7)
                        icon.setPixmap(image)

                        # # Free Space Label
                        # free_space_label = QLabel(self.available_devices)
                        # free_space_label.setText(
                        #     f'{get_all_used_backup_device_space(backup_device)} / {get_all_max_backup_device_space()}')
                        # free_space_label.setFont(QFont(MAIN_FONT, 8))
                        # free_space_label.setAlignment(Qt.AlignRight)
                        # free_space_label.move((self.available_devices.width() - 354), 32)
                        
                        text = self.available_devices.text()
                        self.available_devices.toggled.connect(lambda *args, text=text: self.on_device_clicked(text))

                        # ################################################################################
                        # # Add widgets and Layouts
                        # ################################################################################
                        # # Auto checked the choosed backup device
                        # if text == MAIN_INI_FILE.hd_name():
                        #     self.available_devices.setChecked(True)
                        #     # Add the saved device to to this layput
                        #     self.dialog_ui.backup_disk_dialog_layout.addWidget(self.available_devices, Qt.AlignLeft | Qt.AlignTop)
                        # else:
                        #     # Vertical layout
                        #     self.dialog_ui.available_disk_dialog_layout.addWidget(self.available_devices, Qt.AlignLeft | Qt.AlignTop)
            except FileNotFoundError:
                pass

        # Add strech to layout
        self.dialog_ui.available_disk_dialog_layout.addStretch()

        # Show the dialog
        self.exec()

    def on_use_disk_dialog_button_clicked(self):
        # Check devices permission
        if self.may_use_this_device():
            # Update INI file
            save_info(choose_device[-1])

            # Close dialog window
            self.on_cancel_dialog_button_clicked()

            # Show
            MAIN.ui.remove_backup_device.show()

            # Hide
            MAIN.ui.select_disk_button.hide()

            # Make the first backup
            self.make_first_backup()

    def may_use_this_device(self):
        try:
            # Try to write to storage
            test_file_path = os.path.join(self.devices_location, "write_test.txt")
            with open(test_file_path, "w") as test_file:
                test_file.write("Testing write permission")
            
            # If the write operation succeeded, delete the test file
            os.remove(test_file_path)

            return True
        
        except PermissionError as errno13:
            print(f"Permission denied error: {errno13}")
            # MAIN_INI_FILE.report_error(errno13)

            # Grant Write Permissions
            write_permission = QMessageBox.question(
                self,
                'Permission Denied',
                'To use this device, write permission is required. '
                f'\nDo you want to grant write permission for this device" {MAIN_INI_FILE.hd_name()}"?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)

            if write_permission == QMessageBox.Yes:
                # Execute the command
                # Command to grant write permissions to others
                command = [
                    "pkexec", 
                    "sudo", 
                    "chmod", 
                    "o+w", 
                    MAIN_INI_FILE.hd_name()]
                
                # Use pkexec for installing packages
                result = sub.run(
                    command, capture_output=True, text=True)
                
                return True
            else:
                QMessageBox.Close
                return False
                    
    def make_first_backup(self):
        # Base folder do no exists (TMB)
        if not os.path.exists(MAIN_INI_FILE.create_base_folder()):
            try:
                # Prepare backup disk
                MAIN_PREPARE.prepare_the_backup()

                creation_confirmation = QMessageBox.question(
                    self,
                    'Create First Backup',
                    'Do you want to create your first backup now?',
                    QMessageBox.Yes
                    |
                    QMessageBox.No,
                    QMessageBox.No)

                if creation_confirmation == QMessageBox.Yes:
                    # Go create the first backup
                    sub.Popen(
                        ['python3', SRC_ANALYSE_PY], 
                            stdout=sub.PIPE, 
                            stderr=sub.PIPE)
                else:
                    QMessageBox.Close
            except Exception as error:
                MAIN_INI_FILE.report_error(error)

    def on_device_clicked(self, device):
        # Enable use disk button
        self.dialog_ui.use_disk_button_dialog.setEnabled(True)
        self.dialog_ui.use_disk_button_dialog.setStyleSheet(
            """
                background-color: #2196f3;
                color: white;
            """)
        
        # Add to the list
        if device not in choose_device:
            # Add to choosed device list
            choose_device.insert(0, device)

    def on_cancel_dialog_button_clicked(self):
        # Clean lists
        capture_devices.clear()
        
        # Close dialog window 
        self.close()


class OptionsWindow(QDialog):
    def __init__(self, parent=True):
        super().__init__()
        self.options_ui = Ui_Options()
        self.options_ui.setupUi(self)
        # self.setWindowFlags(
        #     Qt.FramelessWindowHint | 
        #     Qt.WindowStaysOnTopHint | 
        #     Qt.Tool)

        # Already added
        self.home_folder_added = False
        
        # Flatpak data
        if MAIN_INI_FILE.get_database_value('STATUS', 'allow_flatpak_data'):
            self.options_ui.allow_flatpak_data_checkBox.setChecked(True)

        # Version
        self.options_ui.version_label.setText(APP_VERSION)


        # Automatically backup
        if MAIN_INI_FILE.automatically_backup():
            self.options_ui.automatically_backup_checkbox.setChecked(True)
        else:
            self.options_ui.automatically_backup_checkbox.setChecked(False)

        # System tray
        if MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
            self.options_ui.show_in_system_tray_checkbox.setChecked(True)
        else:
            self.options_ui.show_in_system_tray_checkbox.setChecked(False)
        
        # Experimental features
        if MAIN_INI_FILE.get_database_value('INFO', 'allow_browser_in_time_machine'):
            self.options_ui.allow_browser_in_time_machine.setChecked(True)
        else:
            self.options_ui.allow_browser_in_time_machine.setChecked(False)

        ######################################################################
        # Connection
        ######################################################################
        # Flatpaks
        self.options_ui.allow_flatpak_data_checkBox.clicked.connect(
            self.on_allow__flatpak_data_clicked)

        # Automatically backup checkbox
        self.options_ui.automatically_backup_checkbox.clicked.connect(
            self.on_automatically_checkbox_clicked)
        
        # System tray button
        self.options_ui.show_in_system_tray_checkbox.clicked.connect(
            self.on_system_tray_checkbox_clicked)
        
        # Experimental features
        self.options_ui.allow_browser_in_time_machine.clicked.connect(
            self.on_allow_browser_in_time_machine_clicked)
    
        # Reset
        self.options_ui.reset_button.clicked.connect(
            self.on_button_fix_clicked)

    def get_folders(self):
        # start tab index from 0
        self.options_ui.tabWidget.setCurrentIndex(0)

        if not self.home_folder_added:
            home_folders_list = []

            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Query all keys from the specified table
            cursor.execute(f"SELECT key FROM FOLDER")
            keys = [row[0] for row in cursor.fetchall()]

            # Close the connection
            conn.close()

            for key in keys:
                home_folders_list.append(key)

            ################################################################################
            # Get Home Folders and Sort them alphabetically
            # Add On Screen
            ################################################################################
            horizontal = 0
            vertical = 0

            for folder in get_home_folders():
                # Hide hidden folder
                if not "." in folder:
                    # Checkboxes
                    self.home_folders_checkbox = QCheckBox()
                    self.home_folders_checkbox.setText(folder)
                    self.home_folders_checkbox.adjustSize()
                    # self.home_folders_checkbox.setIcon(
                    # QIcon(f"{homeUser}/.local/share/{APPNAMEClose}/src/icons/folder.png"))
                    self.home_folders_checkbox.setStyleSheet(
                        "QCheckBox"
                        "{"
                        "border-color: transparent;"
                        "}")
                    self.home_folders_checkbox.clicked.connect(
                        lambda *args, folder = folder: self.on_folder_clicked(
                            folder))

                    # Activate checkboxes in user.ini
                    if folder.lower() in home_folders_list:
                        self.home_folders_checkbox.setChecked(True)

                    # Add to layout self.leftLayout
                    self.options_ui.grid_folders_layout.addWidget(
                        self.home_folders_checkbox, horizontal, vertical)

                    horizontal += 1

                    # Number of checkbox per column
                    if horizontal == 14:
                        vertical = 1
                        horizontal = 0
            
            self.home_folder_added = True
        
        # App loop
        self.exec()

    def on_folder_clicked(self, folder):
        # Handle spaces 
        folder = handle_spaces(folder)
        
        if MAIN_INI_FILE.get_database_value('FOLDER', f'{folder.lower()}'):
            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Delete the key-value pair from the 'STATUS' table
            cursor.execute(f'DELETE FROM FOLDER WHERE key = ?', (f'{folder.lower()}',))
            conn.commit()
        else:
            MAIN_INI_FILE.set_database_value('FOLDER', f'{folder.lower()}', 'True')

    def on_allow__flatpak_data_clicked(self):
        if self.options_ui.allow_flatpak_data_checkBox.isChecked():
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'True')
        else:
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'False')

    def on_button_fix_clicked(self):
        reset_confirmation = QMessageBox.question(
            self,
            'Reset All Settings',
            'Are you sure you want to reset all settings?',
            QMessageBox.No | QMessageBox.Yes,
            QMessageBox.No) 

        if reset_confirmation == QMessageBox.Yes:
            MAIN.ui.last_backup_label.setText("Last Backup:")
            MAIN.ui.next_backup_label.setText("Next Backup:")
            
            # Reset settings
            # Backup section
            MAIN_INI_FILE.set_database_value('STATUS', 'unfinished_backup', 'No')
            # MAIN_INI_FILE.set_database_value('STATUS', 'automatically_backup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'backing_up_now', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'first_startup', 'False')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_names', 'True')
            MAIN_INI_FILE.set_database_value('STATUS', 'allow_flatpak_data', 'False')
            # MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')

            # INFO
            MAIN_INI_FILE.set_database_value('INFO', 'latest_backup_date', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'oldest_backup_date', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'latest_backup_to_main', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'latest_backup_time_check', 'None')

            # EXTERNAL  
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'hd', 'None')
            MAIN_INI_FILE.set_database_value('EXTERNAL', 'name', 'None')
            
            # SYSTEMTRAY 
            MAIN_INI_FILE.set_database_value('SYSTEMTRAY', 'system_tray', 'False')
            
            MAIN_INI_FILE.set_database_value('INFO', 'language', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'os', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'packageManager', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'theme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'icon', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'cursor', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'colortheme', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'saved_notification', 'None')
            MAIN_INI_FILE.set_database_value('INFO', 'current_backing_up', 'None')
            
            # Remove all keys first
            # Connect to the SQLite database
            conn = sqlite3.connect(SRC_USER_CONFIG_DB)
            cursor = conn.cursor()

            # Execute the DELETE statement to remove all rows from a table
            table_name = 'FOLDER'
            cursor.execute(f"DELETE FROM {table_name}")

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            MAIN_INI_FILE.set_database_value('FOLDER', 'pictures', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'documents', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'music', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'videos', 'True')
            MAIN_INI_FILE.set_database_value('FOLDER', 'desktop', 'True')

            # Hide
            MAIN.ui.frame_1.hide()
            MAIN.ui.frame_2.hide()

            print("All settings was reset!")

            # Re-open Main Windows
            sub.Popen(['python3', SRC_MAIN_WINDOW_PY])

            # Quit
            exit()
        else:
            QMessageBox.Close

    def on_automatically_checkbox_clicked(self):
        if self.options_ui.automatically_backup_checkbox.isChecked():
            # Create backup checker .desktop and move it to the destination
            create_backup_checker_desktop()

            # Copy backup_check.desktop
            shutil.copy(DST_BACKUP_CHECK_DESKTOP, DST_AUTOSTART_LOCATION)

            MAIN_INI_FILE.set_database_value(
                'STATUS', 'automatically_backup', 'True')

            # call backup check
            sub.Popen(
                ['python3', SRC_BACKUP_CHECKER_PY],
                stdout=sub.PIPE, 
                stderr=sub.PIPE)
            
            print("Auto backup was successfully activated!")
        else:
            # Remove autostart.desktop
            os.remove(DST_AUTOSTART_LOCATION)

            MAIN_INI_FILE.set_database_value(
                'STATUS', 'automatically_backup', 'False')

            print("Auto backup was successfully deactivated!")
   
    def on_system_tray_checkbox_clicked(self):
        if self.options_ui.show_in_system_tray_checkbox.isChecked():
            MAIN_INI_FILE.set_database_value(
                'SYSTEMTRAY', 'system_tray', 'True')

            # Call system tray
            sub.Popen(['python3', SRC_SYSTEM_TRAY_PY])

            print("System tray was successfully enabled!")

        else:
            MAIN_INI_FILE.set_database_value(
                'SYSTEMTRAY', 'system_tray', 'False')

            print("System tray was successfully disabled!")
    
    def on_allow_browser_in_time_machine_clicked(self):
        if self.options_ui.allow_browser_in_time_machine.isChecked():
            MAIN_INI_FILE.set_database_value(
                'INFO', 'allow_browser_in_time_machine', 'True')
            print("Showing Browser In Time Machine")

        else:
            MAIN_INI_FILE.set_database_value(
                'INFO', 'allow_browser_in_time_machine', 'False')
            print("Hiding Browser In Time Machine")
                 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Main window
    MAIN = MainWindow()
    MAIN_PREPARE = PREPAREBACKUP()

    # Window icon
    MAIN.setWindowIcon(QIcon(SRC_BACKUP_ICON))

    # Options window
    options_window_class = OptionsWindow()
    options_window_class.setWindowTitle('Settings')

    MAIN.show()

    sys.exit(app.exec())
