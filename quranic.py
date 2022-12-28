import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By

#from webdriver_manager.chrome import ChromeDriverManager

# tested 23
def make3DigitsStr(x):
    x = str(x).strip()
    return '0' * (3-len(x)) + x

def downloadAudioAyaat(surah, ayaat, qari="Ghamadi_40kbps"):
    surah = make3DigitsStr(surah)
    ayaat = [make3DigitsStr(ayat) for ayat in ayaat]

    for ayat in ayaat:
        url = f"https://everyayah.com/data/{qari}/{surah}{ayat}.mp3"
        r = requests.get(url, allow_redirects=True)

        filename = url.split('/')[-1]
        open(filename, 'wb').write(r.content)

    return surah, ayaat

# tested 23
def downloadAudioUrdu(surah, ayaat, qari="translations/urdu_shamshad_ali_khan_46kbps"):
    surah = make3DigitsStr(surah)
    ayaat = [make3DigitsStr(ayat) for ayat in ayaat]

    filenames = []
    for ayat in ayaat:
        url = f"https://everyayah.com/data/{qari}/{surah}{ayat}.mp3"
        r = requests.get(url, allow_redirects=True)

        filename = f"Ayaat_Audio\\Urdu_{surah}{ayat}.mp3"
        filenames.append(filename)
        open(filename, 'wb').write(r.content)

    return filenames

def getArabicText(surah, ayaat):
    surah = make3DigitsStr(surah)
    url = f"https://al-quran.info/#{surah}"

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    
    time.sleep(2)
    arabic_ayaat = []
    ayaat = [make3DigitsStr(ayat) for ayat in ayaat]
    for ayat in ayaat:
        elem = browser.find_element_by_id("a"+ayat)
        elem = elem.find_element_by_xpath('..')
        elem = elem.find_element_by_class_name("quran-content")
        arabic_ayaat.append(elem.get_attribute('innerHTML')[::-1])
    return arabic_ayaat

# tested 23
def getEnglishText(surah, ayaat):
    surah = make3DigitsStr(surah)
    url = "https://ahadees.com/english-surah-"+surah+".html"
    
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    browser = webdriver.Chrome(options=chrome_options, executable_path=r'D:\Summer Projects\Hidayat Mania\chromedriver.exe')
    browser.get(url)
    
    time.sleep(2)
    eng_ayaat = []
    ayaat = [int(ayat) for ayat in ayaat]
    for ayat in ayaat:
        elem = browser.find_elements(By.CLASS_NAME,"MsoNormal")[ayat-1]
        eng_ayaat.append(elem.text)
    return eng_ayaat

def getUrduText(surah, ayaat):
    surah = make3DigitsStr(surah)
    url = f"https://www.searchtruth.com/chapter_display.php?chapter={surah}&translator=17"
    
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    
    time.sleep(2)
    urdu_ayaat = []
    for ayat in ayaat:
        elem = browser.find_element_by_id(str(ayat))
        urdu_ayaat.append(elem.text[::-1])
    return urdu_ayaat

if __name__ == "__main__":
    # downloadAudioAyaat(1,[1,2])
    x = getEnglishText(1,[1,2,3,4,5,6,7])
    print(x)