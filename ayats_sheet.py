import ezsheets
from datetime import datetime, timedelta

from ayat_compile import ayat_compile_Urdu_English
from SocialUpload import mediaUploadDrive, TOTAL_HASHTAG_SETS

from quranic import getEnglishText, downloadAudioUrdu
from surah_list import surah_dict
import re
from config import GoogleConfig, TOTAL_HASHTAG_SETS

ss = ezsheets.Spreadsheet(GoogleConfig.SPREADSHEET_ID)


ayat_sheet = ss['Hidayat Mania']
stats = ss['Stats']
insta_sheet = ss['Instagram']

PST_TIME_SCHEDULE = sorted([11, 17, 22])


#from datetime import date
#d0 = date(2017, 8, 18)
#d1 = date(2017, 10, 26)
#delta = d1 - d0
#print(delta.days)

#cdate = datetime.strptime('1999-9-9 09:09:09', '%Y-%m-%d %H:%M:%S') 
def scheduleUpdate(scheduled_last):
    scheduled_last = scheduled_last if scheduled_last else str(datetime.now())
    scheduled_last = datetime.strptime(scheduled_last.split('.')[0], '%Y-%m-%d %H:%M:%S')

    if (scheduled_last.hour < PST_TIME_SCHEDULE[0]):
        schedule_new = scheduled_last.replace(hour = PST_TIME_SCHEDULE[0])
    elif (scheduled_last.hour >= PST_TIME_SCHEDULE[-1]):
        schedule_new = scheduled_last.replace(hour = PST_TIME_SCHEDULE[0]) + timedelta(days=1)
    else:
        for i, hr in enumerate(PST_TIME_SCHEDULE):
            if scheduled_last.hour >= hr:
                schedule_new = scheduled_last.replace(hour = PST_TIME_SCHEDULE[i+1])


    if ( schedule_new < datetime.now()  ):
        schedule_new = scheduleUpdate(str(datetime.now()))

    return schedule_new

def getVideoNumber(col_to_look):
    return int(ayat_sheet[f'{col_to_look}1'])

def getSuratNumber(col_to_look):
    return int(ayat_sheet[f'{col_to_look}2'])

def getAyatRange(col_to_look):
    ayat_range = ayat_sheet[f'{col_to_look}3'].split('-')
    return [i for i in range(int(ayat_range[0]), 1 + int(ayat_range[-1]) )]

def getVideoCategory(col_to_look):
    vid_catg = ayat_sheet[f'{col_to_look}4']
    return 'general' if not vid_catg else vid_catg

def getLastSchedule():
    return stats['E5']

def getTotalVideosDone():
    return int(stats['B5'])

def setTotalVideosDone(total_videos_done):
    stats['B5'] = total_videos_done + 1

def getColToLook(total_videos_done):
    to_find = total_videos_done + 1
    return ezsheets.getColumnLetterOf(to_find+2)

def getStartStatus(col_to_look):
    return ayat_sheet[f'{col_to_look}7'].lower()

def getWorkingStatus(col_to_look):
    return ayat_sheet[f'{col_to_look}8']

def setWorkingStatus(col_to_look, value):
    ayat_sheet[f'{col_to_look}8'] = value

def setVideoSavePath(col_to_look, save_path):
    ayat_sheet[f'{col_to_look}9'] = save_path

def getVideoSavePath(col_to_look):
    return ayat_sheet[f'{col_to_look}9']

def setVideoSchedule(col_to_look, shedule_to_write):
    ayat_sheet[f'{col_to_look}10'] = str(shedule_to_write)

def setScheduleStats(shedule_to_write):
    stats['E5'] = str(shedule_to_write)
    
def generateNameForDrive(video_number, save_path, shedule_to_write ):
    hashtag_set_num = (video_number % TOTAL_HASHTAG_SETS) + 1
    vid_title = re.sub('[:\-\s]','_', str(shedule_to_write).split('.')[0])
    vid_title = f"{vid_title}_Set_{hashtag_set_num}"
    vid_title = vid_title + f"{'_IGTV.mp4' if 'IGTV' in save_path else '.mp4'}"
    return vid_title

def getHashtagSetInstagram(video_number) -> list(str):
    return insta_sheet.getColumn((video_number % TOTAL_HASHTAG_SETS) + 1)[1:11]

def main():
    TOTAL_VIDEOS_DONE = getTotalVideosDone()
    SCHEDULED_LAST = getLastSchedule() #Schedule of LAST in str
    col_to_look = getColToLook(TOTAL_VIDEOS_DONE)
    vid_no = getVideoNumber(col_to_look)
    surah_no = getSuratNumber(col_to_look)
    ayat_range = getAyatRange(col_to_look)
    vid_catg = getVideoCategory(col_to_look)
    vid_start = getStartStatus(col_to_look)

    #print(vid_no,fact_title, facts_text, fact_tags, vid_catg, vid_desc, vid_start)
    
    if (vid_start == 'yes') :
        #working status update

        if getWorkingStatus(col_to_look) != 'Compiled':
            setWorkingStatus(col_to_look, 'Under Process')

            try_no = 0
            while True:
                try:
                    try_no += 1
                    texts = getEnglishText(surah_no, ayat_range)
                    audio_list = downloadAudioUrdu(surah_no, ayat_range)
                    break
                except Exception as e:
                    print(e)
                    if try_no >= 3:
                        raise Exception("TEXT & Audio ISSUE")
                    else:
                        pass

            try_no = 0
            while True:
                try:
                    try_no += 1
                    save_path = ayat_compile_Urdu_English(surah_no, ayat_range, texts, audio_list, vid_catg=vid_catg)
                    break
                except Exception as e:
                    print("Compile Error is -> ",e)
                    if try_no >= 3:
                        raise Exception("Compilation Error")
                    else:
                        pass

            print(save_path)
            
            setWorkingStatus(col_to_look, 'Compiled')
            setVideoSavePath(col_to_look, save_path)
        else:
            save_path = getVideoSavePath(col_to_look)

        shedule_to_write = scheduleUpdate(SCHEDULED_LAST)
        setVideoSchedule(col_to_look, shedule_to_write)
        mediaUploadDrive(
            save_path, 
            generateNameForDrive(vid_no, save_path, shedule_to_write)
        )
        setWorkingStatus(col_to_look, 'Uploaded')
        setTotalVideosDone(TOTAL_VIDEOS_DONE)
        setScheduleStats(shedule_to_write)

    ayat_sheet.refresh()
    stats.refresh()
        
if __name__ == "__main__":
    for i in range(1):
        main()
    

