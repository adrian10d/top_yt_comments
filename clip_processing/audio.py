import pandas as pd
import pyttsx3
from bs4 import BeautifulSoup
import demoji


def get_rid_of_html(string):
    soup = BeautifulSoup(string)
    return soup.get_text()


def comments_to_mp3(project_path, words_per_minute, language):
    demoji.download_codes()
    lang_id = None
    if language == 'eng':
        lang_id = 1
    elif language == 'spa':
        lang_id = 2
    elif language == 'pl':
        lang_id = 0
    elif language == 'de':
        lang_id = 4
    comments_path = project_path + r'\merged_comms_vids.csv'
    comments_df = pd.read_csv(comments_path)
    audio_path = project_path + r'\audio'
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[lang_id].id)
    engine.setProperty('rate', words_per_minute)
    for index, comment in comments_df.iterrows():
        text = get_rid_of_html(comment['textDisplay'])
        text = demoji.replace(text, '')
        engine.save_to_file(text, audio_path + r'\audio' + str(index+1) + '.mp3')
        engine.runAndWait()


def manually_test_to_mp3(string, path, words_per_minute, language):
    lang_id = None
    if language == 'm_eng':
        lang_id = 1
    elif language == 'm_spa':
        lang_id = 2
    elif language == 'f_pl':
        lang_id = 0
    elif isinstance(language, int):
        lang_id = language
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[lang_id].id)
    engine.setProperty('rate', words_per_minute)
    engine.save_to_file(string, path + r'\audio.mp3')
    engine.runAndWait()


def show_languages():
    engine = pyttsx3.init()
    sound = engine.getProperty('voices')  # list of voices along with id
    for voice in sound:
        print(voice)
