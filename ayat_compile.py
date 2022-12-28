import os
from datetime import datetime
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips, clips_array, vfx, CompositeVideoClip, CompositeAudioClip, TextClip, ImageSequenceClip, concatenate_audioclips
import json 
from PIL import Image, ImageDraw, ImageFont
from surah_list import surah_dict

# max 22 chrs in a line

MAX_LINE_LENGTH = 50
percentwidth_per_tc = .95 / MAX_LINE_LENGTH
TEXT_RGB = (255,255,255) # white
BG_RGB = (0,0,0)    #black
TEXT_SIZE = 40
HEADING_SIZE = 35
TITLE_SIZE = 20
TITLE_TEXT = "HIDAYAT MANIA"
TITLE_RECTANGLE_RGB = (255,255,255, 70)


def makeLines(text):
    lines = []
    words = text.split(' ')
    line = ''
    for word in words:
        if len(f"{line} {word}") <= MAX_LINE_LENGTH:
            line =f"{line} {word}"
        else: 
            lines.append(line)
            line = ''
    if line:
        lines.append(line)

    return lines

def chooseVideo(vid_catg):
    vid_catg = vid_catg.lower()

    with open('vid_record.json') as json_file:
        video_dictionary = json.load(json_file)
    json_file.close()
    
    if vid_catg in video_dictionary:
        dir_to_choose = video_dictionary[vid_catg]["directory"]

        dir_to_choose = os.path.join(os.getcwd(),dir_to_choose)
        print(dir_to_choose)

        videos_list = os.listdir(dir_to_choose)
        path_list = [
            os.path.join(dir_to_choose, video_file) for video_file in videos_list
            ]
        path_list.sort(key = os.path.getctime)
        #print(path_list)

        vid_index = video_dictionary[vid_catg]["index"]
        vid_to_choose = path_list[vid_index]
        video_dictionary[vid_catg]["index"] = (vid_index + 1) % len(videos_list)

        with open('vid_record.json', 'w') as outfile:
            json.dump(video_dictionary, outfile)

        # print("Video To Choose -->",vid_to_choose)
        return  vid_to_choose
    else:
        return "error"

