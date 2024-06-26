import subprocess as sub
import os
import shutil
import pathlib
from pathlib import Path


# Remember to change setup too!
HOME_USER = str(Path.home())
GET_CURRENT_LOCATION = pathlib.Path().resolve()

APP_NAME_CLOSE = "timemachine"
APP_NAME = "Time Machine"
APP_VERSION = "v1.1.6.102 dev"

DST_FOLDER_INSTALL = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}"
DST_APPLICATIONS_LOCATION = f"{HOME_USER}/.local/share/applications"
DST_FILE_EXE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
SRC_AUTOSTARTFOLDER_LOCATION=f"{HOME_USER}/.config/autostart"

SRC_MAIN_WINDOW_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/main_window.py"
SRC_CALL_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/call_migration_assistant.py"
SRC_MIGRATION_ASSISTANT_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/migration_assistant.py"

SRC_MIGRATION_ASSISTANT_ICON_212PX = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/migration_assistant_212px.png"

DST_BACKUP_CHECK_DESKTOP = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/desktop/backup_check.desktop"
SRC_TIMEMACHINE_DESKTOP = f"{HOME_USER}/.local/share/applications/{APP_NAME_CLOSE}.desktop"
DST_MIGRATION_ASSISTANT_DESKTOP = f"{HOME_USER}/.local/share/applications/migration_assistant.desktop"

SRC_RESTORE_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/restore_64px.svg"
SRC_BACKUP_ICON = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/icons/backup_128px.png"
SRC_ANALYSE_PY = f"{HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/analyse.py"


def install_dependencies(user_distro_name):
    # sudo apt install libxcb-*
    # sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
    # Depedencies
    if distribution_info:
        if (
            'debian' in user_distro_name or 
            'ubuntu' in user_distro_name or
            'mint' in user_distro_name):
            commands = ['python3-pip', 'flatpak']
            sub.run(
                ['sudo', 'apt', 'install', '-y'] + commands, check=True)
        
        elif 'fedora' in user_distro_name:
            commands = ['python3-pip', 'flatpak']
            sub.run(
                ['sudo', 'dnf', 'install', '-y'] + commands, check=True)

        elif 'opensuse' in user_distro_name:
            commands = ['python3-pip', 'flatpak']
            sub.run(
                ['sudo', 'zypper', 'install', '-y'] + commands, check=True)

        elif 'arch' in user_distro_name:
            commands = ["python-pip", "qt6-wayland", "flatpak"]
            for command in commands:
                try:
                    sub.run(
                        ["pacman", "-Qq", command], check=True)
                except sub.CalledProcessError:
                    sub.run(
                        ['sudo', 'pacman', '-S', command], check=True)

        try:
            command = f"{GET_CURRENT_LOCATION}/requirements.txt"
            sub.run(
                ["pip", "install", "-r", command], 
                    check=True)
        except:
            pass

        # Install Flathub remote
        sub.run(
            ['flatpak', 'remote-add',
            '--if-not-exists',
            'flathub',
            'https://dl.flathub.org/repo/flathub.flatpakrepo'], check=True)
    else:
        print('Could not install the dependencies!')
        print('Manual install all the dependencies, you can see them in requirements.txt')
        print('Copying files...')

def copy_files():
    try:
        # Copy current folder to the destination folder
        print('-----[COPYING]-----')
        print('From:', GET_CURRENT_LOCATION)
        print('To:', DST_FOLDER_INSTALL)
        print()
        shutil.copytree(
            GET_CURRENT_LOCATION, 
            DST_FOLDER_INSTALL, dirs_exist_ok=True)
    except Exception as error:
        print(error)
        # Remove 
        os.remove(DST_FOLDER_INSTALL)

