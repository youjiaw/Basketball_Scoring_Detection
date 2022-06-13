from moviepy.editor import *
from django.conf import settings

input_video_dir = settings.MEDIA_ROOT



# Default discard audio of original video
def AddSoundEffect(video, audio, origin_audio=False):
    if origin_audio:
        video_audio = video.audio
        audio = CompositeAudioClip([video_audio,audio])
    return video.set_audio(audio)

# Default speed = 0.5
def SlowMotion(video, spd=0.5):
    return video.fx(vfx.speedx, spd)


def main(s, m, musicdir, filename):

    video_path = input_video_dir + "/filtered_videos/" + filename
    print(video_path)

    video = VideoFileClip(video_path)

    if s == 1:
        slow_out_path = input_video_dir + "/filtered_videos/slow_" + filename
        print(slow_out_path)
        SlowMotion(video).write_videofile(slow_out_path)

    input_audio_name = ""
    if m != 0:
        if m == 1:
            input_audio_name = "1.mp3"
        elif m == 2:
            input_audio_name = "2.mp3"
        elif m == 3:
            input_audio_name = "3.mp3"
        elif m == 4:
            input_audio_name = "4.mp3"
        elif m == 5:
            input_audio_name = "5.mp3"
        
        
        audio = AudioFileClip(musicdir + "/" + input_audio_name)

        if s == 1:
            musicslow_out_path = input_video_dir + "/filtered_videos/musicslow_" + filename
            print(musicslow_out_path)
            video = VideoFileClip(slow_out_path)
            AddSoundEffect(video,audio).write_videofile(musicslow_out_path)

        else:
            music_out_path = input_video_dir + "/filtered_videos/music_" + filename
            print(music_out_path)
            AddSoundEffect(video,audio).write_videofile(music_out_path)

        
        
        