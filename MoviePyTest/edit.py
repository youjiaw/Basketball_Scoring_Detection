from moviepy.editor import *

input_video_name = "Fat cat with bread stick.mp4"
input_audio_name = "sample.mp3"

# audioclip = AudioFileClip(input_audio_name).subclip(45,52)
# videoclip = VideoFileClip(input_video_name)
# videoclip2 = videoclip.set_audio(audioclip)
# videoclip2.write_videofile("output.mp4")

# Default discard audio of original video
def AddSoundEffect(video, audio, origin_audio=False):
    if origin_audio:
        video_audio = video.audio
        audio = CompositeAudioClip([video_audio,audio])
    return video.set_audio(audio)

# Default speed = 0.5
def SlowMotion(video, spd=0.5):
    return video.fx(vfx.speedx, spd)


if __name__=="__main__":
    
    video = VideoFileClip(input_video_name)
    audio = AudioFileClip(input_audio_name).subclip(45,52)
    AddSoundEffect(video,audio).write_videofile("SoundEffect.mp4")
    SlowMotion(video).write_videofile("SlowMotion.mp4")
