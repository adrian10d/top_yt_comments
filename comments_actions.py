import os
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import pandas as pd


def get_comments_from_vid(video_id, max_pages):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = ""

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id, snippet",
        order="relevance",
        videoId=video_id,
        pageToken=None
    )
    items = []
    response = request.execute()
    for item in response['items']:
        items.append(item['snippet']['topLevelComment']['snippet'])

    # Numeracja, żeby nie brać wszystkich komentarzy
    page = 1
    # Weź token do następnej strony
    try:
        next_page_token = response['nextPageToken']
    except KeyError:
        next_page_token = None

    while next_page_token:
        if page == max_pages:
            break
        request = youtube.commentThreads().list(
            part="id, snippet, replies",
            order="relevance",
            videoId=video_id,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            items.append(item['snippet']['topLevelComment']['snippet'])
        page += 1

        try:
            next_page_token = response['nextPageToken']
        except KeyError:
            break

    fields = ['textDisplay', 'authorDisplayName', 'authorProfileImageUrl', 'likeCount', 'videoId']
    df = pd.json_normalize(items)
    df = df[fields]
    return df


def all_comments_to_df(project_path, comment_pages):
    comments_path = project_path + '\comments.csv'
    backup_path = project_path + r'\backup.csv'
    videos_path = project_path + r'\videos.csv'
    vids_df = pd.read_csv(videos_path)
    numb_of_vids = len(vids_df.index)
    comments_df_list = []
    progress = 0
    for index, vid in vids_df.iterrows():
        try:
            temp_df = get_comments_from_vid(vid['resourceId.videoId'], comment_pages)
            comments_df_list.append(temp_df)
        except (HttpError, KeyError):
            comments_df = pd.concat(comments_df_list)
            comments_df.to_csv(backup_path, index=False)
            continue
        progress += 1
        progress_line = str(progress) + '/' + str(numb_of_vids)
        print(progress_line)
    comments_df = pd.concat(comments_df_list)
    comments_df.to_csv(comments_path, index=False)


def get_top_comments(project_path, head, channel_name):
    comments_path = project_path + r'\comments.csv'
    top_comments_path = project_path + r'\top_comments.csv'
    comments_df = pd.read_csv(comments_path)
    comments_df = comments_df[~comments_df['authorDisplayName'].str.contains(channel_name, na=False)]
    comments_df = comments_df[~comments_df['textDisplay'].str.len().gt(500)]
    comments_df = comments_df.sort_values(by=['likeCount'], ascending=False).reset_index(drop=True)
    comments_df = comments_df.head(head)
    comments_df.to_csv(top_comments_path, index=False)


def merge_comments_on_vids(project_path):
    videos_path = project_path + r'\videos.csv'
    comments_path = project_path + r'\top_comments.csv'
    merged_comms_vids_path = project_path + r'\merged_comms_vids.csv'
    comments_df = pd.read_csv(comments_path)
    videos_df = pd.read_csv(videos_path)
    result = comments_df.merge(videos_df, left_on='videoId', right_on='resourceId.videoId')
    result = result.sort_values(by=['likeCount'], ascending=False).reset_index(drop=True)
    result = result.drop(['resourceId.videoId'], axis=1)
    result.to_csv(merged_comms_vids_path, index=False)
