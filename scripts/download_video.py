import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor
from google.colab import files
import re

basepath = os.getcwd()
uploaded = files.upload()  # 上传文件
for filename in uploaded.keys():
    assert (filename.endswith(".txt")), "speaker-videolink info could only be .txt file!"
    filpath_dest = os.path.join("./speaker_links.txt")
    print("Moving file to ", filpath_dest)
    shutil.move(os.path.join(basepath, filename), filpath_dest)


def generate_infos():
    infos = []
    with open("./speaker_links.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print("lines", lines)
    for line in lines:
        line = line.replace("\n", "").replace(" ", "")
        if line == "":
            continue
        speaker, link = line.split("|")
        # link_sanitized = '-'.join(re.findall(r'\w+', link))
        filename = speaker + "_" + str(random.randint(0, 1000000))
        info = {"link": link, "filename": filename}
        print("speaker, link")
        print(speaker, link, info)
        infos.append(info)
    return infos


def download_video(info):
    link = info["link"]
    filename = info["filename"]
    command = f'yt-dlp {link} -o "./video_data/{filename}.%(ext)s" -f "(bestaudio)" -x  --no-check-certificate'
    print("download_video", info)
    print("command", command)
    os.system(command)


if __name__ == "__main__":
    infos = generate_infos()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(download_video, infos)
