import requests, json, time
from datetime import datetime, timedelta
from config import Facebook, GoogleConfig
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
import sys


app_secret = Facebook.APP_SECRET
client_id = Facebook.CLIENT_ID
ig_user_id = Facebook.IG_USER_ID

GRAPH_VIDEO_URL = "https://graph-video.facebook.com/"
GRAPH_API_URL = "https://graph.facebook.com/v13.0/"
GRAPH_REEL_URL = "https://rupload.facebook.com/video-upload/v13.0/"
TOTAL_HASHTAG_SETS = 10


def videoUploadFacebook(video_path: str, 
    schedule: datetime = datetime.now() + timedelta(minutes=15),
    title: str ="", 
    description: str =""
    ):
    url = GRAPH_VIDEO_URL  + Facebook.PAGE_ID + "/videos"

    payload = {
        'description': description,
        'title' : title,
        'access_token': Facebook.getPageToken(),
        'scheduled_publish_time': int(schedule.timestamp()),
        'published': False
    }

    files = {'file': open(video_path, 'rb')}
    response = requests.post(url, files=files, params=payload)
    return response

def videoUploadInstagram(video_url, caption="", 
    schedule = datetime.now() + timedelta(minutes=15)
    ):
    creation_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media"
    data = {
        "caption" : caption,
        "video_url" : video_url,
        "media_type" : "VIDEO",
        "access_token" : Facebook.getPageToken()
    }
    response = requests.post(creation_url, data=data)
    creation_id = json.loads(response.text)['id'] 
    print(creation_id)

    time.sleep(30)
    publish_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media_publish"
    data = {
        "creation_id" : creation_id,
        "access_token" : Facebook.getPageToken(),
        # 'scheduled_publish_time': int(schedule.timestamp()),
        # 'published': False
    }
    response = requests.post(publish_url, data=data)
    return response

def reelUploadInstagram(video_url, caption="", 
    schedule = datetime.now() + timedelta(minutes=15),
    share_to_feed: bool = True
    ):
    creation_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media"
    data = {
        "caption" : caption,
        "video_url" : video_url,
        "media_type" : "REELS",
        "access_token" : Facebook.getPageToken(),
        "share_to_feed": share_to_feed
    }
    response = requests.post(creation_url, data=data)
    creation_id = json.loads(response.text)['id'] 
    print(creation_id)

    time.sleep(30)
    publish_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media_publish"
    data = {
        "creation_id" : creation_id,
        "access_token" : Facebook.getPageToken(),
        # 'scheduled_publish_time': int(schedule.timestamp()),
        # 'published': False
    }
    response = requests.post(publish_url, data=data)
    return response

def imageUploadInstagram(image_url, caption=""):
    creation_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media"
    data = {
        "caption" : caption,
        "image_url" : image_url,
        "access_token" : Facebook.getPageToken()
    }
    response = requests.post(creation_url, data=data)
    creation_id = json.loads(response.text)['id'] 
    print(creation_id)

    time.sleep(15)
    publish_url = "https://graph.facebook.com/v11.0/" + Facebook.IG_USER_ID + "/media_publish"
    data = {
        "creation_id" : creation_id,
        "access_token" : Facebook.getPageToken(),
    }
    response = requests.post(publish_url, data=data)
    return response

def reelUploadFacebook(video_file: str, schedule: datetime, description: str =""):
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
    print(sys.getsizeof(files))
    response = requests.post(upload_url, data=files, headers=headers)
    # verify=False

    # Step 3

    # Step 4
    publish_url = GRAPH_API_URL + Facebook.PAGE_ID + "/video_reels"
    data = {
        "upload_phase": "finish",
        "access_token": Facebook.getPageToken(),
        "video_state": "SCHEDULED",
        "description": description,
        "video_id": video_id,
        "scheduled_publish_time":  int(schedule.timestamp())
    }
    response = requests.post(publish_url, data=data)
    print(video_id, response)
    return response

def mediaUploadDrive(save_path: str, video_title: str):    
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("drive_credentials.json")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        try:
            gauth.Refresh()
            gauth.Authorize()    
        except:
            gauth.LocalWebserverAuth()
    else:
        # Initialize the saved creds
        gauth.Refresh()
        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile("drive_credentials.json")
    drive = GoogleDrive(gauth)
    
    # Upload Drive
    f = drive.CreateFile({
        'title': video_title,
        "parents" : [{'id': GoogleConfig.DRIVE_PARENT_ID}]
        })

    f.SetContentFile(save_path)
    f.Upload()
    file_id = f.metadata.get('id')
    f = None
    return file_id

def URLFromDriveID(file_id: str) -> str:
    url = "https://drive.google.com/uc?id=" + file_id
    response = requests.get(url)
    return response.url

if __name__ == "__main__":
    # response = videoUploadFacebook("1.mp4")
    # response = reelUploadFacebook("2.mp4")

    # image_url = "https://drive.google.com/uc?id=1l8H-Gkaqf3lEPNWUrQlLDUnarkMY1Xc0"
    # response = requests.get(image_url)
    # response = imageUploadInstagram(response.url)

    # video_url = "https://drive.google.com/uc?id=1NEA3nAceOW1wIbNuLYHF64BRwmBuPMG5"
    # response = requests.get(video_url)
    # response = reelUploadInstagram(response.url)
    # # response = videoUploadInstagram(response.url)

    response = mediaUploadDrive("TESTING.jpeg", "Test_Image.jpeg")
    print(response)
