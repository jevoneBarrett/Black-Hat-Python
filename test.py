import time
import win32com.client as win32
import win32api


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


data = win32api.GetLogicalDriveStrings()
print(data)