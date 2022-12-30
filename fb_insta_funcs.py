import requests, json, time
from datetime import datetime, timedelta
from config import Facebook
import os


app_secret = Facebook.APP_SECRET
client_id = Facebook.CLIENT_ID
ig_user_id = Facebook.IG_USER_ID

GRAPH_VIDEO_URL = "https://graph-video.facebook.com/"
GRAPH_API_URL = "https://graph.facebook.com/v13.0/"
GRAPH_REEL_URL = "https://rupload.facebook.com/video-upload/v13.0/"


def uploadToFacebook(
    video_path,
    schedule: datetime,
    title="", 
    description=""
    ):
    url = f"{ GRAPH_VIDEO_URL  + Facebook.PAGE_ID }/videos"

    payload = {
        'description': description,
        'title' : title,
        'access_token': Facebook.getPageToken(),
        'scheduled_publish_time': int((schedule+ timedelta(hours=1)).timestamp()),
        'published': False
    }

    files = {'file': open(video_path, 'rb')}
    response = requests.post(url, files=files, params=payload).text
    print(response)
    return response

# def uploadToInstagram(
#     ig_user_id, 
#     access_token, 
#     video_url, 
#     caption=""
#     ):
    
#     url = f"https://graph.facebook.com/v11.0/{ig_user_id}/media?caption={caption}&video_url={video_url}&media_type=VIDEO&access_token={access_token}"
#     response = requests.post(url)
#     print(response.text)
#     creation_id = json.loads(response.text)['id'] 
#     print(creation_id)

#     time.sleep(30)
#     url2  = f"https://graph.facebook.com/v11.0/{ig_user_id}/media_publish?creation_id={creation_id}&access_token={access_token}" 
#     response = requests.post(url2)
#     print(response.text)

def uploadToInstagram(
    video_url, 
    caption=""
    ):
    creation_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media"
    data = {
        "caption" : caption,
        "video_url" : video_url,
        "media_type" : "VIDEO",
        "access_token" : Facebook.getPageToken()
    }
    response = requests.post(creation_url, data=data)
    print(response.text)
    creation_id = json.loads(response.text)['id'] 
    print(creation_id)

    time.sleep(30)
    publish_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media_publish"
    data = {
        "creation_id" : creation_id,
        "access_token" : Facebook.getPageToken()
    }
    response = requests.post(publish_url, data=data)
    print(response.text)
    return response.status_code

def uploadAsFBReel(video_file: str, schedule: datetime):
    # Step 1
    session_url = GRAPH_API_URL + Facebook.PAGE_ID + "/video_reels"
    data = {
        "upload_phase": "start",
        "access_token": Facebook.getPageToken()
    }
    response = requests.post(session_url, data=data)
    
    # Step 2
    upload_url: str = json.loads(response.text)['upload_url']
    video_id = json.loads(response.text)['video_id']
    headers = {
        "Authorization" : "OAuth " +  Facebook.getPageToken(),
        "offset" : '0',
        "file_size": f"{os.path.getsize(video_file)}"
    }
    files = {'file': open(video_file, 'rb')}
    response = requests.post(upload_url, files=files, headers=headers)
    # verify=False

    # Step 3

    # Step 4
    publish_url = GRAPH_API_URL + Facebook.PAGE_ID + "/video_reels"
    data = {
        "upload_phase": "finish",
        "access_token": Facebook.getPageToken(),
        "video_state": "SCHEDULED",
        "description": "",
        "video_id": video_id,
        "scheduled_publish_time":  int((schedule+ timedelta(hours=1)).timestamp())
    }
    response = requests.post(publish_url, data=data)
    print(video_id, response)
    return response


if __name__ == "__main__":
    # res = uploadToFacebook(
    #     '1.mp4',
    #     datetime.now() + timedelta(minutes=15),
    #     title="", 
    #     description=""
    # )
    # print(res)
    # uploadAsFBReel()
    uploadAsFBReel("2.mp4", datetime.now()+timedelta(minutes=15))
    # response = uploadToInstagram("1.mp4")
