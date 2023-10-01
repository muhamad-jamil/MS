# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py

from ui.ui_untitled import Ui_MainWindow
from setup import *
from read_ini_file import UPDATEINIFILE
from datetime import datetime
from get_latest_backup_date import latest_backup_date_label
from handle_spaces import handle_spaces

MAIN_INI_FILE = UPDATEINIFILE()

TXT_TYPES = [
    "txt", "py", "cpp", "h", "c", "cgi",
    "cs", "class", "java", "php", "sh",
    "swift", "vb", "doc", "docx", "odt",
    "pdf", "rtf", "tex", "wpd"
]

IMAGE_TYPES = [
    "png", "jpg", "jpeg", "webp", "gif", "svg",
    "eps", "pdf", "ai", "raw", "tiff",
    "bmp", "ps", "tif"
]


def size_format(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"

        size_bytes /= 1024.0

def get_full_location(item, column):
    item_txt = item.text(column)
    full_location = item_txt

    parent_item = item.parent()
    while parent_item:
        parent_txt = parent_item.text(column)
        full_location = f"{parent_txt}/{full_location}"
        parent_item = parent_item.parent()

    return full_location

def resize_image(pixmap, max_size):
    if pixmap.width() > max_size or pixmap.height() > max_size:
        pixmap = pixmap.scaled(
            max_size, max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return pixmap

def get_all_backup_folders():
    folders_list = []

    # Connect to the SQLite database
    conn = sqlite3.connect(SRC_USER_CONFIG_DB)
    cursor = conn.cursor()
    # Query all keys from the specified table
    cursor.execute(f"SELECT key FROM FOLDER")
    keys = [row[0] for row in cursor.fetchall()]
    # Close the connection
    conn.close()

    for folder in keys:
        folders_list.append(folder)
        folders_list.sort()

    return folders_list

def btn_cancel_clicked():
    exit()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.folder_already_opened = False

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)  # This ensures exclusive behavior


        self.checked_items = []

        self.ALREADY_CHECKED_FIRST_FOLDER = False

        self.files_to_restore = []
        self.list_of_preview_items = []
        self.LIST_OF_ALL_BACKUP_DATES = []
        self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE = []

        self.INDEX_TIME = 0
        self.COUNTER_FOR_DATE = 0
        self.COUNTER_FOR_TIME = 0

        self.current_location_label = QLabel(self)
        self.CURRENT_FOLDER = ""

        # Connections
        # Up button
        self.ui.btn_up.clicked.connect(self.btn_up_clicked)
        # Down button
        self.ui.btn_down.clicked.connect(self.btn_down_clicked)
        # Cancel button
        self.ui.btn_cancel.clicked.connect(btn_cancel_clicked)
        # Restore button
        self.ui.btn_restore.clicked.connect(self.start_restore)

        # Settings from QTree
        self.ui.tree_widget.setHeaderLabels(["Name", "Date Modified", "Size", "Type"])
        self.ui.tree_widget.setColumnWidth(0, 250)
        self.ui.tree_widget.setColumnWidth(1, 150)
        # self.ui.tree_widget.clicked.connect(self.selected_item_for_preview)
        # self.ui.tree_widget.itemSelectionChanged.connect(self.selected_item_for_preview)
        self.ui.tree_widget.itemChanged.connect(self.qtree_checkbox_clicked)

        # Settings for the preview window
        self.preview_window = None

    def add_backup_folders(self):
        # Get backup folders names
        for folder in get_all_backup_folders():
            print(folder)
            try:
                # Can the folder be found inside Users Home?
                folder = folder.capitalize()
                os.listdir(f"{HOME_USER}/{folder}")

            except FileNotFoundError:
                # Lower folder first letter
                folder = folder.lower()  # Lower folder first letter

            ################################################################################
            # PUSH BUTTON
            ################################################################################
            self.btn_backup_home_folders = QPushButton()
            self.btn_backup_home_folders.setText(folder)
            self.btn_backup_home_folders.setFixedSize(140, 34)
            self.btn_backup_home_folders.setCheckable(True)
            self.btn_backup_home_folders.setAutoExclusive(True)
            self.btn_backup_home_folders.setStyleSheet(
                """
                    QPushButton
                    {
                        padding: 5px 12px 6px 12px;
                        outline: none;
                        font-size: 12px;
                    }
                """)
            self.btn_backup_home_folders.clicked.connect(lambda *args, directory=folder: self.change_directory(directory))
            self.ui.folders_layout.addWidget(self.btn_backup_home_folders)

            # Automatically check the first folder in the list
            if not self.ALREADY_CHECKED_FIRST_FOLDER:
                self.btn_backup_home_folders.setChecked(True)
                # Set as current selected folder
                self.CURRENT_FOLDER = folder
                # Set already checked to True
                self.ALREADY_CHECKED_FIRST_FOLDER = True

        # Add stretch after the last added folder
        self.ui.folders_layout.addStretch()

    def add_backup_dates(self):
        # Show sorted dates folders
        counter = 0
        horizontal = 0
        vertical = 0
        for date in self.LIST_OF_ALL_BACKUP_DATES:
            ################################################################################
            # PUSH BUTTON
            ################################################################################
            # Convert date from 00-00-00 to Xxxxx 00, 000
            date_obj = datetime.strptime(date, "%d-%m-%y")
            formatted_date = date_obj.strftime("%B %d, %Y")

            # Set text to button
            self.btn_backup_date_folders = QPushButton()
            self.btn_backup_date_folders.setText(formatted_date)
            self.btn_backup_date_folders.setMinimumWidth(120)
            self.btn_backup_date_folders.setFixedHeight(28)
            self.btn_backup_date_folders.setCheckable(True)
            # self.btn_backup_date_folders.setAutoExclusive(True)
            self.btn_backup_date_folders.clicked.connect(
                lambda *args, send_date=date: self.change_date(send_date))
            self.btn_backup_date_folders.setStyleSheet(
                """
                    QPushButton
                    {
                        padding: 5px 12px 6px 12px;
                        outline: none;
                        font-size: 12px;
                    }
                """)

            # Add widget to layout
            # self.ui.dates_layout.addWidget(self.btn_backup_date_folders, Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.dates_layout.addWidget(self.btn_backup_date_folders, horizontal, vertical)
            self.button_group.addButton(self.btn_backup_date_folders)
            # self.ui.dates_layout.addWidget(self.btn_backup_date_folders, horizontal, vertical)

            # Limit the number of dates on screen
            horizontal += 1
            counter += 1
            if horizontal == 3:
                vertical += 1
                horizontal = 0

                if counter == 24:
                    break

        """ Check it, so it wont auto check the first in the list
            again after just changing time or folder 
        """
        for index in range(self.ui.dates_layout.count()):
            button = self.ui.dates_layout.itemAt(index).widget()
            if isinstance(button, QPushButton):
                # Check the latest date button found
                button.setChecked(True)
                # Counter for date is iqual to 0, so, the first one
                self.COUNTER_FOR_DATE = self.ui.dates_layout.count() - self.ui.dates_layout.count()
                break
                # Check the last date button found
                # button.setChecked(index == self.ui.dates_layout.count() - 1)
                # Get the new counter for date after new dates changing
                # self.COUNTER_FOR_DATE = self.ui.dates_layout.count() - 1

    def add_backup_times(self):
        try:
            inside_this_date_folder = f"{MAIN_INI_FILE.hd_hd()}/{BASE_FOLDER_NAME}/" \
                                      f"{BACKUP_FOLDER_NAME}/{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/"

            ################################################################################
            # If inside the external "date folders" has not "time folder", pass to avoid display error :D
            ################################################################################
            for time_folder in os.listdir(inside_this_date_folder):
                # Add found "dates time" to the Time list
                self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.append(time_folder)
                # Sort and reverse
                self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.sort(reverse=True)

                # Check if chose time folder exists
                if os.path.exists(
                        f"{MAIN_INI_FILE.hd_hd()}/"
                        f"{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"
                        f"{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/"
                        f"{time_folder}/"):
                    ################################################################################
                    # PUSH BUTTON
                    ################################################################################
                    self.btn_backup_time_folders = QPushButton()
                    self.btn_backup_time_folders.setText(time_folder.replace("-", ":"))
                    # time_folder = time_folder.replace(":", "-")
                    self.btn_backup_time_folders.setFixedSize(100, 34)
                    # self.btn_backup_time_folders.setCheckable(True)
                    # self.btn_backup_time_folders.setAutoExclusive(True)
                    self.btn_backup_time_folders.setStyleSheet(
                        """
                        QPushButton
                        {
                            padding: 5px 12px 6px 12px;
                            outline: none;
                            font-size: 12px;
                        }
                    """)

                # Auto selected the last time option
                self.btn_backup_time_folders.setChecked(True)

        except IndexError:
            # Reset counter for time
            self.COUNTER_FOR_TIME = 0
            # Add 1 for time counter
            self.COUNTER_FOR_TIME += 1

        # Update ui informations 
        self.update_labels()

        # Show results
        #  asynchronously
        self.show_thread = threading.Thread(target=self.show_results)
        self.show_thread.start()

    def show_results(self):
        # Clean previous results
        self.delete_all_results()

        inside_current_folder = f"{MAIN_INI_FILE.hd_hd()}/{BASE_FOLDER_NAME}/" \
                                f"{BACKUP_FOLDER_NAME}/{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/" \
                                f"{self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]}/" \
                                f"{self.CURRENT_FOLDER}"

        # Add options to QTree
        file_list = []
        try:
            for filename in os.listdir(inside_current_folder):
                full_path = os.path.join(inside_current_folder, filename)
                
                # Only include files, skip hidden files
                if os.path.isfile(full_path) and not filename.startswith('.'): 
                    result_size = os.path.getsize(full_path)
                    date_modified = os.path.getmtime(full_path)
                    extension = os.path.splitext(filename)[1]

                    formatted_date = datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S')
                    formatted_size = size_format(result_size) if result_size is not None else ''

                    file_list.append((filename, formatted_date, formatted_size, extension, date_modified))

            # Sort the file list by filename before populating the tree
            file_list.sort(key=lambda x: x[0])

            for item_data in file_list:
                qt_item = QTreeWidgetItem(self.ui.tree_widget, item_data[:-1])
                qt_item.setData(1, Qt.UserRole, item_data[-1])  # Store the timestamp as user data
                qt_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                qt_item.setCheckState(0, Qt.Unchecked)

            self.qtree_add_results(inside_current_folder)

        except FileNotFoundError:
            pass

    def qtree_add_results(self, inside_current_folder):
        for folder_name in os.listdir(inside_current_folder):
            folder_path = os.path.join(inside_current_folder, folder_name)

            if os.path.isdir(folder_path) and not str(folder_name).startswith('.'):
                folder_item = QTreeWidgetItem(self.ui.tree_widget, [folder_name, '', '', 'Folder'])
                # Chekbox for folders
                folder_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                folder_item.setCheckState(0, Qt.Unchecked)
                
                self.qtree_add_sub_items(folder_item, folder_path)

    def qtree_add_sub_items(self, parent_item, folder_path):
        try:
            for item_name in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item_name)
                if os.path.isdir(item_path):
                    # sub_folder_item = QTreeWidgetItem(parent_item, [item_name, '', '', 'Folder'])
                    
                    # Checkbox
                    folder = QTreeWidgetItem(parent_item, [item_name, formatted_date, formatted_size, extension])
                    folder.setData(1, Qt.UserRole, date_modified)  # Store the timestamp as user data
                    folder.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    folder.setCheckState(0, Qt.Unchecked)

                    # TODO
                    # By uncomment this, will add all subfolders and so on, but freezes ui
                    # self.qtree_add_sub_items(sub_folder_item, item_path)
                    
                elif os.path.isfile(item_path) and not item_name.startswith('.'):
                    item_size = os.path.getsize(item_path)
                    date_modified = os.path.getmtime(item_path)
                    extension = os.path.splitext(item_name)[1]

                    formatted_date = datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S')
                    formatted_size = size_format(item_size) if item_size is not None else ''

                    # Checkbox
                    item = QTreeWidgetItem(parent_item, [item_name, formatted_date, formatted_size, extension])
                    item.setData(1, Qt.UserRole, date_modified)  # Store the timestamp as user data
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    item.setCheckState(0, Qt.Unchecked)

        except UnboundLocalError:
            # If folder is empty, change date, until find something
            print("Nothing inside", self.CURRENT_FOLDER, "for", self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE])
            # self.COUNTER_FOR_DATE += 1
            
            for index in range(self.ui.dates_layout.count()):
                button = self.ui.dates_layout.itemAt(index).widget()
                if isinstance(button, QPushButton):
                    # If index match counter for date int
                    if index == self.COUNTER_FOR_DATE:
                        # Check the latest date button found
                        button.setChecked(True)
                        break
        # TODO
        # Needs to reset or update the time gray label, is not
        # self.COUNTER_FOR_TIME = 0
        self.update_labels()

    def up_down_settings(self):
        try:
            # Get index of the current time folder
            self.INDEX_TIME = self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.index(
                self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME])

            ################################################################################
            # DOWN ARROW
            ################################################################################
            # If the first time from the list is checked
            if self.INDEX_TIME == 0:  # 0 = The latest time folder available
                # Disable down arrow, unable to go back from 0
                self.ui.btn_down.setEnabled(False)
            else:
                # Enable down arrow, able to go back from current index
                self.ui.btn_down.setEnabled(True)

            ################################################################################
            # UP ARROW
            ################################################################################
            # If is there more options to choose from the time list
            if self.INDEX_TIME + 1 == len(self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE):
                # Disable up arrow, unable to go forward, there are no more options to choose
                self.ui.btn_up.setEnabled(False)
            else:
                # Enable up arrow, able to go forward, there are more options to choose
                self.ui.btn_up.setEnabled(True)
        except:
            pass

    def update_labels(self):
        # Get current date
        date_now = MAIN_INI_FILE.current_date() + "-" \
                 + MAIN_INI_FILE.current_month() + "-" \
                 + MAIN_INI_FILE.current_year()
        
        # TODO
        # Re-code this
        # replaced_the_time = str(latest_backup_date_label().split(
        #     ",")[0] +  ", " + 
        #     self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]).replace("-",":")


        # date_checker1 = str(self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]).split('-')[0] 
        # date_checker2 = str(self.LIST_OF_ALL_BACKUP_DATES[1]).split('-')[0] 

        # # If today, show "Today"
        # if self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE] != str(date_now):
        #     # Update gray time label
        #     self.ui.label_gray_time.setText(
        #         f'({self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]})'.replace("-", ":"))

        # if self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE] == date_now:
        #     # 
        #     if self.COUNTER_FOR_TIME == 0:
        #         # Today or Yesterday
        #         self.ui.label_gray_time.setText(latest_backup_date_label())
        #     # Edit date, keep text before ",", and update the label time 
        #     else:
        #         self.ui.label_gray_time.setText(replaced_the_time)

        # elif int(date_checker1) - int(date_checker2) == 1:
        #     if self.COUNTER_FOR_TIME == 0:
        #         # Today or Yesterday
        #         self.ui.label_gray_time.setText(latest_backup_date_label())
        #     else:
        #         self.ui.label_gray_time.setText(replaced_the_time)

        # Enable/Disable up, down button
        self.up_down_settings()

    ################################################################################
    # CONNECTIONS
    ################################################################################
    def btn_up_clicked(self):
        self.COUNTER_FOR_TIME += 1

        # Update ui informations
        self.update_labels()

        # Show results asynchronously
        self.show_thread = threading.Thread(target=self.show_results)
        self.show_thread.start()

    def btn_down_clicked(self):
        self.COUNTER_FOR_TIME -= 1
        
        # Update ui informations
        self.update_labels()
        
        # Show results asynchronously
        self.show_thread = threading.Thread(target=self.show_results)
        self.show_thread.start()

    def change_date(self, date):
        # Clean QTree area
        self.delete_all_results()

        # Reset counter for time
        self.COUNTER_FOR_TIME = 0

        # Clear list 0f time folders
        self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.clear()

        # Get new index for counter of dates
        self.COUNTER_FOR_DATE = self.LIST_OF_ALL_BACKUP_DATES.index(date)

        # Add news time folders
        self.add_backup_times()

    def change_directory(self, directory):
        # Clean QTree
        self.ui.tree_widget.clear()

        # Get current folder name
        self.CURRENT_FOLDER = directory

        # Reset counter for time
        self.COUNTER_FOR_TIME = 0

        # Show results asynchronously
        self.show_thread = threading.Thread(target=self.show_results)
        self.show_thread.start()

    def qtree_checkbox_clicked(self, item, column):
        if item.checkState(column) == Qt.Checked:
            # item_txt = item.text(column)
            full_location = get_full_location(item, column)
            # Handle spaces
            # full_location = handle_spaces(full_location)

            print("Full location:", full_location)

            if full_location not in self.files_to_restore:
                # Add if not already in the list
                self.files_to_restore.append(full_location)
            else:
                # Remove from the list
                self.files_to_restore.remove(full_location)

        elif item.checkState(column) == Qt.Unchecked:
            full_location = item.text(column)
            try:
                self.files_to_restore.remove(full_location)
            except ValueError:
                pass
            
        if self.files_to_restore:
            self.show_small_preview(self.files_to_restore[-1])

        else:
            self.ui.small_preview_label.clear()
        
        self.add_to_restore()

    def show_small_preview(self, item_txt):
        # If a file
        if "." in item_txt:
            self.selected_item_extension = str(item_txt).split('.')[-1]
            self.selected_item_full_location = f"{MAIN_INI_FILE.hd_hd()}/" \
                                               f"{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/" \
                                               f"{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/" \
                                               f"{self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]}" \
                                               f"/{self.CURRENT_FOLDER}/{item_txt}"

            # Image
            if self.selected_item_extension in IMAGE_TYPES:
                pixmap = QPixmap(self.selected_item_full_location)
                pixmap = pixmap.scaledToWidth(196, Qt.SmoothTransformation)
                self.ui.small_preview_label.setPixmap(pixmap)

                # Hide ui text
                self.ui.small_preview_text.setFixedHeight(0)
                self.ui.small_preview_text.hide()

                # Expand ui label
                self.ui.small_preview_label.setFixedHeight(222)
                self.ui.small_preview_label.show()

            elif self.selected_item_extension in TXT_TYPES:
                self.read_file(self.selected_item_full_location)

            # Non ok item
            else:
                # Hide ui text
                self.ui.small_preview_text.setFixedHeight(0)
                self.ui.small_preview_text.hide()

                # Hide ui label
                self.ui.small_preview_label.setFixedHeight(0)
                self.ui.small_preview_label.hide()
     
    def read_file(self, file):
        with open(file, "r") as file:
            # Hide ui label
            self.ui.small_preview_label.setFixedHeight(0)
            self.ui.small_preview_label.hide()

            # Expand ui text
            self.ui.small_preview_text.setFixedHeight(222)
            self.ui.small_preview_text.show()

            self.ui.small_preview_text.adjustSize()
            self.ui.small_preview_text.setPlainText(file.read())
            self.ui.small_preview_text.moveCursor(QTextCursor.Start)
            self.ui.small_preview_text.setStyleSheet(
                """
                    font-size: 8px;
                """)

    def add_to_restore(self):
        ################################################################################
        # Enable/Disable functions if item(s) is/are selected
        ################################################################################
        if len(self.files_to_restore)  >= 1:  # If something inside the list
            # If it has at least one item, enable restore button
            self.ui.btn_restore.setEnabled(True)
            # Update restore label
            self.ui.btn_restore.setText(
                f"   Restore({len(self.files_to_restore)})   "
            )

            # Disable other buttons if items have been selected
            self.ui.btn_up.setEnabled(False)
            self.ui.btn_down.setEnabled(False)

            # Disable all home folders
            for i in range(self.ui.folders_layout.count()):
                item_from_list = self.ui.folders_layout.itemAt(i)
                widget = item_from_list.widget()
                if isinstance(widget, QPushButton):
                    widget.setEnabled(False)  # Disable function
                    i -= 1

            # Disable all home folders
            for i in range(self.ui.dates_layout.count()):
                item_from_list = self.ui.dates_layout.itemAt(i)
                widget = item_from_list.widget()
                if isinstance(widget, QPushButton):
                    widget.setEnabled(False)  # Disable function
                    i -= 1

        # If not, item was selected
        else:
            # Disable restore button
            self.ui.btn_restore.setEnabled(False)
            # Set self.files_to_restore length
            self.ui.btn_restore.setText("   Restore   ")

            # Enable all home folders            
            for i in range(self.ui.folders_layout.count()):
                item_from_list = self.ui.folders_layout.itemAt(i)
                widget = item_from_list.widget()
                if isinstance(widget, QPushButton):
                    widget.setEnabled(True)  # Disable function
                    i -= 1

            # Enable all dates folders            
            for i in range(self.ui.dates_layout.count()):
                item_from_list = self.ui.dates_layout.itemAt(i)
                widget = item_from_list.widget()
                if isinstance(widget, QPushButton):
                    widget.setEnabled(True)  # Disable function
                    i -= 1

        # Connection restore button
        # self.ui.btn_restore.clicked.connect(self.pre_start_restoring)

    def pre_start_restoring(self):
        """
        After restore is done, open the item restore folder. 
        If is not opened already.
        """
        if not self.folder_already_opened:
            self.folder_already_opened = True
            # Open folder manager
            print(f"Opening {HOME_USER}/{self.CURRENT_FOLDER}...")

            dst = HOME_USER + "/" + self.CURRENT_FOLDER
            sub.run(["xdg-open", dst], stdout=sub.PIPE, stderr=sub.PIPE)
            exit()

    def start_restore(self):
        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'True')
        
        file_path = f"{MAIN_INI_FILE.hd_hd()}/"\
            f"{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"\
            f"{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/"\
            f"{self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]}"\
            f"/{self.CURRENT_FOLDER}"

        ################################################################################
        # Restore files without spaces
        ################################################################################
        for counter in range(len(self.files_to_restore)):
            print(f"Restoring {handle_spaces(self.files_to_restore[counter])}")
            
            src = file_path + "/" + handle_spaces(self.files_to_restore[counter])
            dst = HOME_USER + "/" + self.CURRENT_FOLDER + "/"
            sub.Popen(['cp', '-rvf', src, dst], stdout=sub.PIPE, stderr=sub.PIPE)
            
        # Open file manager
        dst = HOME_USER + "/" + self.CURRENT_FOLDER
        sub.Popen(["xdg-open", "-avr", src, dst], stdout=sub.PIPE, stderr=sub.PIPE)

        # Update DB
        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')
        exit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if not self.preview_window:
                self.preview_window = PreviewWindow(self)

            if self.selected_item_extension in IMAGE_TYPES:
                pixmap = QPixmap(self.selected_item_full_location)

                self.preview_window.file_directory = self.selected_item_full_location

                # set_preview
                # self.preview_window.set_preview(pixmap.scaledToWidth(round(900/2)))
                self.preview_window.set_preview(pixmap)
                self.preview_window.show()

            elif self.selected_item_extension in TXT_TYPES:
                with open(self.selected_item_full_location, "r") as file:
                    # self.preview_window.preview_label.clear()
                    self.preview_window.set_preview(file.read())

                self.preview_window.show()

    def delete_all_results(self):
        self.ui.tree_widget.clear()

    ################################################################################
    # RETURN VALUES
    ################################################################################
    def get_all_backup_dates(self):
        for date_folder in os.listdir(
                f"{MAIN_INI_FILE.hd_hd()}/{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}"):

            # Hide hidden date_folder
            if "." not in date_folder:
                # ALREADY_GOT_LIST_OF_DATES = True

                self.LIST_OF_ALL_BACKUP_DATES.append(date_folder)
                self.LIST_OF_ALL_BACKUP_DATES.sort(
                    reverse=True,
                    key=lambda date_folder: datetime.strptime(date_folder, "%d-%m-%y"))
   

class PreviewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.setModal(True)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.file_directory = ""

        self.layout = QVBoxLayout(self)

    def set_preview(self, pixmap):
        open_file_button = QPushButton()
        open_file_button.setText("Open File Directory")
        open_file_button.setFocusPolicy(Qt.NoFocus)
        open_file_button.clicked.connect(self.open_file_button_clicked)

        if isinstance(pixmap, QPixmap):
            pixmap = pixmap.scaledToWidth((screen_height - 440), Qt.SmoothTransformation)
            preview_label = QLabel(self)
            preview_label.setPixmap(pixmap)

            self.layout.addWidget(preview_label)

        elif isinstance(pixmap, str):
            text_browser = QTextBrowser(self)
            text_browser.setFixedSize((screen_height - 440), (screen_height - 440))
            text_browser.setPlainText(pixmap)
            text_browser.adjustSize()
            text_browser.moveCursor(QTextCursor.Start)
            # text_browser.setStyleSheet(
            #     """
            #         font-size: 2px;
            #     """)

            self.layout.addWidget(text_browser)
            self.layout.addWidget(open_file_button)

        self.layout.addWidget(open_file_button)
        self.layout.setAlignment(open_file_button, Qt.AlignHCenter | Qt.AlignVCenter)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.remove_items()

    def remove_items(self):
        for i in range(self.layout.count()):
            widget_item = self.layout.itemAt(i)

            if widget_item.widget():
                print("Removing items")
                widget_item.widget().deleteLater()

        self.close()

    def open_file_button_clicked(self):
        file_directory = "/".join(self.file_directory.split("/")[:-1])
        # Open file directory
        sub.Popen(["xdg-open", file_directory], stdout=sub.PIPE, stderr=sub.PIPE)
        
        # Close external preview window
        self.remove_items()


if __name__ == "__main__":
    APP = QApplication(sys.argv)

    screen = APP.primaryScreen()  # Get the primary screen
    size = screen.size()  # Get the screen size
    screen_width = size.width()  # Get the screen width
    screen_height = size.height()  # Get the screen height

    MAIN = MainWindow()
    MAIN.setWindowTitle("Enter In Time Machine")

    # Get all backup folders
    get_all_backup_folders()
    # Add all backup folders
    MAIN.add_backup_folders()

    # Get all backup dates
    MAIN.get_all_backup_dates()
    # Add all backup dates
    MAIN.add_backup_dates()

    # Add  backup times folders for the current date folder
    MAIN.add_backup_times()

    MAIN.update_labels()

    # MAIN.showFullScreen()
    MAIN.show()

    sys.exit(APP.exec())
