from setup import *

# Configparser
config = configparser.ConfigParser()
config.read(src_user_config)

# Timer
timer = QtCore.QTimer()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        loadUi(src_ui_options, self)
        self.setWindowTitle("Options Screen")
        appIcon = QIcon(src_restore_icon)
        self.setWindowIcon(appIcon)
        self.setFixedHeight(550)
        self.setFixedWidth(800)

        # Connections
        self.check_desktop.clicked.connect(self.on_check_desktop_checked)
        self.check_downloads.clicked.connect(self.on_check_downloads_checked)
        self.check_documents.clicked.connect(self.on_check_documents_checked)
        self.check_music.clicked.connect(self.on_check_music_checked)
        self.check_pictures.clicked.connect(self.on_check_pictures_checked)
        self.check_videos.clicked.connect(self.on_check_videos_checked)
        self.label_hours.valueChanged.connect(self.label_hours_changed)
        self.label_minutes.valueChanged.connect(self.label_minutes_changed)
        self.one_time_mode.clicked.connect(self.on_frequency_clicked)
        self.more_time_mode.clicked.connect(self.on_frequency_clicked)
        self.every_combox.currentIndexChanged.connect(self.on_every_combox_changed)
        self.button_save.clicked.connect(self.on_buttons_save_clicked)

        # Get user.ini
        read_desktop = config['FOLDER']['desktop']
        read_downloads = config['FOLDER']['downloads']
        read_documents = config['FOLDER']['documents']
        read_music = config['FOLDER']['music']
        read_pictures = config['FOLDER']['pictures']
        read_videos = config['FOLDER']['videos']

        sun = config['SCHEDULE']['sun']
        mon = config['SCHEDULE']['mon']
        tue = config['SCHEDULE']['tue']
        wed = config['SCHEDULE']['wed']
        thu = config['SCHEDULE']['thu']
        fri = config['SCHEDULE']['fri']
        sat = config['SCHEDULE']['sat']

        get_everytime = config['SCHEDULE']['everytime']

        # Schedule options
        # Hours
        hrs = int(config['SCHEDULE']['hours'])
        self.label_hours.setValue(hrs)

        # Minutes
        min = int(config['SCHEDULE']['minutes'])
        self.label_minutes.setValue(min)

        # Read folders
        if read_desktop == "true":
            self.check_desktop.setChecked(True)

        if read_downloads == "true":
            self.check_downloads.setChecked(True)

        if read_documents == "true":
            self.check_documents.setChecked(True)

        if read_music == "true":
            self.check_music.setChecked(True)

        if read_pictures == "true":
            self.check_pictures.setChecked(True)

        if read_videos == "true":
            self.check_videos.setChecked(True)

        # # MORE FOLDERS
        # vertical_checkbox = 210
        # vertical_label = 170
        # for self.files in (get_home_folders):
        #     if not self.files.startswith("."):
        #         if not self.files in ["Desktop", "Documents", "Downloads", "Music", "Videos", "Pictures"]:
        #             label_text = QLabel(self.files, self.folders_frame)
        #             label_text.setFixedSize(200, 22)
        #             label_text.move(35, vertical_label)
        #             vertical_label = vertical_label + 22
        #
        #             folders_checkbox = QCheckBox(self)
        #             folders_checkbox.setFixedSize(200, 22)
        #             folders_checkbox.move(32, vertical_checkbox)
        #             vertical_checkbox = vertical_checkbox + 22
        #             self.text = label_text.text()
        #             folders_checkbox.show()
        #             folders_checkbox.clicked.connect(lambda ch, text=self.text: print(text))
        #             folders_checkbox.clicked.connect(lambda ch, text=self.text: self.here(text))

        if sun == "true":
            self.check_sun.setChecked(True)

        if mon == "true":
            self.check_mon.setChecked(True)

        if tue == "true":
            self.check_tue.setChecked(True)

        if wed == "true":
            self.check_wed.setChecked(True)

        if thu == "true":
            self.check_thu.setChecked(True)

        if fri == "true":
            self.check_fri.setChecked(True)

        if sat == "true":
            self.check_sat.setChecked(True)

        # Everytime
        if get_everytime == "15":
            self.every_combox.setCurrentIndex(0)

        elif get_everytime == "30":
            self.every_combox.setCurrentIndex(1)

        elif get_everytime == "60":
            self.every_combox.setCurrentIndex(2)

        elif get_everytime == "120":
            self.every_combox.setCurrentIndex(3)

        elif get_everytime == "240":
            self.every_combox.setCurrentIndex(4)

        # Timer
        timer.timeout.connect(self.updates)
        timer.start(500)  # update every second
        self.updates()

    def updates(self):
        # Configparser
        config = configparser.ConfigParser()
        config.read(src_user_config)

        # Frequency check
        one_time_mode = config['MODE']['one_time_mode']
        more_time_mode = config['MODE']['more_time_mode']

        if one_time_mode == "true":
            self.every_combox.setEnabled(False)
            self.label_hours.setEnabled(True)
            self.label_minutes.setEnabled(True)
            self.one_time_mode.setChecked(True)

        if more_time_mode == "true":
            self.label_hours.setEnabled(False)
            self.label_minutes.setEnabled(False)
            self.every_combox.setEnabled(True)
            self.more_time_mode.setChecked(True)

    def on_every_combox_changed(self):
        choose_every_combox = self.every_combox.currentIndex()
        with open(src_user_config, 'w') as configfile:
            if choose_every_combox == 0:
                config.set('SCHEDULE', 'everytime', '15')
                config.write(configfile)

            elif choose_every_combox == 1:
                config.set('SCHEDULE', 'everytime', '30')
                config.write(configfile)

            elif choose_every_combox == 2:
                config.set('SCHEDULE', 'everytime', '60')
                config.write(configfile)

            elif choose_every_combox == 3:
                config.set('SCHEDULE', 'everytime', '120')
                config.write(configfile)

            elif choose_every_combox == 4:
                config.set('SCHEDULE', 'everytime', '240')
                config.write(configfile)

    def on_check_desktop_checked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_desktop.isChecked():
                config.set('FOLDER', 'desktop', 'true')
            else:
                config.set('FOLDER', 'desktop', 'false')

            config.write(configfile)

    def on_check_downloads_checked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_downloads.isChecked():
                config.set('FOLDER', 'downloads', 'true')
            else:
                config.set('FOLDER', 'downloads', 'false')

            config.write(configfile)

    def on_check_documents_checked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_documents.isChecked():
                config.set('FOLDER', 'documents', 'true')
            else:
                config.set('FOLDER', 'documents', 'false')

            config.write(configfile)

    def on_check_music_checked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_music.isChecked():
                config.set('FOLDER', 'music', 'true')
            else:
                config.set('FOLDER', 'music', 'false')

            config.write(configfile)

    def on_check_pictures_checked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_pictures.isChecked():
                config.set('FOLDER', 'pictures', 'true')
            else:
                config.set('FOLDER', 'pictures', 'false')

            config.write(configfile)

    def on_check_videos_checked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_videos.isChecked():
                config.set('FOLDER', 'videos', 'true')
            else:
                config.set('FOLDER', 'videos', 'false')

            config.write(configfile)

    def on_check_sun_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_sun.isChecked():
                config.set('SCHEDULE', 'sun', 'true')
                config.write(configfile)
                print("Sun")
            else:
                config.set('SCHEDULE', 'sun', 'false')
                config.write(configfile)

    def on_check_mon_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_mon.isChecked():
                config.set('SCHEDULE', 'mon', 'true')
                config.write(configfile)
                print("Mon")
            else:
                config.set('SCHEDULE', 'mon', 'false')
                config.write(configfile)

    def on_check_tue_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_tue.isChecked():
                config.set('SCHEDULE', 'tue', 'true')
                config.write(configfile)
                print("Tue")
            else:
                config.set('SCHEDULE', 'tue', 'false')
                config.write(configfile)

    def on_check_wed_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_wed.isChecked():
                config.set('SCHEDULE', 'wed', 'true')
                config.write(configfile)
                print("Wed")
            else:
                config.set('SCHEDULE', 'wed', 'false')
                config.write(configfile)

    def on_check_thu_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_thu.isChecked():
                config.set('SCHEDULE', 'thu', 'true')
                config.write(configfile)
                print("Thu")
            else:
                config.set('SCHEDULE', 'thu', 'false')
                config.write(configfile)

    def on_check_fri_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_fri.isChecked():
                config.set('SCHEDULE', 'fri', 'true')
                config.write(configfile)
                print("Fri")
            else:
                config.set('SCHEDULE', 'fri', 'false')
                config.write(configfile)

    def on_check_sat_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.check_sat.isChecked():
                config.set('SCHEDULE', 'sat', 'true')
                config.write(configfile)
                print("Sat")
            else:
                config.set('SCHEDULE', 'sat', 'false')
                config.write(configfile)

    def label_hours_changed(self):
        hours = self.label_hours.value()
        hours = str(hours)

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'hours', hours)
            if hours in min_fix:
                config.set('SCHEDULE', 'hours', '0' + hours)

            config.write(configfile)

    def label_minutes_changed(self):
        minutes = self.label_minutes.value()
        minutes = str(minutes)

        with open(src_user_config, 'w') as configfile:
            config.set('SCHEDULE', 'minutes', minutes)
            if minutes in min_fix:
                config.set('SCHEDULE', 'minutes', '0' + minutes)

            config.write(configfile)

    def on_frequency_clicked(self):
        with open(src_user_config, 'w') as configfile:
            if self.one_time_mode.isChecked():
                config.set('MODE', 'one_time_mode', 'true')
                print("One time mode selected")

                # DISABLE MORE TIME MODE
                config.set('MODE', 'more_time_mode', 'false')
                print("More time mode disabled")
                config.write(configfile)

            elif self.more_time_mode.isChecked():
                config.set('MODE', 'more_time_mode', 'true')
                print("Multiple time mode selected")

                # DISABLE ONE TIME MODE
                config.set('MODE', 'one_time_mode', 'false')
                print("One time mode disabled")
                config.write(configfile)

    @staticmethod
    def on_buttons_save_clicked():
        sub.Popen("python3 " + src_backup_py, shell=True)   # Call backup py
        exit()


app = QApplication(sys.argv)
main = UI()
main.show()
sys.exit(app.exec())
