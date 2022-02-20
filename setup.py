import os
import pandas as pd
import glob


def make_dirs(project_path):
    os.makedirs(project_path + r'\htmls', exist_ok=True)
    os.makedirs(project_path + r'\comments_imgs', exist_ok=True)
    os.makedirs(project_path + r'\final_imgs', exist_ok=True)
    os.makedirs(project_path + r'\audio', exist_ok=True)


def generate_description(project_path, language, channel_name):
    heading, music, remaining_links = None, None, None
    if language == 'eng':
        heading = 'Compilation of most liked comments of ' + channel_name + '\'s videos.\n Links to source videos:\n'
        music = '\n Music:\n'
        remaining_links = '\nRemaining links:\n'
    elif language == 'pl':
        heading = 'Kompilacja najbardziej lajkowanych komentarzy na kanale ' + channel_name + '.\n Linki do filmów:\n'
        music = '\n Muzyka:\n'
        remaining_links = '\nPozostałe linki: \n'
    elif language == 'de':
        heading = 'Zusammenstellung der beliebtesten Kommentare auf dem Kanal ' + channel_name +\
                  '.\n Links zu Videos:\n'
        music = '\n Musik:\n'
        remaining_links = '\n Verbleibende Links:\n'

    df = pd.read_csv(project_path + r'\merged_comms_vids.csv')
    description_path = project_path + r"\description.txt"
    song_title = glob.glob(project_path + r'\*.mp3', recursive=False)[0]
    song_title = song_title.replace(project_path + '\\', '').replace('.mp3', '')
    file = open(description_path, 'a', encoding='utf-8')
    file.write(heading)
    df = df.sort_values(by=['likeCount'])
    broken = False
    file_lenght = len(heading) + len(music) + len(song_title)

    for index, comment in df.iterrows():
        line1 = '#' + str(index+1) + ' ' + comment['title'] + ':\n'
        line2 = '   ' + 'https://www.youtube.com/watch?v=' + comment['videoId'] + '\n'
        file.write(str(line1))
        file.write(str(line2))
        file_lenght += len(line1)
        file_lenght += len(line2)
        if file_lenght > 4500 and (index+1) % 5 == 1 and not broken:
            file.write(music)
            file.write(song_title)
            file.write(remaining_links)
            broken = True
    file.close()
