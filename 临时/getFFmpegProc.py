import psutil
import time

def getFFmpegProc():
    ffmpeg = 0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            ffmpeg = ffmpeg + 1 if pinfo["name"] == "ffmpeg.exe" else ffmpeg
    return ffmpeg


while True:
	print(getFFmpegProc())
	time.sleep(2)

