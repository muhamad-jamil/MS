#! /usr/bin/env python3
from zoneinfo import available_timezones
from setup import *

# QTimer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle(appName)
        self.setWindowIcon(QIcon(src_restore_icon))
        self.setFixedSize(700, 450)

        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.widgets()

    def widgets(self):
        ################################################################################
        # Left Widget
        ################################################################################
        self.leftWidget = QWidget(self)
        self.leftWidget.setGeometry(20, 20, 200, 410)
        self.leftWidget.setStyleSheet("""
            border-right: 1px solid rgb(68, 69, 70);
        """)

        # Left widget
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(20)

        # Backup images
        self.backupImageLabel = QLabel()
        self.backupImageLabel.setFixedSize(128, 128)
        self.backupImageLabel.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_backup_icon});"
            "border-color: transparent;"
            "}")

        # Automatically checkbox
        self.automaticallyCheckBox = QCheckBox()
        self.automaticallyCheckBox.setFont(item)
        self.automaticallyCheckBox.setText("Back Up Automatically")
        self.automaticallyCheckBox.setFixedSize(175, 20)
        self.automaticallyCheckBox.setStyleSheet("""
            border-color: transparent;
        """)
        self.automaticallyCheckBox.clicked.connect(self.automatically_clicked)

        ################################################################################
        # Right Widget
        ################################################################################
        self.rightWidget = QWidget(self)
        self.rightWidget.setGeometry(240, 40, 170, 154)
        # self.rightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right widget
        self.rightLayout = QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(20)

        # Restore images
        self.restoreImageLabel = QLabel()
        self.restoreImageLabel.setFixedSize(84, 84)
        self.restoreImageLabel.setStyleSheet(
            "QLabel"
            "{"
            f"background-image: url({src_restore_icon});"
            "background-repeat: no-repeat;"
            "}")

        # Select disk button
        self.selectDiskButton = QPushButton(self)
        self.selectDiskButton.setFont(item)
        self.selectDiskButton.setText("Select Backup Disk...")
        self.selectDiskButton.setFixedSize(150, 28)
        self.selectDiskButton.clicked.connect(self.select_external_clicked)

        ################################################################################
        # Far right Widget
        ################################################################################
        self.farRightWidget = QWidget(self)
        self.farRightWidget.setContentsMargins(0, 0, 0, 0)
        self.farRightWidget.setGeometry(412, 40, 280, 120)
        # self.farRightWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Right widget
        self.farRightLayout = QVBoxLayout(self.farRightWidget)
        self.farRightLayout.setSpacing(0)

        ################################################################################
        # Set external name
        ################################################################################
        self.externalNameLabel = QLabel()
        self.externalNameLabel.setFont(bigTitle)
        self.externalNameLabel.setFixedSize(350, 80)
        self.externalNameLabel.setAlignment(QtCore.Qt.AlignLeft)

        ################################################################################
        # Get external size
        ################################################################################
        self.externalSizeLabel = QLabel()
        self.externalSizeLabel.setFont(item)
        self.externalSizeLabel.setFixedSize(200, 18)

        ################################################################################
        # Label last backup
        ################################################################################
        self.lastBackupLabel = QLabel()
        self.lastBackupLabel.setFont(item)
        self.lastBackupLabel.setText("Last Backup: None")
        self.lastBackupLabel.setFixedSize(200, 18)

        # Label last backup
        self.nextBackupLabel = QLabel()
        self.nextBackupLabel.setFont(item)
        self.nextBackupLabel.setText("Next Backup: None")
        self.nextBackupLabel.setFixedSize(250, 18)

        # Status external hd
        self.externalStatusLabel = QLabel()
        self.externalStatusLabel.setFont(QFont('DejaVu Sans', 10))
        self.externalStatusLabel.setText("External HD:")
        self.externalStatusLabel.setFixedSize(200, 18)

        ################################################################################
        # Gif for preparing backup
        ################################################################################
        self.gif = QLabel(self)
        self.gif.move(420, 154)
        self.gif.setStyleSheet(
            "QLabel"
            "{"
            "background-color: transparent;"
            "border: 0px;"
            "}")

        # Set qmovie as gif
        self.movie = QMovie(src_loadingGif)
        self.movie.setScaledSize(QSize().scaled(22, 22, Qt.KeepAspectRatio))
        self.gif.setMovie(self.movie)

        ################################################################################
        # Backup now button
        ################################################################################
        self.backupNowButton = QPushButton(self)
        self.backupNowButton.setText("Back Up Now")
        self.backupNowButton.setFixedSize(100, 28)
        self.backupNowButton.move(420, 155)
        self.backupNowButton.clicked.connect(self.backup_now_clicked)
        self.backupNowButton.hide()

        ################################################################################
        # Description
        ################################################################################
        self.descriptionWidget = QWidget(self)
        self.descriptionWidget.setGeometry(240, 200, 440, 140)
        self.descriptionWidget.setStyleSheet("""
            border-top: 1px solid rgb(68, 69, 70);
        """)

        # Description Layout
        self.descriptionLayout = QVBoxLayout(self.descriptionWidget)

        # Description Title
        self.descriptionTitle = QLabel()
        self.descriptionTitle.setFont(topicTitle)
        self.descriptionTitle.setText(f"{appName} is able to:\n\n")
        self.descriptionTitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.descriptionTitle.setFixedSize(420, 24)
        self.descriptionTitle.setStyleSheet("""
            border-color: transparent;
        """)

        # Description Text
        self.descriptionText = QLabel()
        self.descriptionText.setFont(item)
        self.descriptionText.setText(
            "* Keep local snapshots as space permits\n"
            "* Schedule backups (Minutely, Hourly or Daily)\n"
            f"* Automatically back up at first PC boot, if backup time\n   has passed.\n\n"
            "Delete the oldest backups when your disk becomes full.\n")
        self.descriptionText.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.descriptionText.setFixedSize(420, 120)
        self.descriptionText.setStyleSheet("""
            border-color: transparent;
        """)

        ################################################################################
        # Donate and Settings buttons
        ################################################################################
        self.optionsWidget = QWidget(self)
        self.optionsWidget.setGeometry(340, 380, 350, 80)
        # self.optionsWidget.setStyleSheet("""
        #     border: 1px solid red;
        # """)

        # Options Layout
        self.optionsLayout = QHBoxLayout(self.optionsWidget)
        self.optionsLayout.setSpacing(10)

        # Options button
        self.optionsButton = QPushButton()
        self.optionsButton.setText("Options...")
        self.optionsButton.setFont(item)
        self.optionsButton.setFixedSize(80, 28)
        self.optionsButton.clicked.connect(self.options_clicked)

        # Show system tray
        self.showInSystemTrayCheckBox = QCheckBox(self)
        self.showInSystemTrayCheckBox.setFont(item)
        self.showInSystemTrayCheckBox.setText(f"Show {appName} in system tray")
        self.showInSystemTrayCheckBox.setFixedSize(280, 20)
        self.showInSystemTrayCheckBox.move(240, 410)
        self.showInSystemTrayCheckBox.setStyleSheet("""
            border-color: transparent;
        """)
        self.showInSystemTrayCheckBox.clicked.connect(self.system_tray_clicked)

        ################################################################################
        # Add widgets and Layouts
        ################################################################################
        # Left Layout
        self.leftLayout.addWidget(self.backupImageLabel, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.leftLayout.addWidget(self.automaticallyCheckBox, 1, Qt.AlignHCenter | Qt.AlignTop)

        #  Right Layout
        self.rightLayout.addWidget(self.restoreImageLabel, 0, Qt.AlignVCenter | Qt.AlignHCenter)
        self.rightLayout.addWidget(self.selectDiskButton, 1, Qt.AlignVCenter | Qt.AlignHCenter)

        #  Far Right Layout
        self.farRightLayout.addWidget(self.externalNameLabel, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.externalSizeLabel, 0, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.lastBackupLabel, 1, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.nextBackupLabel, 2, Qt.AlignLeft | Qt.AlignTop)
        self.farRightLayout.addWidget(self.externalStatusLabel, 3, Qt.AlignLeft | Qt.AlignTop)

        # Description Layout
        self.descriptionLayout.addWidget(self.descriptionTitle, 0, Qt.AlignVCenter | Qt.AlignLeft)
        self.descriptionLayout.addWidget(self.descriptionText, 0, Qt.AlignVCenter | Qt.AlignLeft)

        #  Options layout
        self.optionsLayout.addWidget(self.optionsButton, 0, Qt.AlignRight | Qt.AlignVCenter)

        # Set Layouts
        self.setLayout(self.leftLayout)

        # Update
        timer.timeout.connect(self.read_ini_file)
        timer.start(1000)
        self.read_ini_file()

    def read_ini_file(self):
        try:
            ################################################################################
            # Read INI file
            ################################################################################
            config = configparser.ConfigParser()
            config.read(src_user_config)

            # Get current hour, minutes
            now = datetime.now()
            self.dayName = now.strftime("%a")
            self.currentHour = now.strftime("%H")
            self.currentMinute = now.strftime("%M")

            # INI file
            self.iniHDName = config['EXTERNAL']['name']
            self.iniExternalLocation = config['EXTERNAL']['hd']
            self.iniBackupNow = config['BACKUP']['backup_now']
            self.iniAutomaticallyBackup = config['BACKUP']['auto_backup']
            self.iniSystemTray = config['SYSTEMTRAY']['system_tray']
            self.iniLastBackup = config['INFO']['latest']
            self.iniNextBackup = config['INFO']['next']
            self.iniNotification = config['INFO']['notification']
            self.moreTimeMode = config['MODE']['more_time_mode']

            # Dates
            self.nextDay = "None"
            self.iniNextHour = config['SCHEDULE']['hours']
            self.iniNextMinute = config['SCHEDULE']['minutes']
            self.iniNextBackupSun = config['SCHEDULE']['sun']
            self.iniNextBackupMon = config['SCHEDULE']['mon']
            self.iniNextBackupTue = config['SCHEDULE']['tue']
            self.iniNextBackupWed = config['SCHEDULE']['wed']
            self.iniNextBackupThu = config['SCHEDULE']['thu']
            self.iniNextBackupFri = config['SCHEDULE']['fri']
            self.iniNextBackupSat = config['SCHEDULE']['sat']
            self.everytime = config['SCHEDULE']['everytime']

            self.currentTime = self.currentHour + self.currentMinute
            self.backupTime = self.iniNextHour + self.iniNextMinute

        except KeyError:
            print("Error trying to read user.ini!")
            exit()

        self.check_connection_media()

    def check_connection_media(self):
        ################################################################################
        # External availability
        ################################################################################
        try:
            os.listdir(f"/media/{userName}/{self.iniHDName}")  # Check if external can be found
            self.set_external_status()

        except FileNotFoundError:
            self.check_connection_run()

    def check_connection_run(self):
        ################################################################################
        # External availability
        ################################################################################
        try:
            os.listdir(f"/run/media/{userName}/{self.iniHDName}")  # Opensuse, external is inside "/run"
            self.set_external_status()

        except FileNotFoundError:
            # Hide backup now button
            self.backupNowButton.hide()
            # External status
            self.externalStatusLabel.setText("External HD: Disconnected")
            self.externalStatusLabel.setStyleSheet('color: red')
            self.externalStatusLabel.setAlignment(QtCore.Qt.AlignTop)
            # External size
            self.externalSizeLabel.setText("No information available")

        self.set_external_name()

    def set_external_status(self):
        ################################################################################
        # External status
        ################################################################################
        self.externalStatusLabel.setText("External HD: Connected")
        self.externalStatusLabel.setStyleSheet('color: green')

        self.get_size_informations()

    def get_size_informations(self):
        ################################################################################
        # Get external size values
        ################################################################################
        try:
            # Get external max size
            externalMaxSize = os.popen(f"df --output=size -h {self.iniExternalLocation}")
            externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace("Size", "").replace(
                "\n", "").replace(" ", "")
            externalMaxSize = str(externalMaxSize)

            # Get external usded size
            usedSpace = os.popen(f"df --output=used -h {self.iniExternalLocation}")
            usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace("Used", "").replace(
                "\n", "").replace(" ", "")
            usedSpace = str(usedSpace)

            self.externalSizeLabel.setText(f"{usedSpace} of {externalMaxSize} available")

        except:
            self.externalSizeLabel.setText("No information available")

        self.condition()

    def condition(self):
        ################################################################################
        # Set external name label from INI file if != "None"
        ################################################################################
        if self.iniHDName != "None":  # If location can be found
            ################################################################################
            # If is not backing up right now
            ################################################################################
            if self.iniBackupNow == "false":
                # Hide loading gif
                self.movie.stop()
                # Backup Now
                self.backupNowButton.setEnabled(True)  # Disable backup now button
                self.backupNowButton.setFixedSize(120, 28)  # Resize backup button
                self.backupNowButton.show()

            else:
                # Show loading gif
                self.movie.start()
                # Hide backup now button
                self.backupNowButton.hide()

        else:
            # Set external name
            self.externalNameLabel.setText("None")
            # Hide backup now button
            self.backupNowButton.hide()

        self.set_external_name()

    def set_external_name(self):
        self.externalNameLabel.setText(self.iniHDName)

        self.set_external_last_backup()

    def set_external_last_backup(self):
        ################################################################################
        # Last backup label
        ################################################################################
        if self.iniLastBackup != "":
            self.lastBackupLabel.setText(f"Last Backup: {self.iniLastBackup}")

        self.set_external_next_backup()

    def set_external_next_backup(self):
        ################################################################################
        # Next backup label
        ################################################################################
        if self.iniNextBackup != "":
            self.nextBackupLabel.setText(f"Next Backup: {self.iniNextBackup}")

        # If automaticallyCheckBox is unchecked == AUtomatic backups off
        if not self.automaticallyCheckBox.isChecked():
            self.nextBackupLabel.setText("Next Backup: Automatic backups off")

        else:
            self.nextBackupLabel.setText(f"Next Backup: {self.iniNextBackup}")

        ################################################################################
        # Next backup multiple times per day
        ################################################################################
        if self.moreTimeMode == "true" and self.everytime == "30":
            self.nextBackupLabel.setText("Next Backup: Every 30 minutes")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        elif self.moreTimeMode == "true" and self.everytime == "60":
            self.nextBackupLabel.setText("Next Backup: Every 1 hour")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        elif self.moreTimeMode == "true" and self.everytime == "120":
            self.nextBackupLabel.setText("Next Backup: Every 2 hours")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        elif self.moreTimeMode == "true" and self.everytime == "240":
            self.nextBackupLabel.setText("Next Backup: Every 4 hours")
            self.nextBackupLabel.setFont(QFont('DejaVu Sans', 10))

        ################################################################################
        # Days to run
        ################################################################################
        if self.dayName == "Sun":
            if self.iniNextBackupSun == "true" and self.currentHour <= self.iniNextHour and self.currentMinute <= self.iniNextMinute:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"

        if self.dayName == "Mon":
            if self.iniNextBackupMon == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"

        if self.dayName == "Tue":
            if self.iniNextBackupTue == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"

        if self.dayName == "Wed":
            if self.iniNextBackupWed == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"

        if self.dayName == "Thu":
            if self.iniNextBackupThu == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"

        if self.dayName == "Fri":
            if self.iniNextBackupFri == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"
                elif self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"

        if self.dayName == "Sat":
            if self.iniNextBackupSat == "true" and self.currentTime < self.backupTime:
                self.nextDay = "Today"
            else:
                if self.iniNextBackupSun == "true":
                    self.nextDay = "Sun"
                elif self.iniNextBackupMon == "true":
                    self.nextDay = "Mon"
                elif self.iniNextBackupTue == "true":
                    self.nextDay = "Tue"
                elif self.iniNextBackupWed == "true":
                    self.nextDay = "Wed"
                elif self.iniNextBackupThu == "true":
                    self.nextDay = "Thu"
                elif self.iniNextBackupFri == "true":
                    self.nextDay = "Fri"
                elif self.iniNextBackupSat == "true":
                    self.nextDay = "Sat"

        ################################################################################
        # Save next backup to user.ini
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set('INFO', 'next', f'{self.nextDay}, {self.iniNextHour}:{self.iniNextMinute}')
            config.write(configfile)

        ################################################################################
        # Print current time and day
        ################################################################################
        print("")
        print(f"Current time: {self.currentHour}:{self.currentMinute}")
        print(f"Today is: {self.dayName}")
        print("")

        self.is_auto_backup_enabled()

    def is_auto_backup_enabled(self):
        ################################################################################
        # Auto backup
        ################################################################################
        if self.iniAutomaticallyBackup == "true":
            self.automaticallyCheckBox.setChecked(True)

        else:
            self.automaticallyCheckBox.setChecked(False)

        self.system_tray()

    def system_tray(self):
        ################################################################################
        # System tray
        ################################################################################
        if self.iniSystemTray == "true":
            self.showInSystemTrayCheckBox.setChecked(True)

        else:
            self.showInSystemTrayCheckBox.setChecked(False)

    def automatically_clicked(self):
        ################################################################################
        # Copy .desktop to user folder (Autostart .desktop)
        ################################################################################
        if self.automaticallyCheckBox.isChecked():
            # If .desktop has not already been copied
            if not os.path.exists(src_backup_check_desktop):
                shutil.copy(src_backup_check, src_backup_check_desktop)  # Copy to /home/#USER/.config/autostart
            
            ################################################################################
            # Set auto backup to true if external has choosen already
            ################################################################################
            if self.iniHDName != "None":
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:  # Set auto backup to true
                    config.set('BACKUP', 'auto_backup', 'true')
                    config.write(configfile)

                ################################################################################
                # Call backup check if self.iniName != "None"
                ################################################################################
                print("Auto backup was successfully activated!")
                sub.Popen(f"python3 {src_backup_check_py}", shell=True)

            else:
                ################################################################################
                # Set notification_id to 3
                ################################################################################
                config = configparser.ConfigParser()
                config.read(src_user_config)
                with open(src_user_config, 'w') as configfile:  # Set auto backup to true
                    config.set('INFO', 'notification_id', '3')
                    config.write(configfile)

                # If user has allow app to send notifications
                if self.iniNotification == "true":
                    sub.Popen(f"python3 {src_notification}", shell=True)

        else:
            config = configparser.ConfigParser()
            config.read(src_user_config)
            with open(src_user_config, 'w') as configfile:
                config.set('BACKUP', 'auto_backup', 'false')
                config.set('BACKUP', 'checker_running', 'false')
                config.write(configfile)

            print("Auto backup was successfully deactivated!")


    def system_tray_clicked(self):
        ################################################################################
        # System tray enabled
        ################################################################################
        ################################################################################
        # Write to ini file
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:  # Set auto backup to true
            if self.showInSystemTrayCheckBox.isChecked():
                config.set('SYSTEMTRAY', 'system_tray', 'true')
                config.write(configfile)
                print("System tray was successfully enabled!")

            else:

                config.set('SYSTEMTRAY', 'system_tray', 'false')
                config.write(configfile)
                print("System tray was successfully disabled!")

        ################################################################################
        # Call backup check py
        ################################################################################
        sub.Popen(f"python3 {src_system_tray}", shell=True)

    def select_external_clicked(self):
        # Choose external hd
        self.setEnabled(False)
        externalMain.show()  # Show Choose external:

    def backup_now_clicked(self):
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile: # Set backup now to true
            config.set('BACKUP', 'backup_now', 'true')
            config.write(configfile)

        # Call backup now py
        sub.Popen(f"python3 {src_backup_now}", shell=True)

    def options_clicked(self):
        # Call schedule
        sub.run(f"python3 {src_options_py}", shell=True)


################################################################################
# Show external option to back up
################################################################################
class EXTERNAL(QWidget):
    def __init__(self):
        super(EXTERNAL, self).__init__()
        # Media location
        self.foundInMedia = None
        self.media = "/media"
        self.run = "/run/media"

        self.iniUI()

    def iniUI(self):
        self.setWindowIcon(QIcon(src_restore_icon))
        self.setWindowTitle("Choose external:")
        self.setFixedSize(500, 380)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        ################################################################################
        # Center window
        ################################################################################
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())

        self.widgets()

    def widgets(self):
        ################################################################################
        # Frame
        ################################################################################
        self.whereFrame = QFrame(self)
        self.whereFrame.setFixedSize(460, 280)
        self.whereFrame.move(20, 40)
        self.whereFrame.setStyleSheet("""
            background-color: rgb(48, 49, 50);
        """)

        # Backup images
        self.cancelButton = QPushButton(self)
        self.cancelButton.setFont(item)
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFixedSize(80, 28)
        self.cancelButton.move(400, 340)
        self.cancelButton.clicked.connect(self.on_button_cancel_clicked)

        self.check_connection_media()

    def check_connection_media(self):
        ################################################################################
        # Search external inside media
        ################################################################################
        try:
            os.listdir(f'{self.media}/{userName}')
            self.foundInMedia = True
            self.show_one_screen()

        except FileNotFoundError:
            self.check_connection_run()

    def check_connection_run(self):
        ################################################################################
        # Search external inside run/media
        ################################################################################
        try:
            os.listdir(f'{self.run}/{userName}')  # Opensuse, external is inside "/run"
            self.foundInMedia = False
            self.show_one_screen()

        except FileNotFoundError:
            print("No external devices mounted or available...")
            pass

    def show_one_screen(self):
        ################################################################################
        # Check source
        ################################################################################
        if self.foundInMedia:
            self.foundWhere = self.media
        else:
            self.foundWhere = self.run

        ################################################################################
        # Add buttons and images for each external
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)

        vertical = 20
        verticalImg = 52
        for output in os.listdir(f'{self.foundWhere}/{userName}'):
            image = QLabel(self)
            pixmap = QPixmap(src_restore_small_icon)
            image.setPixmap(pixmap)
            image.setFixedSize(48, 48)
            image.move(30, verticalImg)
            verticalImg += 50

            # Avaliables external devices
            availableDevices = QPushButton(output, self.whereFrame)
            availableDevices.setFixedSize(380, 30)
            availableDevices.move(60, vertical)
            availableDevices.setFont(item)
            availableDevices.setCheckable(True)
            text = availableDevices.text()
            availableDevices.setStyleSheet("""
                color: white;
            """)

            ################################################################################
            # Auto checked this choosed external device
            ################################################################################
            if text == main.iniHDName:
                availableDevices.setChecked(True)

            vertical += 50
            availableDevices.show()
            availableDevices.clicked.connect(lambda *args, text=text: self.on_button_clicked(text))

    def on_button_clicked(self, get):
        ################################################################################
        # Adapt external name is it has space in the name
        ################################################################################
        if " " in get:
            get = str(get.replace(" ", "\ "))

        ################################################################################
        # Write changes to ini
        ################################################################################
        config = configparser.ConfigParser()
        config.read(src_user_config)
        with open(src_user_config, 'w') as configfile:
            config.set(f'EXTERNAL', 'hd', f'{self.foundWhere}/{userName}/{get}')
            config.set('EXTERNAL', 'name', get)
            config.write(configfile)

        self.close()
        main.setEnabled(True)

    def on_button_cancel_clicked(self):
        externalMain.close()
        main.setEnabled(True)


app = QApplication(sys.argv)
tic = time.time()
main = UI()
main.show()
externalMain = EXTERNAL()
toc = time.time()
print(f'{appName} {(toc - tic):.4f} seconds')
app.exit(app.exec())
