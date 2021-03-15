import contextlib
import os
import queue
import requests
import sys
import requests
import threading
import time
import getpass


FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "https://reviewfix.com"
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()

def gather_paths():
    for root, _, files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        time.sleep(2)
        r = requests.get(url)
        if r.status_code == 200:
            sys.stdout.write('+')
        else:
            sys.stdout.write('x')
        sys.stdout.flush()

def run():
    my_threads = list()
    for i in range(THREADS):
        print(f'Spawining thread {i}')
        t = threading.Thread(target=test_remote)
        my_threads.append(t)
        t.start()
    for thread in my_threads:
        thread.join()


@contextlib.contextmanager
def chdir(path):
    """
    On enter, change directory to specified path
    On exit, change directory back to original
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)


if __name__=='__main__':
    local_wordpress = f"C:/Users/{getpass.getuser()}/Downloads/wordpress-5.6.2/wordpress"
    with chdir(local_wordpress):
        gather_paths()
    input('Press return to continue. ')
    run()
    with open('myanswers.txt', 'w') as f:
        f.write(f'{answers.get()}\n')
    print("Done")