import os
from concurrent.futures import ThreadPoolExecutor

from moviepy.editor import AudioFileClip

video_dir = "./video_data/"
audio_dir = "./raw_audio/"
filelist = list(os.walk(video_dir))[0][2]


def generate_infos():
    videos = []
    for file in filelist:
        videos.append(file)
    return videos


def clip_file(file):
    filepath =  video_dir + file
    try:
        my_audio_clip = AudioFileClip(filepath)
        my_audio_clip.write_audiofile(audio_dir + file.rstrip(".mp4") + ".wav")
    except Exception as e:
        print(e)
        print(f'Failed to get audio from file "{filepath}"')


if __name__ == "__main__":
    infos = generate_infos()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(clip_file, infos)