def create_application_files():
    # Create .local/share/applications
    if not os.path.exists(DST_APPLICATIONS_LOCATION):
        command = DST_APPLICATIONS_LOCATION
        os.makedirs(command, exist_ok=True)
        # sub.run(["mkdir", command])

    # Send to DST_FILE_EXE_DESKTOP
    with open(SRC_TIMEMACHINE_DESKTOP, "w") as writer:
        writer.write(
            f"[Desktop Entry]\n "
            f"Version={APP_VERSION}\n "
            f"Type=Application\n "
            f"Name={APP_NAME}\n "
            f"Comment=Backup your files with {APP_NAME}\n "
            f"GenericName=Backup Tool\n "
            f"Icon={SRC_BACKUP_ICON}\n "
            f"Exec=python3 {SRC_MAIN_WINDOW_PY}\n "
            f"Path={HOME_USER}/.local/share/{APP_NAME_CLOSE}/\n "
            f"Categories=System\n "
            f"StartupWMClass={SRC_MAIN_WINDOW_PY.split('/')[-1]}\n "
            f"Actions=backup-now;\n "
            f"Terminal=false\n\n"

            f"[Desktop Action backup-now]\n "
            f"Name=Backup Now\n "
            f"Exec=python3 {SRC_ANALYSE_PY} %F\n ")

    # Migration_assistant .desktop
    with open(DST_MIGRATION_ASSISTANT_DESKTOP, "w") as writer:
        writer.write(
            f"[Desktop Entry]\n "
            f"Version={APP_VERSION}\n "
            f"Type=Application\n "
            f"Name=Migration Assistant\n "
            f"Comment=Restore files/folders etc. from a {APP_NAME}'s backup\n "
            f"Icon={SRC_MIGRATION_ASSISTANT_ICON_212PX}\n "
            f"Exec=python3 {SRC_CALL_MIGRATION_ASSISTANT_PY}\n "
            # f"Exec=python3 {SRC_MIGRATION_ASSISTANT_PY}\n "
            f"Path={HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/\n "
            f"Categories=System\n "
            f"StartupWMClass={(SRC_MIGRATION_ASSISTANT_PY).split('/')[-1]}\n "
            f"Terminal=false")

def create_backup_checker_desktop():
    try:
        # Create autostart folder if necessary
        if not os.path.exists(SRC_AUTOSTARTFOLDER_LOCATION):
            os.makedirs(SRC_AUTOSTARTFOLDER_LOCATION, exist_ok=True)

        # Edit file startup with system
        with open(DST_BACKUP_CHECK_DESKTOP, "w") as writer:
            writer.write(
                f"[Desktop Entry]\n "
                f"Type=Application\n "
                f"Exec=/bin/python3 {HOME_USER}/.local/share/{APP_NAME_CLOSE}/src/at_boot.py\n "
                f"Hidden=false\n "
                f"NoDisplay=false\n "
                f"Name={APP_NAME}\n "
                f"Comment={APP_NAME}'s manager before boot.\n "
                f"Icon={SRC_RESTORE_ICON}")
    except:
        pass

def detect_linux_distribution():
    distribution_info = {}
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release', 'r') as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                # Remove quotes from value
                value = value.strip('"')
                distribution_info[key] = value
    return distribution_info


if __name__ == '__main__':
    distribution_info = detect_linux_distribution()
    if distribution_info:
        USERS_DISTRO_NAME = distribution_info.get('NAME')
        print()
        print("Detected Linux distribution:", USERS_DISTRO_NAME)
        print("Version:", distribution_info.get('VERSION'))
        print()
    else:
        print("Unable to detect Linux distribution.")
        exit()
    
    try:
        # Install dependencies
        print("Installing dependencies...")
        install_dependencies(user_distro_name=str(USERS_DISTRO_NAME).lower())
    except Exception as e:
        print('Error while trying to install the dependencies.')
        exit()
    try:
        # Begin installation
        print()
        print(f"Copyng files to {HOME_USER}/.local/share/{APP_NAME_CLOSE}/...")
        copy_files()
    except Exception as e:
        print('Error while trying to copy the files.')
        exit()
    try:
        # Create exe files
        print(f"Creating {APP_NAME_CLOSE}.desktop...")
        create_application_files()

        # Create backup checker.dekstop
        print(f"Creating backup_checker.desktop...")
        create_backup_checker_desktop()
    except Exception as e:
        print('Error while trying to creating .desktop files.')
        exit()
    
    print()
    print("Program was successfully installed!")
    exit()
