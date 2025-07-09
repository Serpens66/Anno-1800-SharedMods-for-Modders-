# Python ModOp code snippets for various purposes

The code is made for my own purposes, so you may need to adjust it for your purpose.  
If you don't know python that may be too difficult for you.  

- [Add Anno 1404 Voice Sounds to Anno 1800](#https://github.com/Serpens66/Anno1404SoundsTo1800/tree/main)
- [soundsforanno](#soundsforanno)
- [upload_modio](#upload_modio)
- [create_hardlinks](#create_hardlinks)


###  soundsforanno
- Converting mp3 to wav and read out soundbank details from json and conert speech to text (needs https://ffmpeg.org/download.html)

  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```python
    # Its best if you already understand python and can adjust the script to your needs!
  # Otherwise use this project instead: https://github.com/Serpens66/Anno1404SoundsTo1800/tree/main


  # A script to prepare your mp3/wav files to be used in wwise to put into a soundbank.
  # And to create your assets.xml/text_xml file after the soundbank was created to be used in Anno1800.
  # As audio to Text it supports using Anno 1404 texts and speech to text from google



  # Das Skript supported nur sehr simple soundbanks, welche bei denen die json pro language nur eine soundbank drin hat
   # und jedes event nur eine IncludedMemoryFiles hat


  g_Mood = "Neutral"
  g_SpeechAudioType = "Murmur"
  # SpeechAudioType is in vanilla Campaign for Narrator and Murmur for texts your ships are saying. And PaMSy for things the other characters are saying.
  # Mood should bei "Neutral" in most cases, unless it is a audio that is ment to be aggressive (Negative) or very positive (Positve), so mostly relevant for PaMSy of other characters.

  # audioinfo = {"FileID":FileID,"DurationMin":DurationMin,"DurationMax":DurationMax,"AnnoLanguage":AnnoLanguage,"Languagebnk":Languagebnk,"SoundBankName":SoundBankName,"SoundBankID":SoundBankID,"Eventname":eventname,"wavfilename":wavfilename}
  def customGetTextFn(eventID,AnnoLanguage,audioinfo):
    Text = "UNKNOWN"
    # your code
    return Text
    
  ######################################################################################

  # Wwise auch soviel wie möglich automatisieren, evlt mit: https://github.com/matheusvilano/PyWwise ?  https://www.audiokinetic.com/en/blog/pywwise-waapi-made-pythonic/
  # man muss wwise dennoch installieren und öffnen und "Project > User Preferences... > Enable Wwise Authoring API" aktivieren
  # wobei selbst der kleine "Hello World" Test code nicht funktioniert, vermutlich ist wwise version 2019.2.15.7667
  # zu alt dafür (und neuere Version darf für games die alte version nutzen tatsächlich nicht genutzt werden...)
  # WWise 2019 has to be used for Anno1800 which is too old for wwise: https://github.com/matheusvilano/PyWwise/discussions/71
      
  ######################################################################################

  import subprocess
  import pathlib
  # pip install SpeechRecognition , braucht wohl internet und nutzt google https://thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
  import speech_recognition as sr
  from datetime import datetime
  import traceback
  import time
  import json
  import shutil
  # optional: pip install python-ffmpeg, but it saves the hassle to deal with this stupid command line formatting (still needs the ffmpeg exe file in path)
  # https://python-ffmpeg.readthedocs.io/en/stable/examples/querying-metadata/
  # https://python-ffmpeg.readthedocs.io/en/stable/api/
  # from ffmpeg import FFmpeg
  # optional, just for my GetTextFromGUIDsAnno1404 fn using get_encoding_type
  from chardet import detect as chardet_detect # get file encoding type # pip install chardet

  ######################################################################################


  # Anno1800 can only use these four audio languages (tried different, but it uses english)
  # Anno uses english automatically (references languages set in wwise) for all unsupported languages
  Languages_AnnoToOfficial = {"German":"de-DE","English":"en-US","French":"fr-FR","Russian":"ru-RU"}
  Languages_bnkToAnno = {"de_de":"German","en_us":"English","fr_fr":"French","ru_ru":"Russian"}


  xml_base = """<ModOps>  
    <!-- uses GUIDs {StartingGUID} to including {EndGUID} -->

    <!-- Positioning: -->
    <!-- for things like shots and stuff that is played without your user interaction at a location ingame, you might want to define MaxAttenuation in Audio property -->
    

    {SoundBankCode}
    {AssetCode}
    
  </ModOps>"""

  xml_Asset_base = """<ModOp Type="addNextSibling" GUID="224035">
      {AudioAssets}
    </ModOp>"""

  xml_AudioAsset = """    <Asset>
        <Template>Audio</Template>
        <Values>
          <Standard>
            <GUID>{AudioGUID}</GUID>
            <Name>{Eventname}</Name>
          </Standard>
          <Audio>
            <DurationLanguageArray>
              <German>
                <DurationMinimum>{German_DurationMin}</DurationMinimum>
                <DurationMaximum>{German_DurationMax}</DurationMaximum>
              </German>
              <English>
                <DurationMinimum>{English_DurationMin}</DurationMinimum>
                <DurationMaximum>{English_DurationMax}</DurationMaximum>
              </English>
              <French>
                <DurationMinimum>{French_DurationMin}</DurationMinimum>
                <DurationMaximum>{French_DurationMax}</DurationMaximum>
              </French>
              <Russian>
                <DurationMinimum>{Russian_DurationMin}</DurationMinimum>
                <DurationMaximum>{Russian_DurationMax}</DurationMaximum>
              </Russian>
            </DurationLanguageArray>
          </Audio>
          <WwiseStandard>
            <WwiseID>{SoundBankID}</WwiseID>
          </WwiseStandard>
        </Values>
      </Asset>"""

  xml_AudioTextAsset = """    <Asset>
        <Template>AudioText</Template>
        <Values>
          <Standard>
            <GUID>{AudioTextGUID}</GUID>
            <Name>AudioText {Eventname}: {Text}</Name>
          </Standard>
          <Text />
          <AudioText>
            <AudioAsset>{AudioGUID}</AudioAsset>
            <SpeechAudioType>{SpeechAudioType}</SpeechAudioType>
            <Mood>{Mood}</Mood>
          </AudioText>
        </Values>
      </Asset>"""




  xml_SoundBank_base = """<ModOp Type="addNextSibling" GUID="234859">
      {SoundBankAsset}
    </ModOp>
    <!-- the global sound 9899002 loads before mods, so we have to add our sounds instead to the regions -->
    <ModOp Type="add" GUID="5000001,5000000,160001,114327" Path="/Values/RequiredSoundBanks/SoundBanks">
      {SoundBankEntry}
    </ModOp>
    <!-- if asia region exists (your mod needs to load after that mod) -->
    <ModOp Type="add" GUID="133700001" Path="/Values/RequiredSoundBanks/SoundBanks"
      Condition="@133700001">
      {SoundBankEntry}
    </ModOp>"""
    
  xml_SoundBankAsset = """    <Asset>
        <Template>SoundBank</Template>
        <Values>
          <Standard>
            <GUID>{SoundBankGUID}</GUID>
            <Name>BNK_VO_{SoundBankName}</Name>
            <IconFilename>test_data/graphics/wwise_icons/soundbank.png</IconFilename>
          </Standard>
          <SoundBank>
            <SoundBankLocalized>1</SoundBankLocalized>
          </SoundBank>
          <WwiseStandard>
            <WwiseID>{SoundBankID}</WwiseID>
          </WwiseStandard>
        </Values>
      </Asset>"""
      
  xml_SoundBankEntry = """    <Item>
        <Bank>{SoundBankGUID}</Bank>
      </Item>"""
      
  xml_text_base = """<ModOps>

    <ModOp Type="add" Path="/TextExport/Texts">
      {TextEntries}
    </ModOp>

  </ModOps>"""

  xml_textentry = """    <Text>
        <GUID>{AudioTextGUID}</GUID>
        <Text>{Text}</Text>
      </Text>"""
      


      
      


  ######################################################################################

  r = sr.Recognizer()


  # https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#recognizer_instancerecognize_googleaudio_data-audiodata-key-unionstr-none--none-language-str--en-us--pfilter-union0-1-show_all-bool--false---unionstr-dictstr-any
  # Irgendwo soll wohl das API Limit stehen mit: https://stackoverflow.com/questions/71121167/googles-speech-recognition-api-recognize-google-function-in-python-usage-limi
      # The current API usage limits for Speech-to-Text are as follows:
      # 900 requests per 60 seconds
      # Processing per day: 480 hours of audio

  # extreme simple api call limit system, just wait a minute after each 900 calls
  class Limiter:
    def __init__(self,maxperminute):
      self.maxperminute = maxperminute
      self.callcount = 0
    def checkcalllimit(self):
      self.callcount += 1
      if self.callcount>=self.maxperminute:
        print("sleep 65 seconds for call limit...")
        time.sleep(65)
        self.callcount = 0
  limiter=Limiter(900)

  def audiototext(filepath,language="en-US"):
    limiter.checkcalllimit()
    with sr.AudioFile(filepath) as source:
      audio_data = r.record(source) # listen for the data (load audio to memory)
      # r.recognize_google(audio_data: AudioData, key: Union[str, None] = None, language: str = "en-US", , pfilter: Union[0, 1], show_all: bool = False)
      text = r.recognize_google(audio_data, language=language) # recognize (convert from speech to text)
      return text

  def getaudioduration(filepath): # return string!
    return subprocess.check_output(['tools/ffmpeg/ffprobe', '-v', 'quiet', '-print_format', 'compact=print_section=0:nokey=1:escape=csv', '-show_entries', 'format=duration', f'{filepath}']).decode()

  # def getmetadata(filepath):
    # ffprobe = FFmpeg(executable="tools/ffmpeg/ffprobe").input(
        # filepath,
        # print_format="json", # ffprobe will output the results in JSON format
        # show_streams=None,
    # )
    # return json.loads(ffprobe.execute())
    # {'streams': [{'index': 0, 'codec_name': 'pcm_s16le', 'codec_long_name': 'PCM signed 16-bit little-endian', 'codec_type': 'audio', 'codec_tag_string': '[1][0][0][0]', 'codec_tag': '0x0001', 'sample_fmt': 's16', 'sample_rate': '44100', 'channels': 1, 'bits_per_sample': 16, 'initial_padding': 0, 'r_frame_rate': '0/0', 'avg_frame_rate': '0/0', 'time_base': '1/44100', 'duration_ts': 256896, 'duration': '5.825306', 'bit_rate': '705600', 'disposition': {'default': 0, 'dub': 0, 'original': 0, 'comment': 0, 'lyrics': 0, 'karaoke': 0, 'forced': 0, 'hearing_impaired': 0, 'visual_impaired': 0, 'clean_effects': 0, 'attached_pic': 0, 'timed_thumbnails': 0, 'non_diegetic': 0, 'captions': 0, 'descriptions': 0, 'metadata': 0, 'dependent': 0, 'still_image': 0, 'multilayer': 0}}]}

  # convert mp3 to wav file
  def convertmp3towav(inputpath,outputpath): # path with extension .mp3 and .wav
    subprocess.call(['tools/ffmpeg/ffmpeg', '-i', f"{inputpath}", f"{outputpath}"])  # ffmpeg muss in in Umgebungsvariablen als Path gespeichert sein, ist sonst in D:\CDesktopLink\Portable\ffmpeg

  # creates a subfolder named the same like the filename of the soundbank and puts the wem files in it
  def extract_wem_from_bnk(filepathtobnk):
    return subprocess.check_output(['tools/bnkextr', f'{filepathtobnk}'])

  # the wav file is placed next to the wem file and is named .wem.wav
  def convert_wem_to_wav(filepathtowem):
    return subprocess.check_output(['tools/vgmstream-win64/vgmstream-cli.exe', f'{filepathtowem}'])

  def get_encoding_type(filename):
      try:
          with open(filename, 'rb') as f:
              rawdata = f.read()
          return chardet_detect(rawdata)['encoding']
      except FileNotFoundError as err:
          return None

  def into_path(filename):
      return pathlib.Path(filename) # string umwandeln in path objekt

  def file_exists(filename): # returns True wenn diese Datei/dieser Pfad existiert
      return pathlib.Path(filename).is_file()
      
  def folder_exists(foldername): # returns True wenn dieser Ordner existiert
      return pathlib.Path(filename).is_dir()
  def create_Folder(foldername):
      pathlib.Path(foldername).mkdir(parents=True, exist_ok=True) # create folder       
                
  def GetParentFolderNames(pathobj):
      parentnames = []
      for par in pathobj.parents:
        parentnames.append(par.name)
      return parentnames
                
  def delete_pathfilefolder(pathname): # löscht die Datei oder Ordner an diesem Pfad. Ordner muss leer sein
      path = pathlib.Path(pathname)
      if path.is_file():
          path.unlink(missing_ok=True) # mit missing_ok=False gäbe es ein FileNotFoundError wenns die Datei nicht gibt
      elif path.is_dir():
          try:
            path.rmdir()
          except:
            shutil.rmtree(str(path)) # also deletes filled folders
               
  def rename_file(filename,newfilename,replace=True):# ACHTUNG replace=False, also "rename" funktioniert nur auf Windows. Auf Linux wird immer replaced
      # filename mit Dateiendung übergeben!
      if file_exists(filename):
          if replace:
              pathlib.Path(filename).replace(newfilename) # durch replace: wenn es newfilename bereits gibt, wird sie dadurch überschrieben
          else:
              pathlib.Path(filename).rename(newfilename) # gibt FileExistsError auf Windows wenn es newfilename bereits gibt. Auf Linux wirds aber dennoch replaced!
      else:
          print(f"rename_file: {filename} existiert nicht, kann daher auch nicht umbenannt werden")

  def rename_wemwav_to_wav(filepathtowemwav):
    rename_file(filepathtowemwav,str(filepathtowemwav).replace(".wem.wav",".wav"))

  def GetTextBySpeech(filepathobj,Language):
    Text = "UNKNOWN"
    print(f"getting text from {str(filepathobj)} ...")
    try:
      Text = audiototext(str(filepathobj),Language).capitalize() # for whatever reason google writes most in lower letters. lets at least write the first word capital
      print("->",filepathobj.name,Text)
    except sr.UnknownValueError as err: ## did not understand audio
      print("google did not understand audio from",filepathobj)
    except sr.RequestError as err: # internet/api problem
      print("Connection/API Error...")
      print(err,traceback.format_exc())
    except Exception as err: # any other error
      print(err,traceback.format_exc())
    return Text
               

  # \data\loca\eng\txt
  def GetTextFromGUIDsAnno1404(Anno1404_path,GUIDs):
    Anno1404_pathobj = into_path(Anno1404_path)
    Texts = {}
    for AnnoLanguage,guids in GUIDs.items():
      if AnnoLanguage not in Texts:
        Texts[AnnoLanguage] = {}
      lang_foldername = AnnoLanguage=="German" and "ger" or AnnoLanguage=="English" and "eng" or AnnoLanguage=="French" and "fra" or AnnoLanguage=="Russian" and "rus" or None
      if lang_foldername:
        Anno1404_txtpath = f"{Anno1404_pathobj}/data/loca/{lang_foldername}/txt"
        Anno1404_txtpathobj = into_path(Anno1404_txtpath)
        if Anno1404_txtpathobj.is_dir():
          for sub_p in Anno1404_txtpathobj.rglob("*"):
            if sub_p.is_file():
              filename = sub_p.name
              name,ext = filename.split(".")
              if ext=="txt":
                with open(f'{sub_p}', 'r', encoding=get_encoding_type(sub_p)) as f: # most anno1404 txt files have special encoding, without mentioning it here, we can not search the files
                  filetext = f.read()
                  zeilen = list(filetext.split("\n"))
                  for GUID in guids:
                    GUID = str(GUID)
                    if GUID not in Texts[AnnoLanguage] and GUID in filetext:
                      for zeile in zeilen:
                        if GUID in zeile:
                          zeilensplit = zeile.split("=") # 40000009=Agent of the Doge
                          if len(zeilensplit)==2 and GUID==zeilensplit[0]:
                            Texts[AnnoLanguage][GUID] = zeilensplit[1]
                            break
    return Texts
               
  ######################################################################################

  def main():
    

    if True:  
      
      todo = input("Are you done creating a soundbank with wwise based on your wav files (and put the bnk+json file into your mod with correct folder structure (data/sound/generatedsoundbanks/windows))? (Y)es/(N)o\n")
      if todo.upper()=="N":
        todo = input("\nDo you want to filter your audio files to only use specific ones?\nJust hit enter if not. Enter the full path to your audiofiles (will go through all subfolders and find mp3 and wav files and deletes all audio files not mentioned by you in the next step. So make a security copy of the folder)\n")
        if todo!="":
          pathobj = into_path(todo)
          if pathobj.is_dir():
            todo = input("\nEnter a list of filenames (without extension) you want to keep, like this: abc2,testname,thisfile,thatfile\n")
            Fehler = False
            try:
              liste = list(todo.split(","))
              if isinstance(liste,list):
                todo = input(f"\nIst diese Liste korrekt (Y)es/(N)o: {liste} \n")
                if todo.upper()=="Y":
                  for sub_p in pathobj.rglob("*"): # loop over all sub folders
                    if sub_p.is_file():
                      filename = sub_p.name
                      name,ext = filename.split(".")
                      if ext=="wav" or ext=="mp3":
                        if name not in liste:
                          todo = input(f"\nDelete the file (Y)es/(N)o {filename}\n")
                          if todo.upper()=="Y":
                            delete_pathfilefolder(sub_p)
                else:
                  print("Abort everything")
                  return
              else:
                Fehler = liste
            except Exception as err:
              Fehler = err
            if Fehler:
              print(f"Fehler beim versuch die Eingabe als Liste zu interpretieren. abort. {Fehler}")
              return
          else:
            print("That was not a valid folder, aborting...")
            return
      
        todo = input("\nFor Wwise you need .wav audio files. If you have mp3 file format, do you want to to convert them now?\nJust hit enter if not. Enter the full path to your audiofiles to convert (will go through all subfolders and find mp3 files and puts a wav file next to them)\n")
        if todo!="":
          pathobj = into_path(todo)
          if pathobj.is_dir():
            for sub_p in pathobj.rglob("*"): # loop over all sub folders
              if sub_p.is_file():
                filename = sub_p.name
                name,ext = filename.split(".")
                if ext=="wav":
                  wavpath = f"{sub_p.parents[0]}/{name}.wav"
                  wavpathobj = into_path(wavpath)
                  if not wavpathobj.is_file(): # wav file does not exist in same folder, then convert it
                    convertmp3towav(sub_p,wavpathobj)
            print("Done converting to wav files\n")
          else:
            print("That was not a valid folder, aborting...")
            return
            
        
        todo = input("Do you want to add the parent folder name to the name of your wav files?\nLike if the wav is in a folder called -spy- add -spy_- in front of the name?\nIn your soundbank they all might get in the same folder, so that may make it easier to remember what the sound is.\nJust hit enter if not. Enter the full path to your audiofiles if yes.")
        if todo!="":
          pathobj = into_path(todo)
          if pathobj.is_dir(): # add parentfolder name into wav filename
            for sub_p in pathlib.Path(pathobj).rglob("*"):
              if sub_p.is_file():
                filename = sub_p.name
                name,ext = filename.split(".")
                if ext=="wav":
                  parentfoldername = sub_p.parents[0].name # eg narrator
                  newfilepath = f"{sub_p.parents[0]}_{filename}"
                  rename_file(sub_p,newfilepath,replace=False)
            print("Done renaming wav files\n")
          else:
            print("That was not a valid folder, aborting...")
            return
            
      elif todo.upper()=="Y":
        
        todo = input("\nThis script can create the assets.xml/text_.xml files based on the information in the created json/bnk file.\nJust hit enter if you dont want this. Enter the path to your mod (to the folder with modinfo.json)\nto not overwrite your existing files, the created files be put into a seperate folder named -generated-\n")
        if todo!="":
          pathobj = into_path(todo)
          if pathobj.is_dir():
            destination = f"{pathobj}/generated"
            create_Folder(destination)
            audioinfos = {}
            soundbankfolderpathobj = into_path(f"{pathobj}/data/sound/generatedsoundbanks/windows")
            if soundbankfolderpathobj.is_dir():
              SoundBanks = {} # we have at least one bank per language, but maybe even more
              for sub_p in soundbankfolderpathobj.rglob("*"): # loop over all sub folders
                if sub_p.is_file():
                  filename = sub_p.name
                  name,ext = filename.split(".")
                  if ext=="json":
                    with sub_p.open('r', encoding='utf-8') as file:
                      data = json.load(file)
                      Languagebnk = data["SoundBanksInfo"]["SoundBanks"][0]["Language"] # eg. "de_de"
                      SoundBankName = data["SoundBanksInfo"]["SoundBanks"][0]["ShortName"]
                      SoundBankID = data["SoundBanksInfo"]["SoundBanks"][0]["Id"]
                      AnnoLanguage = Languages_bnkToAnno[Languagebnk]
                      if SoundBankID not in SoundBanks:
                        SoundBanks[SoundBankID] = {}
                      if AnnoLanguage not in SoundBanks[SoundBankID]:
                        SoundBanks[SoundBankID][AnnoLanguage] = {"jsonPath":str(sub_p),"SoundBankName":SoundBankName}
                      for event in data["SoundBanksInfo"]["SoundBanks"][0]["IncludedEvents"]:
                        eventID = event["Id"]
                        DurationMin = round(float(event["DurationMin"])*1000)
                        DurationMax = round(float(event["DurationMax"])*1000)
                        eventname = event["Name"] # "Play_spy_40700606"
                        FileID = event["IncludedMemoryFiles"][0]["Id"]
                        wavfilename = event["IncludedMemoryFiles"][0]["ShortName"] # "spy_40700606.wav"
                        if not eventID in audioinfos:
                          audioinfos[eventID] = {}
                        audioinfos[eventID][AnnoLanguage] = {"FileID":FileID,"DurationMin":DurationMin,"DurationMax":DurationMax,"AnnoLanguage":AnnoLanguage,"Languagebnk":Languagebnk,"SoundBankName":SoundBankName,"SoundBankID":SoundBankID,"Eventname":eventname,"wavfilename":wavfilename}
              
              
            todo = input("\nNow create the xml files? Enter nothing if no. Enter (Audio) for just Audio assets and (AudioText) for Audio+AudioText+text_.xml\n")
            if todo.upper()=="AUDIOTEXT" or todo.upper()=="AUDIO":
              Texts = None
              if todo.upper()=="AUDIOTEXT": # unpack the bnk file to wem and convert to wav again. (I know if we already have wav, this is stupid work, but this way we can control the folder structure and easily find the correct files, so coding wise its easier)
                method = input("To get the text, use (G)oogle which uses internet or from unpacked (A)nno1404 files or your (C)ustom Function?\n")
                if method.upper()=="G": # TODO we may use threads to make the google calls all at the same time
                  Texts = {}
                  for SoundBankID,sbinfos in SoundBanks.items():
                    for AnnoLanguage,sbinfo in sbinfos.items():
                      SoundBankPathObj = into_path(sbinfo["jsonPath"].replace(".json",".bnk"))
                      if SoundBankPathObj.is_file():
                        filename = SoundBankPathObj.name
                        name,ext = filename.split(".")
                        if ext=="bnk":
                          extract_wem_from_bnk(SoundBankPathObj) ## will create wem files in a subfolder named like the soundbank
                          wemfolderpathobj = into_path(f"{SoundBankPathObj.parents[0]}/{name}")
                          if wemfolderpathobj.is_dir():
                            for wempathobj in wemfolderpathobj.iterdir():
                              if wempathobj.is_file():
                                wemfilename = wempathobj.name
                                wemname,wemext = wemfilename.split(".")
                                if wemext=="wem":
                                  convert_wem_to_wav(wempathobj) # convert wem to wav, will be created next to wem file
                                  rename_wemwav_to_wav(f"{wempathobj}.wav") # they are called .wem.wav, but we want it to only be .wav
                                  wavfilename = f"{wemname}.wav"
                                  wavfilepathobj = into_path(f"{wempathobj.parents[0]}/{wavfilename}")
                                  FileID = wemname # the created wem files are named after the FileID
                                  Language_Official = Languages_AnnoToOfficial[AnnoLanguage]
                                  Text = GetTextBySpeech(wavfilepathobj,Language_Official)
                                  Texts[FileID] = Text
                            if wemfolderpathobj.is_dir():
                              delete_pathfilefolder(wemfolderpathobj) # delete the wem folder again
                elif method.upper()=="A":
                  print("!!!!!!!!!!!!!!!!!!!!!!\nThis code assumes that the wav files you used for the soundbank include the original Anno1404 GUIDs in either -GUID.wav- or -customname_GUID.wav- so with one underscore!\n")
                  path = input("Enter the path to your unpacked Anno1404 files (in that folder you will have the data folder)\n")
                  GUIDs = {}
                  for eventID,infos in audioinfos.items():
                    for AnnoLanguage,info in infos.items():
                      if AnnoLanguage not in GUIDs:
                        GUIDs[AnnoLanguage] = []
                      wavfilename = info["wavfilename"]
                      filename,fileext = wavfilename.split(".")
                      filenamesplit = filename.split("_")
                      GUID = None
                      if len(filenamesplit)==1:
                        GUID = filenamesplit[0]
                      elif len(filenamesplit)==2:
                        GUID = filenamesplit[1]
                      if GUID:
                        GUIDs[AnnoLanguage].append(GUID)
                        info["1404GUID"] = GUID
                      else:
                        print(f"was not able to get GUID out of filename, skipping it: {wavfilename}")
                  Texts = GetTextFromGUIDsAnno1404(path,GUIDs)
                        
              StartingGUID = input("\nEnter the Starting GUID for your assets\n") # 1500001900
              if StartingGUID!="":
                StartingGUID = int(StartingGUID)
                
                # audioinfos[eventID][AnnoLanguage] = {"Id":Id,"DurationMin":DurationMin,"DurationMax":DurationMax,"AnnoLanguage":AnnoLanguage,"Languagebnk":Languagebnk,"SoundBankName":SoundBankName,"SoundBankID":SoundBankID,"Eventname":eventname}
                CurrentGUID = StartingGUID
                final_asset_code = ""
                final_text_code = {"Russian":"","German":"","English":"","French":""}
                soundbankentries = ""
                soundbankassets = ""
                soundbanksdone = set() # we have one per language, but the ID is the same and we only need one xml entry
                for SoundBankID,sbinfos in SoundBanks.items():
                  for AnnoLanguage,sbinfo in sbinfos.items():
                    if SoundBankID not in soundbanksdone:
                      SoundBankGUID = CurrentGUID
                      SoundBankName = sbinfo["SoundBankName"]
                      sbentry = xml_SoundBankEntry.format(SoundBankGUID=SoundBankGUID)
                      soundbankentries = f"{soundbankentries}\n{sbentry}"
                      sbasset = xml_SoundBankAsset.format(SoundBankID=SoundBankID,SoundBankName=SoundBankName,SoundBankGUID=SoundBankGUID)
                      soundbankassets = f"{soundbankassets}\n{sbasset}"
                      CurrentGUID += 1
                      soundbanksdone.add(SoundBankID)
                final_soundbank_code = xml_SoundBank_base.format(SoundBankAsset=soundbankassets , SoundBankEntry=soundbankentries)
                for eventID,infos in audioinfos.items():
                  AudioGUID = CurrentGUID
                  CurrentGUID += 1
                  if todo.upper()=="AUDIOTEXT":
                    AudioTextGUID = CurrentGUID
                    CurrentGUID += 1
                  Durations = {}
                  audio_code = xml_AudioAsset
                  filesdone = set() # each file only needs on entry in assets.xml regardless of how many languages
                  for AnnoLanguage,info in infos.items():
                    Durations[f"{AnnoLanguage}_DurationMax"] = info["DurationMax"]
                    try:
                      Durations[f"{AnnoLanguage}_DurationMin"] = info["DurationMin"]
                    except Exception as err:
                      print(infos)
                      raise err
                    
                    if AnnoLanguage=="German":
                      audio_code = audio_code.replace("{German_DurationMax}",str(Durations["German_DurationMax"]))
                      audio_code = audio_code.replace("{German_DurationMin}",str(Durations["German_DurationMin"]))
                    elif AnnoLanguage=="English":
                      audio_code = audio_code.replace("{English_DurationMax}",str(Durations["English_DurationMax"]))
                      audio_code = audio_code.replace("{English_DurationMin}",str(Durations["English_DurationMin"]))
                    elif AnnoLanguage=="French":
                      audio_code = audio_code.replace("{French_DurationMax}",str(Durations["French_DurationMax"]))
                      audio_code = audio_code.replace("{French_DurationMin}",str(Durations["French_DurationMin"]))
                    elif AnnoLanguage=="Russian":
                      audio_code = audio_code.replace("{Russian_DurationMax}",str(Durations["Russian_DurationMax"]))
                      audio_code = audio_code.replace("{Russian_DurationMin}",str(Durations["Russian_DurationMin"]))
                    
                    if eventID not in filesdone:
                      filesdone.add(eventID)
                      Eventname = info["Eventname"]                
                      audio_code = audio_code.replace("{AudioGUID}",str(AudioGUID)).replace("{SoundBankID}",str(info["SoundBankID"])).replace("{Eventname}",str(Eventname))
                      audiotext_code = ""
                      
                    if todo.upper()=="AUDIOTEXT":
                      Text = "UNKNOWN"
                      if method.upper()=="C":
                        Text = customGetTextFn(eventID,AnnoLanguage,info)
                      elif method.upper()=="G":
                        Text = Texts[info["FileID"]]
                      elif method.upper()=="A":
                        Text = Texts[AnnoLanguage][info.get("1404GUID","UNKNOWN")]
                    
                    if todo.upper()=="AUDIOTEXT" and AnnoLanguage=="English": # add AudioText when we do english, to add the enlgish text
                      audiotext_code = xml_AudioTextAsset.format(AudioTextGUID=AudioTextGUID,Eventname=Eventname,AudioGUID=AudioGUID,SpeechAudioType=g_SpeechAudioType,Mood=g_Mood,Text=Text)
                    if todo.upper()=="AUDIOTEXT":
                      final_text_code[AnnoLanguage] = f"{final_text_code[AnnoLanguage]}\n{xml_textentry.format(AudioTextGUID=AudioTextGUID,Text=Text)}\n"
                    
                  final_asset_code = f"{final_asset_code}\n{audio_code}\n{audiotext_code}"
                  
                main_code = xml_base.format(StartingGUID=StartingGUID,EndGUID=CurrentGUID,SoundBankCode=final_soundbank_code,AssetCode=xml_Asset_base.format(AudioAssets=final_asset_code))
                
                for AnnoLanguage,finaltext in final_text_code.items():
                  Textxml = xml_text_base.format(TextEntries=finaltext)
                  with open(f"{destination}/text_{AnnoLanguage.lower()}.xml", "w", encoding='utf-8') as f:
                    f.write(Textxml)
                with open(f"{destination}/assets.xml", "w", encoding='utf-8') as f:
                  f.write(main_code)
                # print(audioinfos)
                print(CurrentGUID)
              
              
          else:
            print("That was not a valid folder, aborting...")
            return
          
          

  if __name__ == '__main__':
    
    main()
    
    
    
    

        
      
    
  

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


