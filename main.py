import setup as org
import get_videos as gv
import comments_actions as ca
import csv_to_images as cti
from clip_processing import audio
from clip_processing import video
import re
import glob
import time


def data_preparation(playlist_id, project_path, comments_pagination):
    gv.videos_to_csv(playlist_id, project_path)
    print('1. Videos collected')
    ca.all_comments_to_df(project_path, comments_pagination)
    print('2. Comments collected')


def data_pre_processing(project_path, top_comments_qty, channel_name):
    ca.get_top_comments(project_path, top_comments_qty, channel_name)
    print('3. Top comments collected')
    ca.merge_comments_on_vids(project_path)
    print('3. Get the top and merged with videos')
    cti.generate_htmls(project_path)
    print('4. HTMLs generated')


def image_processing(project_path):
    cti.screen_shot_comments(project_path)
    cti.generate_final_images(project_path)


def get_channel_name(project_path):
    channel_name = project_path.split('\\')[-1]
    channel_name = re.sub('^\d+. ', '', channel_name)
    return channel_name


def get_language(project_path):
    if r'1. Most liked comments' in project_path:
        return 'eng'
    elif r'2. Najlepsze komentarze YT' in project_path:
        return 'pl'
    elif r'3. Top YouTube Kommentare' in project_path:
        return 'de'


def wait_for_file(project_path, file):
    print('Waiting for ' + file, end='')
    while not glob.glob(project_path + r'\\' + file):
        print('..', end='')
        time.sleep(5)
    print('\nFile ' + file + ' found.')


def execute(playlist_id, project_path, comments_pagination, top_comments_qty, speech_speed):
    channel_name = get_channel_name(project_path)
    language = get_language(project_path)
    data_preparation(playlist_id, project_path, comments_pagination)
    org.make_dirs(project_path)
    data_pre_processing(project_path, top_comments_qty, channel_name)
    audio.comments_to_mp3(project_path, speech_speed, language)
    print('8. Audio files generated')
    wait_for_file(project_path, r'default.jpg')
    image_processing(project_path)
    wait_for_file(project_path, r'*.mp3')
    wait_for_file(project_path, r'thumbnail_animation.mp4')
    video.make_clip(project_path, language, channel_name)
    print('9. Video is done')
    org.generate_description(project_path, language, channel_name)


def main():
    playlist_id = r''
    project_path = r''
    execute(playlist_id=playlist_id,
            project_path=project_path,
            comments_pagination=2,
            top_comments_qty=75,
            speech_speed=130)


   # ap.show_languages()
   # ap.manually_test_to_mp3("Hallo, mein name ist", project_path, 140, 4)



if __name__ == "__main__":
    main()
