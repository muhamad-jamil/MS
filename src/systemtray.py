from setup import *
from stylesheet import *
from check_connection import *
from get_backup_time import *
from get_backup_date import *
from calculate_time_left_to_backup import calculate_time_left_to_backup
from read_ini_file import UPDATEINIFILE
from backup_status import progress_bar_status
import error_catcher

# Handle signal
signal.signal(signal.SIGINT, error_catcher.signal_exit)
signal.signal(signal.SIGTERM, error_catcher.signal_exit)

DELAY_TO_UPDATE = 2000


class APP:
    def __init__(self):
        self.color = str()
        self.iniUI()

    def iniUI(self):
        self.app = QApplication([], stdout=sub.PIPE, stderr=sub.PIPE)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationDisplayName(APP_NAME)
        self.app.setApplicationName(APP_NAME)

        self.widget()

    def widget(self):
        setproctitle.setproctitle(f'{APP_NAME} - System Tray')

        # Tray
        self.tray = QSystemTrayIcon()
        # self.tray.setIcon(QIcon(self.get_system_color()))
        self.tray.setIcon(QIcon(SRC_BACKUP_ICON))
        self.tray.setVisible(True)
        self.tray.activated.connect(self.tray_icon_clicked)

        # Create a menu
        self.menu = QMenu()

        # Ini last backup information
        self.last_backup_information = QAction()
        self.last_backup_information.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.last_backup_information.setEnabled(False)

        self.last_backup_information2 = QAction()
        self.last_backup_information2.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.last_backup_information2.setEnabled(False)

        # Report button
        self.report_button = QAction("See Latest Backup Report")
        self.report_button.triggered.connect(self.open_report)

        # # Error button
        # self.error_button = QAction("🔴 See Logs")
        # self.error_button.triggered.connect(self.open_logs)

        # Backup now button
        self.backup_now_button = QAction("Back Up Now")
        self.backup_now_button.triggered.connect(self.backup_now)

        # Browse Time Machine Backups button
        self.browse_time_machine_backups = QAction(
            "Browse Time Machine Backups")
        self.browse_time_machine_backups.setFont(
            QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.browse_time_machine_backups.triggered.connect(
            self._open_browse_time_machine_backups)

        # Open Time Machine button
        self.open_Time_machine = QAction(f"Open {APP_NAME}")
        self.open_Time_machine.setFont(QFont(MAIN_FONT,BUTTON_FONT_SIZE))
        self.open_Time_machine.triggered.connect(
            lambda: sub.Popen(
                ['python3', SRC_MAIN_WINDOW_PY],
                    stdout=sub.PIPE,
                    stderr=sub.PIPE))

        # Add all to menu
        # self.menu.addAction(self.dummyLine)
        self.menu.addAction(self.last_backup_information)
        self.menu.addAction(self.last_backup_information2)
        self.menu.addAction(self.report_button)
        # self.menu.addAction(self.error_button)
        self.menu.addSeparator()

        self.menu.addAction(self.backup_now_button)
        self.menu.addAction(self.browse_time_machine_backups)
        self.menu.addSeparator()

        self.menu.addAction(self.open_Time_machine)
        self.menu.addSeparator()

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)

        timer.timeout.connect(self.should_be_running)
        timer.start(DELAY_TO_UPDATE)

        self.app.exec()

    def should_be_running(self):
        print('System tray is running....')

        # Check if ini file is locked or not
        if not MAIN_INI_FILE.get_database_value('SYSTEMTRAY', 'system_tray'):
            self.exit()

        self.has_connection()

    def has_connection(self):
        # User has registered a device name
        if MAIN_INI_FILE.hd_hd() is not None:
            # Can device be found?
            if is_connected(MAIN_INI_FILE.hd_hd()):
                # Is backup now running? (chech if file exists)
                self.status_on()
            else:
                if MAIN_INI_FILE.automatically_backup():
                    self.status_off()

        # No backup device registered
        else:
            self.last_backup_information.setText('First, select a backup device.')
            self.last_backup_information2.setText(' ')
            # Backup now button to False
            self.backup_now_button.setEnabled(False)
            # Browser Time Machine button to False
            self.browse_time_machine_backups.setEnabled(False)

        # Experimental features
        if MAIN_INI_FILE.get_database_value('INFO', 'allow_browser_in_time_machine'):
            # Show this feature
            self.browse_time_machine_backups.setVisible(True)
        else:
            # Hide this feature
            self.browse_time_machine_backups.setVisible(False)

    def status_on(self):
        # Frequency modes
        self.informations_label()

        # Has no logs errors
        if not os.path.exists(LOG_LOCATION):
            # Hide this feature
            # self.error_button.setVisible(False)

            # Is not restoring
            if MAIN_INI_FILE.current_restoring():
                self.change_color("Yellow")
                # Disable
                self.backup_now_button.setEnabled(False)
                self.browse_time_machine_backups.setEnabled(False)
            # No backup is been made
            elif not MAIN_INI_FILE.current_backing_up():
                self.change_color("White")

                self.backup_now_button.setEnabled(True)
                self.browse_time_machine_backups.setEnabled(True)
            else:
                # Backing up right now
                self.change_color("Green")
                # Notification information
                self.last_backup_information.setText(MAIN_INI_FILE.get_database_value(
                    'INFO', 'current_backing_up'))
                self.last_backup_information2.setText(progress_bar_status())

                # Disable
                self.backup_now_button.setEnabled(False)
                self.browse_time_machine_backups.setEnabled(False)
        else:
            # Show logs option in system tray
            # self.error_button.setVisible(True)
            # Change system tray color
            self.change_color('Red')
            # Disable backup now
            self.backup_now_button.setEnabled(False)

    def status_off(self):
        # Hide this feature
        # self.error_button.setVisible(False)
        
        # Change color to Red
        self.change_color("Red")
        self.backup_now_button.setEnabled(False)
        self.browse_time_machine_backups.setEnabled(False)

    def informations_label(self):
        # Automatically backup is ON
        if MAIN_INI_FILE.automatically_backup():
            # Show time left only if current minute is higher then x value
            if (59 - int(MAIN_INI_FILE.current_minute())) <= TIME_LEFT_WINDOW:
                self.last_backup_information2.setText(
                    f'{calculate_time_left_to_backup()}\n')
                # Next backup
                self.last_backup_information.setText(
                    (f'Next Backup to "{MAIN_INI_FILE.hd_name()}":'))
            else:
                self.last_backup_information.setText(
                        f'Latest Backup to: "{MAIN_INI_FILE.hd_name()}"')
                # Show latest backup label
                self.last_backup_information2.setText(MAIN_INI_FILE.latest_backup_date())

                # # Show latest backup date
                # if latest_backup_date() is not None:
                #     self.last_backup_information.setText(
                #         f'Latest Backup to: "{MAIN_INI_FILE.hd_name()}"')
                #     self.last_backup_information2.setText(latest_backup_date_label())
                # else:
                #     # Next backup label
                #     self.last_backup_information2.setText(next_backup_label())

        else:
            # Enable backup now action
            self.backup_now_button.setEnabled(True)

            self.last_backup_information.setText(
                    f'Latest Backup to "{MAIN_INI_FILE.hd_name()}:"')

            # Show latest backup label
            self.last_backup_information2.setText(MAIN_INI_FILE.latest_backup_date())

    def _open_browse_time_machine_backups(self):
        try:
            sub.run(
                ['python3', SRC_ENTER_TIME_MACHINE_PY],
                stdout=sub.PIPE,
                stderr=sub.PIPE)
        except Exception as e:
            # Handle or log the exception
            print(f"Error launching subprocess: {e}")

    def backup_now(self):
        # Disable backup now action
        self.backup_now_button.setEnabled(False)

        # try:
        #     sub.Popen(
        #         ['python3', SRC_ANALYSE_PY],
        #             stdout=sub.PIPE,
        #             stderr=sub.PIPE)
        # except Exception as e:
        #     # Save error log
        #     MAIN_INI_FILE.report_error(e)
        try:
            process = sub.Popen(
                ['python3', SRC_ANALYSE_PY],
                stdout=sub.PIPE,
                stderr=sub.PIPE)

            output, error = process.communicate()
            print(output)
            print(error.decode('utf-8'))
            if process.returncode != 0:
                MAIN_INI_FILE.report_error(error.decode('utf-8'))
        except Exception as e:
            print(e)
            MAIN_INI_FILE.report_error(e)
            raise

    def open_report(self):
        report_file_txt = MAIN_INI_FILE.include_to_backup()

        with sub.Popen(
            ['xdg-open', report_file_txt],
            stdout=sub.PIPE,
            stderr=sub.PIPE) as process:
            # You can add further handling of process output if needed
            stdout, stderr = process.communicate()

    def open_logs(self):
        logs_file_txt = LOG_LOCATION

        with sub.Popen(
            ['xdg-open', logs_file_txt],
            stdout=sub.PIPE,
            stderr=sub.PIPE) as process:
            # You can add further handling of process output if needed
            stdout, stderr = process.communicate()

    def change_color(self, color):
        try:
            if self.color != color:
                if color == "Green":
                    self.color=color
                    self.tray.setIcon(QIcon(SRC_SYSTEM_BAR_RUN_ICON))
                elif color == "White":
                    self.color=color
                    self.tray.setIcon(QIcon(SRC_BACKUP_ICON))
                elif color == "Red":
                    self.color=color
                    self.tray.setIcon(QIcon(SRC_SYSTEM_BAR_ERROR_ICON))
                elif color == "Yellow":
                    self.color=color
                    self.tray.setIcon(QIcon(SRC_SYSTEM_BAR_RESTORE_ICON))
        except Exception:
            self.exit()

    def exit(self):
        MAIN_INI_FILE.set_database_value('SYSTEMTRAY', 'system_tray', 'False')

        self.tray.hide()
        exit()

    def tray_icon_clicked(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            self.tray.contextMenu().exec(QCursor.pos())

    def get_system_color(self):
        # print(self.app.palette().windowText().color().getRgb()[0] < 55)
        # Detect dark theme
        if self.app.palette().windowText().color().getRgb()[0] < 55:
            return SRC_SYSTEM_BAR_ICON

        else:
            return SRC_SYSTEM_BAR_WHITE_ICON


MAIN_INI_FILE = UPDATEINIFILE()
main = APP()

