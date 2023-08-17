# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
from ui_untitled import Ui_MainWindow
from setup import *
from read_ini_file import UPDATEINIFILE
from datetime import datetime


MAIN_INI_FILE  = UPDATEINIFILE()

TXT_TYPES = [
    "txt", "py", "cpp", "h", "c", "cgi",
    "cs", "class", "java", "php", "sh",
    "swift", "vb", "doc", "docx", "odt",
    "pdf", "rtf", "tex", "wpd"
    ]

IMAGE_TYPES = [
    "png", "jpg", "jpeg", "webp", "gif", "svg",
    "eps", "pdf", "ai", "indd", "raw", "tiff",
    "bmp", "ps", "tif"
    ]


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ALREADY_CHECKED_FIRST_FOLDER = False
        self.ALREADY_OPENED_FILE_MANAGER = False
        
        self.files_to_restore = []
        self.files_to_Restore_with_space = []
        
        self.INDEX_TIME = 0
        
        self.list_of_preview_items = []

        self.COUNTER_FOR_DATE = 0
        self.COUNTER_FOR_TIME = 0

        self.CURRENT_FOLDER = ""

        self.LIST_OF_ALL_BACKUP_DATES = []
        self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE = []

        self.currentLocationLabel = QLabel(self)

        self.last_selected_item = ""

        # Connections
        ## Up button
        self.ui.btn_up.clicked.connect(self.btn_up_clicked)
        ## Down button
        self.ui.btn_down.clicked.connect(self.btn_down_clicked)
        ## Cancel button
        self.ui.btn_cancel.clicked.connect(self.btn_cancel_clicked)
        ## Restore button
        self.ui.btn_restore.clicked.connect(self.start_restore)
        
        # Settings forom QTree
        self.ui.tree_widget.setHeaderLabels(["Name", "Date Modified", "Size", "Type"])
        self.ui.tree_widget.setColumnWidth(0, 250)  
        self.ui.tree_widget.setColumnWidth(1, 150)  
        self.ui.tree_widget.clicked.connect(self.selected_item_for_preview)
        self.ui.tree_widget.itemSelectionChanged.connect(self.selected_item_for_preview)
        self.ui.tree_widget.itemClicked.connect(self.QTree_checkbox_clicked)

        # Settings for preview window
        self.preview_window = None

    def add_backup_folders(self):
        # Get backup folders names
        for folder in self.get_all_backup_folders():
            try:
                # Can folder be found inside Users Home?
                folder = folder.capitalize()
                os.listdir(f"{HOME_USER}/{folder}")
            except FileNotFoundError as e:
                # Lower folder first letter
                folder = folder.lower() # Lower folder first letter

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
            self.btn_backup_home_folders.clicked.connect(lambda *args, dir = folder: self.change_dir(dir))
            self.ui.folders_layout.addWidget(self.btn_backup_home_folders)

            # Auto check the first folder in the list
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
        for date in self.LIST_OF_ALL_BACKUP_DATES:
            ################################################################################
            # PUSH BUTTON
            ################################################################################
            self.btn_backup_date_folders = QPushButton()

            # Convert date from 00-00-00 to Xxxxx 00, 000
            date_obj = datetime.strptime(date, "%d-%m-%y")
            formatted_date = date_obj.strftime("%B %d, %Y")

            # Set text to button
            self.btn_backup_date_folders.setText(formatted_date)
            self.btn_backup_date_folders.setMinimumWidth(120)
            self.btn_backup_date_folders.setFixedHeight(28)
            self.btn_backup_date_folders.setCheckable(True)
            self.btn_backup_date_folders.setAutoExclusive(True)
            self.btn_backup_date_folders.clicked.connect(
                    lambda *args, date = date:\
                    self.change_date(date)
                    )
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
            self.ui.dates_layout.addWidget(self.btn_backup_date_folders, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            
            # Limit number of dates on screen
            counter += 1
            if counter == 12:
                break

        """ Check it, so it wont auto check the first in the list
            again after just changing time or folder 
        """
        for index in range(self.ui.dates_layout.count()):
            button = self.ui.dates_layout.itemAt(index).widget()
            if isinstance(button, QPushButton):
                print(button.text())
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
            inside_this_date_folder = f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"\
                f"{BACKUP_FOLDER_NAME}/{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/"

            ################################################################################
            # If inside the external "date folders" has not "time folder", pass to avoid display error :D
            ################################################################################
            for time_folder in os.listdir(inside_this_date_folder):
                # Add found "dates time" to the Time list
                self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.append(time_folder)
                # Sort and reverse
                self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.sort(reverse=True)

                # Check if choosed time folder exists
                if os.path.exists(
                        f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/"
                        f"{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"
                        f"{self.LIST_OF_ALL_BACKUP_DATES[(self.COUNTER_FOR_DATE)]}/"
                        f"{time_folder}/"):
                    ################################################################################
                    # PUSH BUTTON
                    ################################################################################
                    self.btn_backup_time_folders = QPushButton()
                    self.btn_backup_time_folders.setText(time_folder.replace("-", ":")  )
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

        except IndexError as e:
            # Reset counter for time
            self.COUNTER_FOR_TIME = 0
            # Add 1 for time counter
            self.COUNTER_FOR_TIME += 1

        # Show results
        # Show results asynchronously
        thread = threading.Thread(target=self.show_results)
        thread.start()

    def show_results(self):
        inside_current_folder = f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/{BASE_FOLDER_NAME}/"\
                f"{BACKUP_FOLDER_NAME}/{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/"\
                f"{self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]}/{self.CURRENT_FOLDER}"

        # Add options to QTree
        file_list = []
        try:
            for filename in os.listdir(inside_current_folder):
                full_path = os.path.join(inside_current_folder, filename)

                if os.path.isfile(full_path) and not filename.startswith('.'):  # Only include files, skip hidden files
                    size = os.path.getsize(full_path)
                    date_modified = os.path.getmtime(full_path)
                    extension = os.path.splitext(filename)[1]

                    formatted_date = datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S')
                    formatted_size = self.size_format(size) if size is not None else ''

                    file_list.append((filename, formatted_date, formatted_size, extension, date_modified))

            # Sort the file list by filename before populating the tree
            file_list.sort(key=lambda x: x[0])

            for item_data in file_list:
                item = QTreeWidgetItem(self.ui.tree_widget, item_data[:-1])
                item.setData(1, Qt.UserRole, item_data[-1])  # Store the timestamp as user data
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Allow selection
                item.setCheckState(0, Qt.Unchecked)

            self.QTree_add_folders(inside_current_folder)

        except FileNotFoundError as e:
            pass

    def QTree_add_folders(self, inside_current_folder):
        for folder_name in os.listdir(inside_current_folder):
            folder_path = os.path.join(inside_current_folder, folder_name)

            if os.path.isdir(folder_path) and not folder_name.startswith('.'):
                folder_item = QTreeWidgetItem(self.ui.tree_widget, [folder_name, '', '', 'Folder'])
                self.QTree_add_subitems(folder_item, folder_path)

    def QTree_add_subitems(self, parent_item, folder_path):
        try:
            for item_name in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item_name)
                if os.path.isdir(item_path):
                    subfolder_item = QTreeWidgetItem(parent_item, [item_name, '', '', 'Folder'])
                    self.QTree_add_subitems(subfolder_item, item_path)
                
                elif os.path.isfile(item_path) and not item_name.startswith('.'):
                    size = os.path.getsize(item_path)
                    date_modified = os.path.getmtime(item_path)
                    extension = os.path.splitext(item_name)[1]

                    formatted_date = datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S')
                    formatted_size = self.size_format(size) if size is not None else ''

                    item = QTreeWidgetItem(parent_item, [item_name, formatted_date, formatted_size, extension])
                    item.setData(1, Qt.UserRole, date_modified)  # Store the timestamp as user data
                    # TODO
                    # item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # Allow selection
                    # item.setCheckState(0, Qt.Unchecked)
        except PermissionError as e:
            pass

        self.up_down_settings()

    def up_down_settings(self):
        # Get index of the current time folder
        self.INDEX_TIME = self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.index(self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME])

        ################################################################################
        # DOWN ARROW
        ################################################################################
        # If the first time from list is checked
        if self.INDEX_TIME  == 0:  # 0 = The latest time folder available
            # Disable down arrow, unable to go back from 0
            self.ui.btn_down.setEnabled(False)
        else:
            # Enable down arrow, able to go back from current index
            self.ui.btn_down.setEnabled(True)

        ################################################################################
        # UP ARROW
        ################################################################################
        # If is there more options to choosed from time list
        if self.INDEX_TIME  + 1  == len(self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE):
            # Disable up arrow, unable to go forward, there is no more options to choose
            self.ui.btn_up.setEnabled(False)
        else:
            # Enable up arrow, able to go forward, there is more options to choose
            self.ui.btn_up.setEnabled(True)

        self.update_labels()

    def update_labels(self):
        date_now = MAIN_INI_FILE.current_date() + "-" + MAIN_INI_FILE.current_month()+ "-"+ MAIN_INI_FILE.current_year()

        # Display current folder on display
        # self.currentLocationLabel.setText(f"<h1>{self.CURRENT_FOLDER}</h1>")
        # self.currentLocationLabel.adjustSize()

        try:
            if self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE] == str(date_now):
                # Update date label
                self.ui.label_gray_time.setText(f'Today ({self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]})'.replace("-", ":"))
            else:
                self.ui.label_gray_time.setText(f'({self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]})'.replace("-", ":"))
        # If a non backup folder was clicked
        except IndexError as i:
            pass

    ################################################################################
    # CONNECTIONS
    ################################################################################
    def btn_up_clicked(self):
        self.COUNTER_FOR_TIME += 1
        # Show results asynchronously
        thread = threading.Thread(target=self.show_results)
        thread.start()

    def btn_down_clicked(self):
        self.COUNTER_FOR_TIME -= 1
        # Show results asynchronously
        thread = threading.Thread(target=self.show_results)
        thread.start()
   
    def btn_cancel_clicked(self):
        exit()

    def change_date(self, date):
        # Clean QTree area
        self.ui.tree_widget.clear()

        # Reset counter for time
        self.COUNTER_FOR_TIME = 0

        # Clear list 0f time folders
        self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE.clear()

        # Get new index for counter of dates
        self.COUNTER_FOR_DATE = self.LIST_OF_ALL_BACKUP_DATES.index(date)

        # Add news time folders
        self.add_backup_times()

    def change_dir(self, dir):
        # Clean QTree
        self.ui.tree_widget.clear()

        # Get current folder name
        self.CURRENT_FOLDER = dir
        # Reset counter for time
        self.COUNTER_FOR_TIME = 0

        # Show results asynchronously
        thread = threading.Thread(target=self.show_results)
        thread.start()

    def selected_item_for_preview(self):
        selected_items = self.ui.tree_widget.selectedItems()
       
        if selected_items:
            item = selected_items[-1]  # Get the last selected item
            item_txt = item.text(0)
            print("Last selected item:", item_txt)
            self.last_selected_item = item_txt
        
            # TODO
            # DECIFRAR ISSO DEPOIS LOL
            # Remove items from self.files_to_restore that are no longer selected
            # self.files_to_restore = [item for item in self.files_to_restore if item in [item.text(0) for item in selected_items]]
            # new_loc = []
            # for item in self.files_to_restore:
            #     found = False
            #     for selected_item_for_preview in selected_items:
            #         if item == selected_item_for_preview.text(0):
            #             found = True
            #             break
            #     if found:
            #         new_loc.append(item)
            # self.files_to_restore = new_loc
            

            # file_path = f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/"\
            #         f"{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"\
            #         f"{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/"\
            #         f"{self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]}"\
            #         f"/{self.CURRENT_FOLDER}/{item_txt}"
            
        try:
            # Show small preview
            self.show_small_preview(item_txt)
        except UnboundLocalError as e:
            # Clear pixmap window
            self.ui.small_preview_label.clear()

    def show_small_preview(self, item_txt):
        # If a file
        if "." in item_txt:
            self.last_selected_item_extension = str(item_txt).split('.')[-1]
            self.last_selected_item_full_location = f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/"\
                    f"{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}/"\
                    f"{self.LIST_OF_ALL_BACKUP_DATES[self.COUNTER_FOR_DATE]}/"\
                    f"{self.LIST_OF_BACKUP_TIME_FOR_CURRENT_DATE[self.COUNTER_FOR_TIME]}"\
                    f"/{self.CURRENT_FOLDER}/{item_txt}"
            
            # Image
            if self.last_selected_item_extension in IMAGE_TYPES:
                pixmap = QPixmap(self.last_selected_item_full_location)
                pixmap = pixmap.scaledToWidth(196, Qt.SmoothTransformation)
                self.ui.small_preview_label.setPixmap(pixmap)

                # Hide ui text
                self.ui.small_preview_text.setFixedHeight(0)
                self.ui.small_preview_text.hide()

                # Expand ui label
                self.ui.small_preview_label.setFixedHeight(222)
                self.ui.small_preview_label.show()

            elif self.last_selected_item_extension in TXT_TYPES:
                self.read_file()
            
            # Non ok item
            else:
                # Hide ui text
                self.ui.small_preview_text.setFixedHeight(0)
                self.ui.small_preview_text.hide()
               
               # Hide ui label
                self.ui.small_preview_label.setFixedHeight(0)
                self.ui.small_preview_label.hide()

    def read_file(self):
        with open(self.last_selected_item_full_location, "r") as file:
            # Hide ui label
            self.ui.small_preview_label.setFixedHeight(0)
            self.ui.small_preview_label.hide()

            # Expand ui text
            self.ui.small_preview_text.setFixedHeight(222)
            self.ui.small_preview_text.show()

            self.ui.small_preview_text.adjustSize()
            self.ui.small_preview_text.setPlainText(file.read())
            self.ui.small_preview_text.moveCursor(QTextCursor.Start)

    def get_full_location(self, item):
        location_parts = []

        while item is not None:
            location_parts.insert(0, item.text(0))
            item = item.parent()

        full_location = os.path.join(self.CURRENT_FOLDER, *location_parts)

        return full_location
    
    def add_to_restore(self):
        ################################################################################
        # Enable/Disable functions if item(s) is/are selected
        ################################################################################
        if len(self.files_to_restore) or len(self.files_to_Restore_with_space) >= 1:  # If something inside list
            # If has at least one item, enable restore button
            self.ui.btn_restore.setEnabled(True)
            # Update restore label
            self.ui.btn_restore.setText(
                f"   Restore({len(self.files_to_restore) + len(self.files_to_Restore_with_space)})   "
                )

            # Disable other buttons if items if been selected
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

        # If not item was selected
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
        if not self.folderAlreadyOpened:
            self.folderAlreadyOpened=True
            # Open folder manager
            print(f"Opening {HOME_USER}/{self.CURRENT_FOLDER}...")
            sub.Popen(f"xdg-open {HOME_USER}/{self.CURRENT_FOLDER}",shell=True)
            exit()

    def start_restore(self):
        print("Your files are been restored...")
        
        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'True')

        ################################################################################
        # Restore files without spaces
        ################################################################################
        counter = 0
        for _ in self.files_to_restore:
            print(f"Restoring {COPY_RSYNC_CMD} {self.files_to_restore[counter]} {HOME_USER}/{self.CURRENT_FOLDER}/")
            # sub.Popen(f"{COPY_RSYNC_CMD} {self.files_to_restore[counter]} {HOME_USER}/{self.CURRENT_FOLDER}/", shell=True)
            counter += 1

        # Open file manager
        if not self.ALREADY_OPENED_FILE_MANAGER:
            self.ALREADY_OPENED_FILE_MANAGER = True
            # Open folder manager
            sub.Popen(f"xdg-open {HOME_USER}/{self.CURRENT_FOLDER}",shell=True)

        MAIN_INI_FILE.set_database_value('STATUS', 'is_restoring', 'False')
        exit()

    def QTree_checkbox_clicked(self, item, column):
        if item.checkState(column) == Qt.Checked:
            item_txt = item.text(column)

            # Spaces in item
            if " " in item_txt:
                # Add to restore list for spaces
                if not item_txt in self.files_to_Restore_with_space:  
                    self.files_to_Restore_with_space.append(item_txt)  
                else:
                    self.files_to_Restore_with_space.remove(item_txt)  

            # No spaces in item_txt
            else:
                if item_txt not in self.files_to_restore:  
                    # Add if not already in list
                    self.files_to_restore.append(item_txt)  
                else:
                    # Remove from list
                    self.files_to_restore.remove(item_txt)  

            self.add_to_restore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if not self.preview_window:
                self.preview_window = PreviewWindow(self)

            if self.last_selected_item_extension in IMAGE_TYPES:
                pixmap = QPixmap(self.last_selected_item_full_location)

                # self.preview_window.set_preview(pixmap.scaledToWidth(round(900/2)))
                self.preview_window.set_preview(pixmap)
                self.preview_window.show()

            elif self.last_selected_item_extension in TXT_TYPES:
                with open(self.last_selected_item_full_location, "r") as file:
                    # self.preview_window.preview_label.clear()
                    self.preview_window.set_preview(file.read())

                self.preview_window.show()

    ################################################################################
    # RETURN VALUES
    ################################################################################
    def get_all_backup_folders(self):
        FOLDERS_LIST = []

        # Connect to the SQLite database
        conn = sqlite3.connect(SRC_USER_CONFIG_DB)
        cursor = conn.cursor()
        # Query all keys from the specified table
        cursor.execute(f"SELECT key FROM FOLDER")
        keys = [row[0] for row in cursor.fetchall()]
        # Close the connection
        conn.close()

        for folder in keys:
            FOLDERS_LIST.append(folder)
            FOLDERS_LIST.sort()

        return FOLDERS_LIST

    def get_all_backup_dates(self):
        counter = 0
        for date_folder_to_be_sort in os.listdir(
                f"{MAIN_INI_FILE.get_database_value('EXTERNAL', 'hd')}/"
                f"{BASE_FOLDER_NAME}/{BACKUP_FOLDER_NAME}"):

            # Hide hidden date_folder_to_be_sort
            if "." not in date_folder_to_be_sort:
                print(date_folder_to_be_sort)
                # ALREADY_GOT_LIST_OF_DATES = True

                self.LIST_OF_ALL_BACKUP_DATES.append(date_folder_to_be_sort)
                self.LIST_OF_ALL_BACKUP_DATES.sort(
                    reverse = True,
                    key = lambda date_folder_to_be_sort:\
                    datetime.strptime(date_folder_to_be_sort, "%d-%m-%y")
                    )

    def size_format(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            
            size_bytes /= 1024.0

    def resize_image(self, pixmap, max_size):
        if pixmap.width() > max_size or pixmap.height() > max_size:
            pixmap = pixmap.scaled(max_size, max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        return pixmap


class PreviewWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.setModal(True)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.layout = QVBoxLayout(self)
    
    def set_preview(self, pixmap):
        if isinstance(pixmap, QPixmap):
            try:
                pixmap = pixmap.scaledToWidth((screen_height - 440), Qt.SmoothTransformation)
                self.preview_label = QLabel(self)
                self.preview_label.setPixmap(pixmap)
                self.layout.addWidget(self.preview_label)
            except Exception as e:
                pass

        elif isinstance(pixmap, str):
            try:
                self.text_browser = QTextBrowser(self)
                self.text_browser.setPlainText(pixmap)
                self.text_browser.adjustSize()
                self.text_browser.moveCursor(QTextCursor.Start)
                self.layout.addWidget(self.text_browser)
            except Exception as e:
                pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            for i in range(self.layout.count()):
                widget_item = self.layout.itemAt(i)

                if widget_item.widget():
                    widget_item.widget().deleteLater()

            self.close()


if __name__ == "__main__":
    APP = QApplication(sys.argv)

    screen = APP.primaryScreen()  # Get the primary screen
    size = screen.size()  # Get the screen size
    screen_width = size.width()   # Get the screen width
    screen_height = size.height()  # Get the screen height
    
    MAIN = MainWindow()
    MAIN.setWindowTitle("Enter In Time Machine")

    # Get all backup folders
    MAIN.get_all_backup_folders()
    # Add all backup folders
    MAIN.add_backup_folders()

    # Get all backup dates
    MAIN.get_all_backup_dates()
    # Add all backup dates
    MAIN.add_backup_dates()

    # Add  backup times folders for the current date folder
    MAIN.add_backup_times()

    # MAIN.showFullScreen()
    MAIN.show()

    sys.exit(APP.exec())