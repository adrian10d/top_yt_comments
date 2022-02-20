import os
import googleapiclient.discovery
import pandas as pd


def videos_to_csv(playlist_id, project_path):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    videos_path = project_path + r'\videos.csv'

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBVyl6BDwsnj0irkM_Fj0TGY8ZbpMCCP5w"

    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=DEVELOPER_KEY
    )

    # Pierwszy wynik - tu podane tokeny kolejnych stron
    request = youtube.playlistItems().list(
        part="id, snippet",
        playlistId=playlist_id,
        maxResults=50,
        pageToken=None
    )
    items = []
    # Wynik zapytania ze strony
    response = request.execute()
    # Liczba itemów to maksymalnie maxResults
    for item in response['items']:
        items.append(item['snippet'])

    # Weź token do następnej strony
    try:
        next_page_token = response['nextPageToken']
    except KeyError:
        next_page_token = None

    while next_page_token:
        request = youtube.playlistItems().list(
            part="id, snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            items.append(item['snippet'])
        try:
            next_page_token = response['nextPageToken']
        except KeyError:
            break
    # Interesujące pola
    fields = ['title', 'resourceId.videoId', 'thumbnails.maxres.url']
    # Znormalizowany JSON
    df = pd.json_normalize(items)
    df = df[fields]
    df.to_csv(videos_path, index=False)

