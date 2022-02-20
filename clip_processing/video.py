from moviepy.editor import *
import glob


def make_clip(project_path, language, channel_name):
    final_imgs_path = project_path + r'\final_imgs'
    audio_path = project_path + r'\audio'
    if language == 'pl':
        end_card_animation_path = r'<path>\end_card_animation_pl.mp4'
        end_card_img_path = r'<path>\end_card_pl.png'
        video_title = 'Najlepsze komentarze - ' + channel_name
    elif language == 'de':
        end_card_animation_path = r'<path>\end_card_animation_de.mp4'
        end_card_img_path = r'<path>\end_card_de.png'
        video_title = 'Top Kommentare - ' + channel_name
    else:
        end_card_animation_path = r'<path>\end_card_animation.mp4'
        end_card_img_path = r'<path>\end_card.png'
        video_title = 'Most liked comments - ' + channel_name
    thumbnail_animation_path = project_path + r'\thumbnail_animation.mp4'
    final_clip_path = project_path + '\\' + video_title + r'.mp4'
    images_files = glob.glob(final_imgs_path + r'\*.jpg')
    clips = []
    thumbnail_animation = VideoFileClip(thumbnail_animation_path)
    clips.append(thumbnail_animation)
    index = len(images_files)
    for n in range(index, 0, -1):
        try:
            audio = AudioFileClip(audio_path + r'\audio' + str(n) + '.mp3')
            duration = audio.duration
            audio = audio.fx(afx.volumex, 2.0)
        except IOError:
            audio = None
            duration = 4
        image = (ImageClip(final_imgs_path + r'\i' + str(n) + '.jpg')
                .set_duration(duration)
                .set_audio(audio))
        clips.append(image)
    end_card_animation = VideoFileClip(end_card_animation_path)
    end_card_img = ImageClip(end_card_img_path).set_duration(20-end_card_animation.duration)
    clips.append(end_card_animation)
    clips.append(end_card_img)
    clip = concatenate_videoclips(clips, method='compose')
    song = glob.glob(project_path + r'\*.mp3', recursive=False)[0]
    music = AudioFileClip(song).subclip(0, -5).fx(afx.audio_fadeout, duration=5)
    audio = afx.audio_loop(music, duration=clip.duration)
    audio = afx.audio_fadeout(audio, duration=5)
    audio = audio.fx(afx.audio_normalize)
    new_audio = CompositeAudioClip([clip.audio, audio.fx(afx.volumex, 0.1)])
    clip = clip.set_audio(new_audio)
    clip.write_videofile(final_clip_path, fps=24)
    music.close()
    new_audio.close()

