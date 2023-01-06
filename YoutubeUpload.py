import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta
from config import GoogleConfig

def serviceName(vid_num: int):
    CLIENT_SECRET_FILE = GoogleConfig.getCredentialsFile(vid_num)
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    return Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def uploadYoutube(
    filename: str, 
    title: str, 
    description: str, 
    tags: list, 
    vid_num: int, 
    schedule: datetime,
    category_id: int =22,
    thumbnail: str =None 
    ):

    upload_date_time = (schedule - timedelta(hours=5)).isoformat()# + '.000Z'

    service = serviceName(vid_num)
    
    request_body = {
        'snippet': {
            'categoryId': category_id,
            'title': title,
            'description': description,
            'tags': tags #['Travel', 'video test', 'Travel Tips']
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(filename)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    if thumbnail != None:
        service.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload(thumbnail)
        ).execute()

if __name__ == "__main__":
    save_path = '1.mp4'
    uploadYoutube(
        save_path,
        "Quran",
        "Test",
        ["1","2","3"],
        23,
        datetime.now() + timedelta(hours=2),
        22,
        None
    )

