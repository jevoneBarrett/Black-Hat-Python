import time
import win32com.client as win32
import win32api
import sys

def explore():
    ie = win32.gencache.EnsureDispatch('InternetExplorer.Application')
    ie.Visible = True
    ie.Navigate("www.google.com")
    time.sleep(5)
    ie.Application.Quit()


def shutDown():
    try:
        print("Attempting to shutdown pc...")
        win32api.InitiateSystemShutdown(None, "Shutting down in 10 seconds", 11, False, True)
    except Exception as e:
        print(f"Attempt to shut down PC failed because: {e}")


def get_default_interface():
    if sys.platform == "win32":
        return "Wi-Fi"
    else:
        return "en0"


data = get_default_interface()
print(data)