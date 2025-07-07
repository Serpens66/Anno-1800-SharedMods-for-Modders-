# Python ModOp code snippets for various purposes

The code is made for my own purposes, so you may need to adjust it for your purpose.  
If you don't know python that may be too difficult for you.  

- [featchsoundfiles](#featchsoundfiles)
- [upload_modio](#upload_modio)
- [create_hardlinks](#create_hardlinks)


###  featchsoundfiles
- Converting mp3 to wav and get duration of audio and audio speach to text (needs https://ffmpeg.org/download.html)

  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```python
  # Dem Skript eine Liste von Dateinamen geben und diese soll es dann aus den extrahierten 1404 Sound Dateien zusammenkopieren
  # (da wir nicht alle Sounds brauchen). Evlt auch noch in wav Datei konvertieren.
  # Und wenn möglich sogar Den Text der sounddatei schreiben


  ######################################################################################


  import subprocess
  import pathlib
  # pip install SpeechRecognition , braucht wohl internet und nutzt google https://thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
  import speech_recognition as sr
  from datetime import datetime
  import traceback
  import time
  import json
  # optional: pip install python-ffmpeg, but it saves the hassle to deal with this stupid command line formatting (still needs the ffmpeg exe file in path)
  # https://python-ffmpeg.readthedocs.io/en/stable/examples/querying-metadata/
  # https://python-ffmpeg.readthedocs.io/en/stable/api/
  from ffmpeg import FFmpeg

  ######################################################################################


  # durch das "r" vorm string sind auch die \ erlaubt. (ansonsten müsste man sie durhc / oder \\ ersetzen, damit python damit klarkommt)

  anno1404sounds = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Anno1800 RDA unpacked\Anno 1404 speech and icons"
  wavoutputfolder = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Wwise Soundtool\ann1404wav_spy"

  SoundToUse = {
    "spy":[40704702,40705500,40705501,40705502,40705600,40705601,40705602,40705700,40705701,40705702,40700000,40700001,40700002,40700003,40700004,40700100,40700101,40700102,40700200,40700201,40700202,40700203,40700204,40700300,40700301,40700302,40700303,40700304,40700400,40700401,40700402,40700500,40700501,40700502,40700503,40700504,40700600,40700601,40700602,40700603,40700604,40700605,40700606,40700607,40700608,40700609,40700800,40700801,40700802,40701100,40701101,40701102,40701200,40701201,40701202,40701300,40701302,40701500,40702000,40702001,40702002,40702300,40702301,40702302,40702600,40702601,40702602,40702900,40702901,40702902,40703800,40703801,40703802,40704100,40704101,40704102,40704400,40704401,40704402,40704700,40704701,],
    "narrator":[40250000,40250001,40250008,40250009,40250020,40250021,40250022,40250026,40250027,40250028,40250029,40250030,40250031,40250032,40250033,40250034,40250035,40250036,40250105,40250108,40250109,5002441,5002450,5002451,5002380,5002381,5002390,5002391,5002400,5002401,5002430,5002431,5002440,],
    "revoluzzer":[40720005,40720006,40720007,40720008,40720009,],
  }
  AllSounds = []
  for k,v in SoundToUse.items():
    for i,item in enumerate(v):
      v[i] = str(item)
    AllSounds += v

  # keine ahnung ob eng US oder GB ist, gucken wir mal US
  # man könnte aber auch mal das ergebnis vergleichen obs identisch ist
  # supported languages and their code: https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages?hl=de
  Languages = {
    "ger":{"official":"de-DE","annoxml":"German"},"eng":{"official":"en-US","annoxml":"English"},
    "fra":{"official":"fr-FR","annoxml":"French"},"esp":{"official":"es-ES","annoxml":"Spanish"},
    "ita":{"official":"it-IT","annoxml":"Italian"},"rus":{"official":"ru-RU","annoxml":"Russian"},
  }
  OtherLanguages = {"Polish","Chinese","Taiwanese","Japanese","Korean"} # using english for them




  ######################################################################################

  r = sr.Recognizer()


  # https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#recognizer_instancerecognize_googleaudio_data-audiodata-key-unionstr-none--none-language-str--en-us--pfilter-union0-1-show_all-bool--false---unionstr-dictstr-any
  # Irgendwo soll wohl das API Limit stehen mit: https://stackoverflow.com/questions/71121167/googles-speech-recognition-api-recognize-google-function-in-python-usage-limi
      # The current API usage limits for Speech-to-Text are as follows:
      # 900 requests per 60 seconds
      # Processing per day: 480 hours of audio

  # extrem simple api call limit system, just wait a minute after each 900 calls
  class Limiter:
    def __init__(self,maxperminute):
      self.maxperminute = maxperminute
      self.calllimit = set()
    def checkcalllimit(self):
      self.calllimit.add(True)
      if len(self.calllimit)>=self.maxperminute:
        print("sleep 65 seconds for call limit...")
        time.sleep(65)
        self.calllimit = set()
  limiter=Limiter(900)

  def audiototext(filepath,language="en-US"):
    limiter.checkcalllimit()
    with sr.AudioFile(filepath) as source:
      audio_data = r.record(source) # listen for the data (load audio to memory)
      # r.recognize_google(audio_data: AudioData, key: Union[str, None] = None, language: str = "en-US", , pfilter: Union[0, 1], show_all: bool = False)
      text = r.recognize_google(audio_data, language=language) # recognize (convert from speech to text)
      return text

  def getaudioduration(filepath): # return string!
    return subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'compact=print_section=0:nokey=1:escape=csv', '-show_entries', 'format=duration', f'{filepath}']).decode()

  def getmetadata(filepath):
    ffprobe = FFmpeg(executable="ffprobe").input(
        filepath,
        print_format="json", # ffprobe will output the results in JSON format
        show_streams=None,
    )
    return json.loads(ffprobe.execute())
    # {'streams': [{'index': 0, 'codec_name': 'pcm_s16le', 'codec_long_name': 'PCM signed 16-bit little-endian', 'codec_type': 'audio', 'codec_tag_string': '[1][0][0][0]', 'codec_tag': '0x0001', 'sample_fmt': 's16', 'sample_rate': '44100', 'channels': 1, 'bits_per_sample': 16, 'initial_padding': 0, 'r_frame_rate': '0/0', 'avg_frame_rate': '0/0', 'time_base': '1/44100', 'duration_ts': 256896, 'duration': '5.825306', 'bit_rate': '705600', 'disposition': {'default': 0, 'dub': 0, 'original': 0, 'comment': 0, 'lyrics': 0, 'karaoke': 0, 'forced': 0, 'hearing_impaired': 0, 'visual_impaired': 0, 'clean_effects': 0, 'attached_pic': 0, 'timed_thumbnails': 0, 'non_diegetic': 0, 'captions': 0, 'descriptions': 0, 'metadata': 0, 'dependent': 0, 'still_image': 0, 'multilayer': 0}}]}

  # convert mp3 to wav file
  def convertmp3towav(inputpath,outputpath): # path with extension .mp3 and .wav
    subprocess.call(['ffmpeg', '-i', f"{inputpath}", f"{outputpath}"])  # ffmpeg muss in in Umgebungsvariablen als Path gespeichert sein, ist sonst in D:\CDesktopLink\Portable\ffmpeg
         
  def create_Folder(foldername):
      pathlib.Path(foldername).mkdir(parents=True, exist_ok=True) # create folder       
                  
  ######################################################################################

  if __name__ == '__main__':
    
    # print(getaudioduration(r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Wwise Soundtool\ann1404wav_spy\eng\spy\40700001.wav"))
    # print(getmetadata(r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Wwise Soundtool\ann1404wav_spy\eng\spy\40700001.wav"))
    
    todo = input("(MP3)toWav? (Text)ToSpeech?\n")
    if todo=="MP3": # toWav

      # Convert mp3 to wav
      alreadywav = set()
      for pathobj in pathlib.Path(wavoutputfolder).iterdir():
        if pathobj.is_dir():
          for sub_p in pathobj.rglob("*"): # loop over all sub folders
            if sub_p.is_file():
              filename = sub_p.name
              name,ext = filename.split(".")
              if ext=="wav":
                alreadywav.add(name)
              
      for pathobj in pathlib.Path(anno1404sounds).iterdir():
        if pathobj.is_dir():
          for sub_p in pathobj.rglob("*"): # loop over all sub folders
            if sub_p.is_file():
              filename = sub_p.name
              name,ext = filename.split(".")
              if ext=="mp3" and name in AllSounds:
                if name not in alreadywav:
                  parentfoldername = sub_p.parents[0].name # eg narrator
                  languagefoldername = sub_p.parents[2].name # eg. "eng"
                  outputpath = f"{wavoutputfolder}/{languagefoldername}/{parentfoldername}"
                  create_Folder(outputpath)
                  finaloutputpath = f"{outputpath}/{name}.wav"
                  convertmp3towav(sub_p,finaloutputpath)
                  
    elif todo=="Text": # toSpeeach
      try:
        print(datetime.now())
        FileNameToText = {}
        breaken = False
        for pathobj in pathlib.Path(wavoutputfolder).iterdir():
          if pathobj.is_dir():
            for sub_p in pathobj.rglob("*"): # loop over all sub folders
              if sub_p.is_file():
                filename = sub_p.name
                name,ext = filename.split(".")
                if ext=="wav":
                  languagefoldername = sub_p.parents[1].name # eg. "eng"
                  language = Languages[languagefoldername]["official"]
                  if language not in FileNameToText:
                    FileNameToText[language] = {}
                  try:
                    text = audiototext(str(sub_p),language)
                  except sr.UnknownValueError as err: ## did not understand audio
                    print("google did not understand audio from",sub_p)
                    FileNameToText[language][name] = "UNKOWN"
                  except sr.RequestError as err: # internet/api problem
                    print("Connection/API Error...")
                    print(err,traceback.format_exc())
                    breaken = True
                    break
                  except Exception as err: # any other error
                    print(err,traceback.format_exc())
                    breaken = True
                    break
                  else:
                    duration = int(float(getaudioduration(str(sub_p))) * 1000)
                    FileNameToText[language][name] = {"D":duration,"T":text}
          if breaken:
            break
            
      except Exception as err:
        print(err,traceback.format_exc())
        
      print(datetime.now())
      with open(f"{wavoutputfolder}/FileNameToText.txt", "w", encoding="utf-8") as f:
        f.write(str(FileNameToText))
      
    
  

  ```
  </details>


###  upload_modio
- Uploading your mods to mod.io:

  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```python
  # Your modinfo.json needs to include:
    # "ModioResourceId" : 1234232
   # while you get this number for your mod after the first upload at the mod page.
  # Optionally you can include a changelog in your modinfo.json:
  # "changelog": {
      # "1.01" : "The game cuts the BasePrice value to integer, so I rounded my mathemtaical result now, this should fit a bit better than simply cutting it.",
      # "1.02" : "Load after New Horizons mod",
      # "1.03" : "Fix zip folder"
    # }
  # (keep in mind that json is very strict about missing/to much commas at the end and so on. To make a linebreak use "\n")

  # This script will check the local modinfo.json files and compare the version of them to the version uploaded at mod.io.
  # If your version can not be converted to a number, you have to adjust the "version_a_bigger_b" function below, so it can compare your functions to find out which is newer



  g_ModsPath = "D:/CDesktopLink/Unterlagen/Mods/Anno 1800/mods bei github" ## use slash "/" for folders . can also be relative path to the py script
  g_sub_folders = ["Anno-1800-Mods/Recommended-Mods","Anno-1800-Mods/YouKnowWhatYouDo-Mods"] # if no subfolder, then just use [""] and have the final path above
  # To get your Token: go to https://mod.io/me/access and create a new OAuth Access with custom client-name (if there is non already). 
  # Then enter a "Token Name" give it Read+Write and hit the "+" Symbol. Then you can copy your very very long Token String
  g_Modio_Token = ""
  g_GameID = 4169 # Anno1800
  g_make_double_folders = True # mod.io needs this. make_archive does not zip the folder, but only its content, while mod.io at best needs these double folders... only workaround I found is to create this double folder ourself and then zip this

  # found at the /access page and named "ID"
  g_Client_ID = 0
  g_base_url = f"https://u-{g_Client_ID}.modapi.io/v1"


  # old url that will be disabled soon
  # g_base_url = "https://api.mod.io/v1"


  # Change this function to sth else, if your version format can not be converted to a number, eg "1.2.1"
  def version_a_bigger_b(a,b):
    return float(a) > float(b)
    




  #######################################################################################

  # https://docs.mod.io/restapiref/?python#files
  # huge thanks to the author from:
  # https://github.com/ClementJ18/mod.io/tree/master/modio
  # without it I would never figured out that the official api documentation is just bullshit...
  # The base_url in the docu is wrong and no word how the hell we can pass a "file" as argument ...

  import requests # pip install requests
  import shutil
  import pathlib
  import json
  import time

  # https://docs.mod.io/restapiref/?javascript--nodejs#get-modfiles
  def api_getModFiles(ModioResourceId):
    headers = {
      'Authorization': f'Bearer {g_Modio_Token}',
      'Accept': 'application/json'
    }
    r = requests.get(f'{g_base_url}/games/{g_GameID}/mods/{ModioResourceId}/files', headers = headers)
    if r.status_code==429: # api limit reached...
      print("API Limit reached, waiting before continue ... ") 
      res_header = r.headers
      print(res_header)
      waitfor = int(res_header.get("retry-after",0)) # should include "retry-after"
      if not waitfor: # None/0 (its 0 for rolling ratelimits)
        waitfor = 60
      time.sleep(waitfor)
      return api_getModFiles(ModioResourceId)
    return r.json()
  # example return from docu:
  # {
    # "data": [
      # {
        # "id": 2,
        # "mod_id": 2,
        # "date_added": 1499841487,
        # "date_updated": 1499841487,
        # "date_scanned": 1499841487,
        # "virus_status": 0,
        # "virus_positive": 0,
        # "virustotal_hash": "",
        # "filesize": 15181,
        # "filesize_uncompressed": 16384,
        # "filehash": {
          # "md5": "2d4a0e2d7273db6b0a94b0740a88ad0d"
        # },
        # "filename": "rogue-knight-v1.zip",
        # "version": "1.3",
        # "changelog": "VERSION 1.3 -- Changes -- Fixed critical castle floor bug.",
        # "metadata_blob": "rogue,hd,high-res,4k,hd textures",
        # "download": {
          # "binary_url": "https://*.modapi.io/v1/games/1/mods/1/files/1/download/c489a0354111a4d76640d47f0cdcb294",
          # "date_expires": 1579316848
        # },
        # "platforms": [
          # {
            # "platform": "windows",
            # "status": 1
          # }
        # ]
      # },
      # {
          # ...
      # }
    # ],
    # "result_count": 70,
    # "result_offset": 0,
    # "result_limit": 100,
    # "result_total": 70
  # }



  # https://docs.mod.io/restapiref/?python#add-mod
  def api_uploadModFile(ModioResourceId,pathtozip,version,changelog="",active=True):
    headers = {
      'Authorization': f'Bearer {g_Modio_Token}',
      # 'Content-Type': 'multipart/form-data', # seems to be added by requests module already while using "files" as param
      'Accept': 'application/json'
    }
    with open(pathtozip, "rb") as file: # we have to open it to be able to actually pass a "file" object ...
      r = requests.post(f'{g_base_url}/games/{g_GameID}/mods/{ModioResourceId}/files', 
          params={ 
            "filedata": pathtozip, # "path/to/modfile.zip"
            "version": version,
            "changelog": changelog,
            "active": active,
            }, 
          headers = headers,
          files={"filedata": file},
          )
    try:
      return r.json()
    except Exception as err:
      print(f"ERROR! Response: {r} : json error: {err}")
      return None


  def api_deleteModFile(ModioResourceId,FileId):
    headers = {
      'Authorization': f'Bearer {g_Modio_Token}',
      'Content-Type':'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    }
    r = requests.delete(f'{g_base_url}/games/{g_GameID}/mods/{ModioResourceId}/files/{FileId}',headers=headers)
    if r.status_code==204:
      return True # success
    try:
      return r.json()
    except Exception as err:
      print(f"ERROR! Response: {r} : json error: {err}")
      return r
    



  if __name__ == '__main__':  
    def CheckAndUpdateMods():
      
      specific_ModID = input("Update specific ModID? Enter the ModID or nothing to check all mods for new version \n")
      if specific_ModID=="":
        specific_ModID = None
      
      # Checking local modfiles
      ModsInPath = {}
      for sub_folder in g_sub_folders:
        path = f"{g_ModsPath}/{sub_folder}"
        print("checking path ",path)
        pathobj1 = pathlib.Path(path) 
        for pathobj2 in pathobj1.iterdir():
          if pathobj2.is_dir():
            ModID = None
            FolderName = pathobj2.name
            for pathobj3 in pathobj2.iterdir(): # eg mods github/{sub_folder}/[Fix] Community Bugfixes
              if pathobj3.is_file():
                if pathobj3.name=="modinfo.json": 
                  with pathobj3.open('r', encoding='utf-8') as file:
                    try:
                      data = json.load(file)
                    except Exception as err:
                      print("ERROR while reading modinfo.json from modfolder: ",FolderName,err)
                      continue
                    ModID = data["ModID"]
                    if specific_ModID is None or specific_ModID==ModID:
                      ModsInPath[ModID] = data
                      ModsInPath[ModID]["FolderName"] = FolderName
                      ModsInPath[ModID]["FolderNameWithSubPath"] = f"{sub_folder}/{FolderName}"
                      ModsInPath[ModID]["latest_changelog"] = data.get("changelog",{}).get(ModsInPath[ModID]["Version"],"")
      # print(ModsInPath)
      # comparing them with uploaded mod.io files
      for ModID,modinfos in ModsInPath.items():
        ModioResourceId = modinfos.get("ModioResourceId")
        if ModioResourceId is None:
          print(f"Mod  {ModID}  hat keine ModioResourceId, kann nicht mit mod.io verglichen werden")
          continue
        modio_files = api_getModFiles(ModioResourceId=ModioResourceId)
        if modio_files.get("data") is None:
          print(modio_files)
        newest_modio_version = 0
        for file in modio_files["data"]:
          file_version = file["version"]
          newest_modio_version = version_a_bigger_b(file_version,newest_modio_version) and file_version or newest_modio_version
        local_version = float(modinfos["Version"])
        if version_a_bigger_b(local_version,newest_modio_version):
          print(f"mod.io version from  {ModID} ({ModioResourceId}) is older than local files: {newest_modio_version} < {local_version}")
          todo = input("Update this modio file? (Y)es or anything else for No\n")
          if todo.upper()=="Y":
            FolderName = modinfos['FolderName']
            FolderNameWithSubPath = modinfos['FolderNameWithSubPath']
            zipname = f"{FolderName}.zip" # creating the file next to this py script (and delete it after upload)
            
            if not g_make_double_folders: ## dont use this, because we need double folders for mod.io
              shutil.make_archive(base_name=FolderName,format='zip',root_dir=FolderNameWithSubPath) # first is the path were we want to create the zip and its name. root_dir is the path to the files we want to include in the zip
            else:
              if pathlib.Path(FolderName).is_dir() or pathlib.Path(FolderName).is_file():
                raise AssertionError("ERROR: please dont put the py script directly next to the mod folders you want to zip")
              shutil.copytree(pathlib.Path(FolderNameWithSubPath), pathlib.Path(f"{FolderName}/{FolderName}")) #  Returns the path to the newly created file. Bei Verknüpfungen wird die echte datei kopiert. ersetzt alte datei in destpath
              shutil.make_archive(base_name=FolderName,format='zip',root_dir=FolderName) # first is the path were we want to create the zip and its name. root_dir is the path to the files we want to include in the zip
            
            ret = api_uploadModFile(ModioResourceId=ModioResourceId,pathtozip=zipname,version=local_version,changelog=modinfos.get("latest_changelog",""),active=True)
            if ret is not None and ret.get("id"):
              print(f"########################### {ModID} upload success! ###########################\n{ret}")
            else:
              print(f"########################### {ModID} upload FAILED! {ret} ###########################")
                    
            pathlib.Path(zipname).unlink(missing_ok=True) # delete zip again. mit missing_ok=False gäbe es ein FileNotFoundError wenns die Datei nicht gibt
            if g_make_double_folders:
              shutil.rmtree(FolderName) # delete the helper folder again
            for file in modio_files["data"]:
              todo = input(f"Do you want to delete the previous mod.io file version  {file['version']}   ? (Y)es or anything else for No\n")
              if todo.upper()=="Y":
                success = api_deleteModFile(ModioResourceId,file['id'])
                if success==True:
                  print(f"########################### Delete File version {file['version']} from {ModID} success. ###########################")
                else:
                  print(f"########################### Delete File version {file['version']} from {ModID} FAILED {success}. ###########################")
    
    CheckAndUpdateMods()
    
    
    
    
    # print(api_getModFiles(3300179))
    # print(api_deleteModFile(3300179,6360416))
    
    
       
    

  ```
  </details>


###  create_hardlinks
- Creating hardlinks to folders (useful for shared mod management)

  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```python
  # hardlinks zu ordnern erstellen, damit ich dieselben Mods in untersch. Ordnern haben kann (sortiert)
   # es die Dateien aber nur einmal gibt, sodass ich sie leicht überall aufeinmal ändern kann

  import os
  import pathlib
  import stat
  import filecmp
  import shutil

  def is_hardlink_folder(dirpath):
    return (os.lstat(dirpath).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT) != 0
      
  def create_hardlink(linkpath,originalpath):
    os.system(f'mklink /J "{linkpath}" "{originalpath}"')
      
  # hab keine methode direkt mit python (os.link) gefunden um Ordner hardlinks zu erstellen, geht nur Dateien,
    # wenn man ordner versucht gibts "no permission" Fehler. Daher jetzt mit cmd command der über os.system() ausgeführt wird
    # os.system(f'mklink /J "{linkpath}" "{originalpath}"')

  # durch das "r" vorm string sind auch die \ erlaubt. (ansonsten müsste man sie durhc / oder \\ ersetzen, damit python damit klarkommt)

  selbernutzen_path = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Meine Mods\Selber Nutzen"
  nichnutzenaberreleased = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Meine Mods\nicht nutzen - interessant\_Released"
  github_recom_path = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\mods bei github\Anno-1800-Mods\Recommended-Mods"
  github_ykwyd_path = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\mods bei github\Anno-1800-Mods\YouKnowWhatYouDo-Mods"
  github_wip_path = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\mods bei github\Anno-1800-Mods\WorkInProgress-Mods"
  github_shared_path = r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\mods bei github\Anno-1800-SharedMods (for Modders)"

  modsfolder = r"C:\Users\Serpens66\Documents\Anno 1800\mods"



  def is_equal(dcmp,withsub=True):
    equal = True
    if dcmp.right_only or dcmp.left_only or dcmp.diff_files: # this only compares the files on the first level
      equal =  False
    if withsub and equal!=False:
      for sub_dcmp in dcmp.subdirs.values():
        equal = is_equal(sub_dcmp)
        if equal==False:
          break
    return equal
    
  def print_diff_files(dcmp,path):
    if not is_equal(dcmp,False):
      print("Ordner:",path)
      if dcmp.left_only:
        print("left_only",dcmp.left_only)
      if dcmp.right_only:
        print("right_only",dcmp.right_only)
      if dcmp.diff_files:
        print("diff_files",dcmp.diff_files)
    for k,sub_dcmp in dcmp.subdirs.items():
      print_diff_files(sub_dcmp,k)

  def compare_if_equal_do_hardlink(linkpath,originalpath):
    if linkpath!=originalpath: ## for whatever reason it shows as unequal and hardlink works, super strange. so prevent it.
      dcmp = filecmp.dircmp(linkpath, originalpath) # vergleichen des Inhalt der zwei genannten Ordner
      todo = "Y"
      if not is_equal(dcmp):
        print("############################")
        print("Vergleich:\n",linkpath,originalpath)
        print_diff_files(dcmp,originalpath.name)
        print("############################")
        todo = input(f"Do you still want to hardlink (assuming the main mod is newer)? (Y)es or anything else for No\n")
      if todo.upper()=="Y": # then hardlink (funktioniert soweit, aber zuerst evlt die shared mods hardlinken)
        print(f"Replacing with hardlink: {originalpath.name}\n{linkpath} VS {originalpath}")
        shutil.rmtree(linkpath) # delete folder
        create_hardlink(linkpath,originalpath)

  if __name__ == '__main__':
    # loopen über die selbernutzen mods um die mods zu bekommen die wir selbst nutzen wollen, ordnernamen merken, nur oberste ebene.
    # dann loopen über alle github mods (obersete ebene) und wenn wir einen selbernutzen mod finden,
     # dann diesen linken. aber vorher selbernutzen mod ordner löschen (oder umbennenne mit "_" davor)
    
    
    # alle selbst mods durch links zu github ordner ersetzen, sofern vorhanden (WIP erstmal nicht, weil manche dadurch doppelt vorkommen)
    # selbstnutzenmods = {}
    # for pathobj in pathlib.Path(selbernutzen_path).iterdir():
      # if not is_hardlink_folder(pathobj):
        # selbstnutzenmods[pathobj.name] = pathobj
    # for githubpath in [github_recom_path,github_ykwyd_path]:
      # for pathobj in pathlib.Path(githubpath).iterdir():
        # if pathobj.is_dir() and not is_hardlink_folder(pathobj):
          # selbernutzenmodpath = selbstnutzenmods.get(pathobj.name)
          # if selbernutzenmodpath:
            # compare_if_equal_do_hardlink(selbernutzenmodpath,pathobj)
            
    # nichnutzenaberreleased
    # selbstnutzenmods = {}
    # for pathobj in pathlib.Path(nichnutzenaberreleased).iterdir():
      # if not is_hardlink_folder(pathobj):
        # selbstnutzenmods[pathobj.name] = pathobj
    # for githubpath in [github_recom_path,github_ykwyd_path]:
      # for pathobj in pathlib.Path(githubpath).iterdir():
        # if pathobj.is_dir() and not is_hardlink_folder(pathobj):
          # selbernutzenmodpath = selbstnutzenmods.get(pathobj.name)
          # if selbernutzenmodpath:
            # compare_if_equal_do_hardlink(selbernutzenmodpath,pathobj)
          
          
    # alle shared mods die verschachtelt in shared mods sind durch hardlinks ersetzen
    # shared_mods = {}
    # for shared_pathobj in pathlib.Path(github_shared_path).iterdir():
      # shared_mods[shared_pathobj.name] = shared_pathobj
    # for shared_pathobj in pathlib.Path(github_shared_path).iterdir():
      # for sub_p in shared_pathobj.rglob("*"): # loop over all sub folders
        # if sub_p.is_dir() and shared_mods.get(sub_p.name) and not is_hardlink_folder(sub_p):
          # main_shared_pathobj = shared_mods[sub_p.name]
          # compare_if_equal_do_hardlink(sub_p,main_shared_pathobj)
        
        
    # bei allen github mods die enthaltenen shared mods durch links zu den shared github mods ersetzen
    # githubsubmods = {}
    # for githubpath in [github_recom_path,github_ykwyd_path,github_wip_path]:
      # for pathobj in pathlib.Path(githubpath).iterdir():
        # if pathobj.is_dir() and not is_hardlink_folder(pathobj):
          # for pathobj2 in pathlib.Path(pathobj).iterdir():
            # if pathobj2.is_dir() and not is_hardlink_folder(pathobj2):
              # if not githubsubmods.get(pathobj2.name):
                # githubsubmods[pathobj2.name] = []
              # githubsubmods[pathobj2.name].append(pathobj2)
              # for pathobj3 in pathlib.Path(pathobj2).iterdir():
                # if pathobj3.is_dir() and not is_hardlink_folder(pathobj3):
                  # if not githubsubmods.get(pathobj3.name):
                    # githubsubmods[pathobj3.name] = []
                  # githubsubmods[pathobj3.name].append(pathobj3)
    # for pathobj in pathlib.Path(github_shared_path).iterdir():
      # if pathobj.is_dir() and not is_hardlink_folder(pathobj):
        # githubmodpaths = githubsubmods.get(pathobj.name)
        # if githubmodpaths:
          # for githubmodpath in githubmodpaths:
            # compare_if_equal_do_hardlink(githubmodpath,pathobj)
      

      
    # replacing the mods in mods folder with hardlinks to github
    # ACHTUNG: modloader kann offenbar nicht mit hardlinks die hardlinks enthalten umgehen...
     # also hier keine hardlinks nutzen
    # mods = {}
    # for pathobj in pathlib.Path(modsfolder).iterdir():
      # if not is_hardlink_folder(pathobj):
        # mods[pathobj.name] = pathobj
    # for githubpath in [github_recom_path,github_ykwyd_path,github_wip_path,github_shared_path]:
      # for pathobj in pathlib.Path(githubpath).iterdir():
        # if pathobj.is_dir() and not is_hardlink_folder(pathobj):
          # selbernutzenmodpath = mods.get(pathobj.name)
          # if selbernutzenmodpath:
            # compare_if_equal_do_hardlink(selbernutzenmodpath,pathobj)
      
      
      
    # bugfix mods:
    # mods = {}
    # for pathobj in pathlib.Path(r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\mods bei github\BugFixes\[Fix] Community Bugfixes\shared_mods").iterdir():
      # if not is_hardlink_folder(pathobj):
        # mods[pathobj.name] = pathobj
    # for githubpath in [github_recom_path,github_ykwyd_path,github_wip_path,github_shared_path]:
      # for pathobj in pathlib.Path(githubpath).iterdir():
        # if pathobj.is_dir() and not is_hardlink_folder(pathobj):
          # selbernutzenmodpath = mods.get(pathobj.name)
          # if selbernutzenmodpath:
            # compare_if_equal_do_hardlink(selbernutzenmodpath,pathobj)
       
     
    

  ```
  </details>


