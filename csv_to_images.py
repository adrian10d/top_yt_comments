import pandas as pd
from selenium import webdriver
import glob
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from time import sleep


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def generate_htmls(project_path):
    comments_path_csv = project_path + r'\merged_comms_vids.csv'
    htmls_path = project_path + r'\htmls'
    top_comments = pd.read_csv(comments_path_csv)
    f = open('form.html', 'r')
    template = f.read()
    f.close()
    path_to_forms = htmls_path

    for index, comment in top_comments.iterrows():
        f = open(path_to_forms + r'\comment' + str(index + 1) + '.html', 'w', encoding='utf-8')
        content = template
        likes = human_format(comment['likeCount'])
        content = content.replace('_%likes%_', likes)
        content = content.replace('_%author_name%_', str(comment['authorDisplayName']))
        content = content.replace('_%tresc%_', str(comment['textDisplay']))
        content = content.replace('_%author_thumbnail%_', str(comment['authorProfileImageUrl']))
        f.write(content)
        f.close()


def screen_shot_comments(project_path):
    htmls_path = project_path + r'\htmls'
    comment_imgs_path = project_path + r'\comments_imgs'
    filenames = glob.glob(htmls_path + '\*.html')
    driver = webdriver.Chrome()

    for file in filenames:
        driver.get(file)
        sleep(0.5)
        element = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div/div/div')
        location = element.location
        size = element.size
        path = file.replace(htmls_path, comment_imgs_path)
        path = path.replace('html', 'png')
        driver.save_screenshot(path)
        x = location['x']
        y = location['y']
        width = location['x'] + size['width'] + (size['width']/3) + 20 #margin
        height = location['y'] + size['height'] + (size['height']/2) + 10
        im = Image.open(path)
        im = im.crop((x, y, width, height))
        im.save(path)
    driver.quit()


def generate_final_images(project_path):
    csv = project_path + r'\merged_comms_vids.csv'
    comment_imgs_path = project_path + r'\comments_imgs'
    final_path = project_path + r'\final_imgs'
    df = pd.read_csv(csv)
    for index, comment in df.iterrows():
        title = comment['title']
        thumbnail = str(comment['thumbnails.maxres.url'])
        try:
            response = requests.get(thumbnail)
            thumbnail_img = Image.open(BytesIO(response.content))
        except requests.exceptions.MissingSchema:
            thumbnail_img = Image.open(project_path + r'\default.jpg')
        width, height = 1920, 1080
        thumbnail_img = thumbnail_img.resize((width, height))
        draw = ImageDraw.Draw(thumbnail_img)
        draw.rectangle((0, 0, width, 80), fill='black')
        font = ImageFont.truetype("impact.ttf", 46)
        draw.text((80, 17), title, (255, 255, 255), font=font)
        draw.text((width - 100, 17), '#' + str(index + 1), (255, 255, 255), font=font)

        comment_img = Image.open(comment_imgs_path + r'\comment' + str(index+1) + '.png', 'r')
        comm_img_w, comm_img_h = comment_img.size
        comm_img_w = int(comm_img_w * 1.5)
        comm_img_h = int(comm_img_h * 1.5)
        comment_img = comment_img.resize((comm_img_w, comm_img_h))

        offset = ((width - comm_img_w) // 2, (height - comm_img_h) // 2)
        thumbnail_img.paste(comment_img, offset)
        thumbnail_img.save(final_path + r'\i' + str(index+1) + '.jpg')

