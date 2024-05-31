from openi import create_tqdm
import time

f = create_tqdm("filename1", 64 * 1024 * 1024, position=0)
f2 = create_tqdm("filename2", 100, position=1)
f3 = create_tqdm("filename3", 3 * 1024 * 1024 * 1024, position=2)


f.uploading()
for i in range(64):
    f.update(1024 * 1024)
    time.sleep(0.1)
f.completed()

f2.skipped()

f3.downloading()
for i in range(2):
    f3.update(1024 * 1024 * 1024)
    time.sleep(0.1)
f3.failed()
