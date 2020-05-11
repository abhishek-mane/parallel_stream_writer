
from time import sleep
from threading import Thread
from stream_writer import ParallelStreamWriter

task_type = 'Downloading'

writer = ParallelStreamWriter(task_type)


files = [
    'readme.txt', 'directx.msi', 'music-file.mp3', 'video-file.mp4',
    'vscode.dmg', 'google-chrome.deb'
]

print('')

## register tasks
for f in files:
    writer.add_task(f)

## initialize tasks
for f in files:
    writer.init_task(f)


def do_download(w, task_name):
    for i in range(1, 101):
        w.update_status(task_name, '{}%'.format(str(i)))
        sleep(.10)
    w.update_status(task_name, 'done')


## threads
tasks = []
for f in files:
    tasks.append(Thread(target=do_download, args=(writer, f)))

for t in tasks:
    t.start()

for t in tasks:
    t.join()