def makeImageClipsUrduEng(surah, ayaat, texts, width, height):
    #   BG CLIP 
    bg_height = 1340
    img = Image.new('RGBA', (width, bg_height), (0, 0, 0))
    d = ImageDraw.Draw(img)

    bg_text = f"CHAP {surah} : VERSE NO"
    if ayaat[0] != ayaat[-1]:
        bg_text = f"{bg_text} {ayaat[0]}-{ayaat[-1]}"
    else:
        bg_text = f"{bg_text} {ayaat[0]}"

    fnt = ImageFont.truetype('arial.ttf', HEADING_SIZE)
    w,h = d.textsize(bg_text, fnt)
    d.text(((width-w)/2, int((132-h)/2.0) ), bg_text, font=fnt, fill=TEXT_RGB)

    img.save('Ayaat_Images\\screen_bg.png', 'PNG')

    #Title Clip
    img = Image.new('RGBA', (width, bg_height), (0, 0, 0, 60))
    d = ImageDraw.Draw(img)
    
    fnt = ImageFont.truetype('arial.ttf', TITLE_SIZE)
    w,h = d.textsize(TITLE_TEXT, fnt)

    d.rounded_rectangle((
    0, 0, 
    width, bg_height), fill=(0, 0, 0, 0), outline="white", width=5, radius=0)

    d.rounded_rectangle((
        ((width-w)/2) - (0.01 * width), 
        (.15 * height - .01*height) + 130, 
        ((width-w)/2) + w + (0.01 * width), 
        (.15 * height + h + .01*height) + 130
        ), fill=TITLE_RECTANGLE_RGB, outline=TITLE_RECTANGLE_RGB, width=2, radius=0)
            
    d.text(((width-w)/2, height * .15 + 130), TITLE_TEXT, font=fnt, fill="black")
            
    img.save('Ayaat_Images\\title.png', 'PNG')

    # Ayat text Image
    for no, text in enumerate(texts):
        img = Image.new('RGBA', (width, height), (255, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        global MAX_LINE_LENGTH
        MAX_LINE_LENGTH = {1920: 80, 1080:50}[width]

        lines = makeLines(text)
        no_of_lines = len(lines)
        
        fnt = ImageFont.truetype('arial.ttf', TEXT_SIZE)
        w,h = d.textsize(lines[0], fnt)
        t_h = no_of_lines * (h) + (no_of_lines-1) * (.03 * height )
        #lines
        for line_no, line in enumerate(lines):
            if line[0] == ' ':
                line = line[1:]
            print (line_no,'\t',line)                   
            fnt = ImageFont.truetype('arial.ttf', TEXT_SIZE)
            w,h = d.textsize(line, fnt)
            if w>width:
                print("wad gaye je")
            
            d.rounded_rectangle((
                ((width-w)/2) - (0.02 * width), 
                ((height-t_h)/2) + line_no *(h+.03*height) - (.02 * height), 
                ((width-w)/2) + w + (0.02 * width), 
                ((height-t_h)/2) + line_no *(h+.03*height) + h + .02* height 
                ), fill=BG_RGB, outline=BG_RGB, width=2, radius=10)
            
            d.text(((width-w)/2, ((height-t_h)/2) + line_no *(h+.03*height)), line, font=fnt, fill=TEXT_RGB)
                
        img.save(f'Ayaat_Images\\ayat{no}.png', 'PNG')

    #Share Screen
    img = Image.new('RGBA', (width, height), (255, 0, 0, 0))
    d = ImageDraw.Draw(img)
        
    lines = ["For Support Please Share and Subscribe","JAZAKALLAH"]
    no_of_lines = len(lines)
    
    fnt = ImageFont.truetype('arial.ttf', TEXT_SIZE)
    w,h = d.textsize(lines[0], fnt)
    t_h = no_of_lines * (h) + (no_of_lines-1) * (.03 * height )
    #lines
    for line_no, line in enumerate(lines):
        print (line_no,'\t',line)                   
        fnt = ImageFont.truetype('arial.ttf', TEXT_SIZE)
        w,h = d.textsize(line, fnt)
        
        d.rounded_rectangle((
            ((width-w)/2) - (0.02 * width), 
            ((height-t_h)/2) + line_no *(h+.03*height) - (.02 * height), 
            ((width-w)/2) + w + (0.02 * width), 
            ((height-t_h)/2) + line_no *(h+.03*height) + h + .02* height 
            ), fill=BG_RGB, outline=BG_RGB, width=2, radius=10)
        if line_no == 0:
            color = "yellow"
        else:
            color = TEXT_RGB
        d.text(((width-w)/2, ((height-t_h)/2) + line_no *(h+.03*height)), line, font=fnt, fill=color)
            
    img.save('Ayaat_Images\\share.png', 'PNG')

def checkTotalDuration(audio_list):
    total_duration = 0
    for audio in audio_list:
        audio_clip = AudioFileClip(audio)
        total_duration = total_duration + audio_clip.duration
        audio_clip.close()
    print("Total Duration--> ",total_duration+5)
    return 1920 if (total_duration + 5) > 60 else 1080

def ayat_compile_Urdu_English(surah, ayaat, ayat_texts_english, audio_list, vid_catg="general"):
    video_to_use = chooseVideo(vid_catg) ### --> Check and customize accordingly
    if (video_to_use == "error"):
        return "error"
    vid_clip = VideoFileClip(video_to_use)
    width, height= vid_clip.size
    print("1--> ",width,height)
    
    
    new_height = 1080
    new_width = checkTotalDuration(audio_list)
    if width < height:
        vid_clip = vid_clip.resize(width = new_width)
    else:
        vid_clip = vid_clip.resize(height = new_height)

    width, height = vid_clip.size
    print("2--> ",vid_clip.size)
    x_1 = (width - new_width) /2
    y_1 = (height - new_height)/2
    print ("x1-->",x_1,"y__1",y_1)
    vid_clip = vid_clip.crop(x1 = x_1, y1 = y_1, x2 = x_1 + new_width, y2 = y_1 + new_height)

    print("3--> ",vid_clip.size)

    image_clips_with_text = makeImageClipsUrduEng(surah, ayaat, ayat_texts_english, new_width, new_height)
    #Bg Screen - youtube - Insta Crop | Screen per ayat -- english | title screen

    bg_clip = ImageClip("Ayaat_Images\\screen_bg.png")
    title_clip = ImageClip("Ayaat_Images\\title.png")
    share_clip = ImageClip("Ayaat_Images\\share.png").set_duration(4)
    image_clips_list = []

    start_time_list = [0]
    texts_duration_total = 0
    
    audio_clips = []
    
    for i in range(len(ayat_texts_english)):
        audio_clips.append(AudioFileClip(audio_list[i]))
        durate = audio_clips[i].duration
        img_clip_itr = ImageClip(f"Ayaat_Images\\ayat{i}.png")#.set_duration(durate-0.3)
        
        texts_duration_total = texts_duration_total + durate
        start_time_list.append(start_time_list[-1] + durate)
        image_clips_list.append(img_clip_itr)

    vid_clip = vid_clip.subclip(0.5, int(vid_clip.duration)-0.5)
    print("VID CLip duration-->", vid_clip.duration,"\nText Duration Total-->",texts_duration_total)


    if vid_clip.duration < (texts_duration_total+2+4):
        times = (texts_duration_total +2+4) / vid_clip.duration
        times = int(times)
        clip1 = vid_clip
        clip2 = vid_clip.fx( vfx.time_mirror)
        concatenate_list = []
        for i in range(times+1):
            if i % 2 == 0:
                concatenate_list.append(clip1)
            else:
                concatenate_list.append(clip2)
        vid_clip = concatenate_videoclips(concatenate_list, method = 'compose')
    vid_clip = vid_clip.subclip(0, int(texts_duration_total) +1+4).fadeout(1)        

    """
    if vid_clip.duration < (texts_duration_total+2+4):
        while vid_clip.duration < (texts_duration_total+2+4): 
            vid_clip = vid_clip.fx( vfx.time_symmetrize)
    vid_clip = vid_clip.subclip(0, int(texts_duration_total) +1+4).fadeout(1)        
    """
    #print("4--> ",vid_clip.size)

    #title_clip , image clips, vid_clips ---> 4:4 | bg_clip 4:5
    composit_list = [bg_clip.set_end(texts_duration_total + 0.5+4), vid_clip.set_position("center"), title_clip.set_position("center").set_end(texts_duration_total + 1.5+4)] + [image_clips_list[i].set_position("center").set_start(start_time_list[i] + (i * 0.1) ).set_end(start_time_list[i+1]) for i in range(len(image_clips_list))] + [share_clip.set_start(texts_duration_total + 1).set_end((texts_duration_total + 0.5+3.5)).set_position("center")]

    final_clip = CompositeVideoClip(composit_list)#, size=(new_width,new_height))
    
    final_clip = final_clip.set_audio(None)

    print("6--> ",final_clip.size)

    aud_clip = concatenate_audioclips(audio_clips)
    aud_clip = CompositeAudioClip(
        [
            aud_clip,
            AudioFileClip("BG_Audios\\bg_3.mp3")
                .volumex(.85)
                .subclip(0,texts_duration_total+1+4)
        ]
    )
    final_clip = final_clip.set_audio(aud_clip)

    
    save_path = f'Videos\\1_Compiled_Videos\\CHAP_{surah}_VERSE_{ayaat}'
    fps1 = 24
    if new_width == 1920:
        save_path = save_path + '_IGTV'
        fps1 = 30
    save_path = save_path +'.mp4'
    try:
        final_clip.write_videofile(save_path, fps = fps1, threads = 8, audio_codec = 'aac')
    except Exception as e:
        print("Error is -->\n", e)
    final_clip.close()
    vid_clip.close()

    return save_path


if __name__ == "__main__":
    surah = 1
    ayaat = [1,2,3,4,5,6,7]
    from quranic import getEnglishText
    texts = getEnglishText(surah, ayaat)
    from quranic import downloadAudioUrdu
    audio_list = downloadAudioUrdu(surah, ayaat)

    ayat_compile_Urdu_English(surah, ayaat, texts, audio_list, vid_catg="general")

