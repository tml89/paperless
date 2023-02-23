from pypdf import PdfReader
import re
import os
import ocrmypdf
import dateparser
import datetime
from enum import Enum
import Logger

LOGLEVEL = Logger.LogLevel.Info

NEXTCLOUDDIR =  "/home/tim/Downloads/" #"/mnt/nextcloudSync/"  
SOURCEDIR = "Inbox"  
DESTDIR = SOURCEDIR

DATE_REGEX = re.compile(
    r"(\b|(?!=([_-])))([0-9]{1,2})[\.\/-]([0-9]{1,2})[\.\/-]([0-9]{4}|[0-9]{2})(\b|(?=([_-])))|"  # noqa: E501
    r"(\b|(?!=([_-])))([0-9]{4}|[0-9]{2})[\.\/-]([0-9]{1,2})[\.\/-]([0-9]{1,2})(\b|(?=([_-])))|"  # noqa: E501
    r"(\b|(?!=([_-])))([0-9]{1,2}[\. ]+[^ ]{3,9} ([0-9]{4}|[0-9]{2}))(\b|(?=([_-])))|"  # noqa: E501
    r"(\b|(?!=([_-])))([^\W\d_]{3,9} [0-9]{1,2}, ([0-9]{4}))(\b|(?=([_-])))|"
    r"(\b|(?!=([_-])))([^\W\d_]{3,9} [0-9]{4})(\b|(?=([_-])))|"
    r"(\b|(?!=([_-])))(\b[0-9]{1,2}[ \.\/-][A-Z]{3}[ \.\/-][0-9]{4})(\b|(?=([_-])))",  # noqa: E501
)

SEARCHANDPATH =	{  
  "Dokumente/Hetzner/": ["Hetzner", "Rechnung"],  
  "Dokumente/Allianz/Private Krankenversicherung/Leistungsabrechnung": ["AK-9447498434","Abrechnung","Leistungsauftrag","AMP100UV"],  
  "Emma/PKV/Leistungsabrechnung": ["AK-9447498434","Abrechnung","Leistungsauftrag","AMP90PU"],  
  "Dokumente/Klarmobil/Rechnung" : ["klarmobil", "Vertragsabrechnungen"]  
}

def matches(tags, text):  
    found = False  
    for tag in tags:  
        if text.find(tag) < 0:  
            Logger.Log('Nicht gefundender Tag: '+ tag, Logger.LogLevel.Debug)  
            found = False  
            break  
        else:
            Logger.Log('Gefundender Tag: '+ tag, Logger.LogLevel.Debug)    
            found = True  
    Logger.Log(found, Logger.LogLevel.Debug)
    return found

def getDate(text,pdfFile):
    Logger.Log("Get Date", Logger.LogLevel.Debug)
    if len(text) > 0:
        for m in re.finditer(DATE_REGEX, text):
                date = dateparser.parse(m.group(0))
                if date is not None:
                    Logger.Log("Found date in Text", Logger.LogLevel.Debug)
                    return date.strftime("%Y-%m-%d")

    ##fallback to pdf creation date
    Logger.Log("Date in Text not found return creation date", Logger.LogLevel.Debug)
    pdf_info = pdfFile.metadata
    return pdf_info.creation_date.strftime("%Y-%m-%d")
    
#----------------------

Logger.Log("Debug log is selected", Logger.LogLevel.Debug)
Logger.Log("---- Begin Settings ----", Logger.LogLevel.Debug)
Logger.log ("NEXTCLOUDDIR: " + NEXTCLOUDDIR, Logger.LogLevel.Debug)  
Logger.log ("SOURCEDIR: " + SOURCEDIR, Logger.LogLevel.Debug)  
Logger.log ("DESTDIR: " + DESTDIR, Logger.LogLevel.Debug)
Logger.Log("---- End Settings ----", Logger.LogLevel.Debug)

Logger.Log("---- Start ----", Logger.LogLevel.Info)
for sourceFilename in os.listdir(NEXTCLOUDDIR + SOURCEDIR):
    sourceFilePath = os.path.join(NEXTCLOUDDIR + SOURCEDIR, sourceFilename)
    # checking if it is a file
    if not os.path.isfile(sourceFilePath) or not sourceFilename.endswith(".pdf"):# or filename.startswith("["): 
        continue
    
    Logger.Log("Read File: " + sourceFilename, Logger.LogLevel.Debug)

    # Öffnen der PDF-Datei
    reader = PdfReader(sourceFilePath)
    number_of_pages = len(reader.pages)

    Logger.Log("Number of Pages: " + number_of_pages, Logger.LogLevel.Debug)

    # Extrahieren des Texts aus der PDF-Datei
    text = ''
    for page in reader.pages:
        text += page.extract_text()

    if text is None or len(text) < 50:
        try:
            Logger.Log("File got no text, OCR it", Logger.LogLevel.Warning)
            ocrmypdf.ocr(sourceFilePath, sourceFilePath, language='deu',skip_text=True, deskew=True, rotate_pages=True, progress_bar=False)
            continue
        except: #ToDo: catch correct exceptions
            Logger.Log("Cannot OCR file", Logger.LogLevel.Error)

    fileDate = getDate(text,reader)
    Logger.Log("File date: " + fileDate, Logger.LogLevel.Debug)
    
    Logger.Log("Find destdir" + fileDate, Logger.LogLevel.Debug)
    currDestDir = DESTDIR  
    for path in SEARCHANDPATH:  
        tags = SEARCHANDPATH[path]  
        if matches(tags, text):  
            currDestDir = path

    #build destination path
    destFilePath = NEXTCLOUDDIR + currDestDir + "/[" + fileDate + "]" + sourceFilename
    Logger.Log("DestFilePath: " + destFilePath, Logger.LogLevel.Debug)

    Logger.Log("Move: " + sourceFilePath + " to: " + destFilePath, Logger.LogLevel.Info)
    os.rename(sourceFilePath, destFilePath)
    Logger.Log("---- End ----", Logger.LogLevel.Info)