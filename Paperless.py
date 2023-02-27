import tempfile
import subprocess
import re
import os
import ocrmypdf
import dateparser
import datetime
import Logger
import Settings
import pikepdf
from tendo import singleton

# Check if another instance is already running
me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

DATE_REGEX = re.compile(
    r"(\b|(?!=([_-])))([0-9]{1,2})[\.\/-]([0-9]{1,2})[\.\/-]([0-9]{4}|[0-9]{2})(\b|(?=([_-])))|"  # noqa: E501
    r"(\b|(?!=([_-])))([0-9]{4}|[0-9]{2})[\.\/-]([0-9]{1,2})[\.\/-]([0-9]{1,2})(\b|(?=([_-])))|"  # noqa: E501
    r"(\b|(?!=([_-])))([0-9]{1,2}[\. ]+[^ ]{3,9} ([0-9]{4}|[0-9]{2}))(\b|(?=([_-])))|"  # noqa: E501
    r"(\b|(?!=([_-])))([^\W\d_]{3,9} [0-9]{1,2}, ([0-9]{4}))(\b|(?=([_-])))|"
    r"(\b|(?!=([_-])))([^\W\d_]{3,9} [0-9]{4})(\b|(?=([_-])))|"
    r"(\b|(?!=([_-])))(\b[0-9]{1,2}[ \.\/-][A-Z]{3}[ \.\/-][0-9]{4})(\b|(?=([_-])))",  # noqa: E501
)

def extract_text(pdf_file):
    text = None
    with tempfile.NamedTemporaryFile(
        mode="w+",
        dir="/var/tmp",
    ) as tmp:
        subprocess.run(
            [
                "pdftotext",
                "-q",
                "-layout",
                "-enc",
                "UTF-8",
                pdf_file,
                tmp.name,
            ],
        )
        text = tmp.read()
    return post_process_text(text)

def post_process_text(text):
    if not text:
        return None

    collapsed_spaces = re.sub(r"([^\S\r\n]+)", " ", text)
    no_leading_whitespace = re.sub(r"([\n\r]+)([^\S\n\r]+)", "\\1", collapsed_spaces)
    no_trailing_whitespace = re.sub(r"([^\S\n\r]+)$", "", no_leading_whitespace)

    # TODO: this needs a rework
    # replace \0 prevents issues with saving to postgres.
    # text may contain \0 when this character is present in PDF files.
    return no_trailing_whitespace.strip().replace("\0", " ")

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
    Logger.Log(str(found), Logger.LogLevel.Debug)
    return found

def getDate(text,pdfFile):
    Logger.Log("Get Date", Logger.LogLevel.Debug)
    if len(text) > 0:
        for m in re.finditer(DATE_REGEX, text):
                date = dateparser.parse(m.group(0), settings={'PREFER_DAY_OF_MONTH': 'first', 'DATE_ORDER': 'DMY'})
                if (
                    date is not None
                    and date.year > 1900
                    and date not in Settings.IGNORE_DATES
                ):
                    Logger.Log("Found date in Text", Logger.LogLevel.Debug)
                    return date.strftime("%Y-%m-%d")

    ##fallback to pdf creation date
    Logger.Log("Date in Text not found return creation date", Logger.LogLevel.Debug)
    pdf = pikepdf.open(pdfFile)
    pdf_info = pdf.docinfo
    creation_date_raw = pdf_info.get('/CreationDate')
    creation_date = datetime.datetime.strptime(str(creation_date_raw), "D:%Y%m%d%H%M%S%z00'00'")
    return creation_date.strftime("%Y-%m-%d")
    
#----------------------

Logger.Log("Debug log is selected", Logger.LogLevel.Debug)
Logger.Log("---- Begin Settings ----", Logger.LogLevel.Debug)
Logger.Log ("NEXTCLOUDDIR: " + Settings.NEXTCLOUDROOT, Logger.LogLevel.Debug)  
Logger.Log ("SOURCEDIR: " + Settings.SOURCEDIR, Logger.LogLevel.Debug)  
Logger.Log ("DESTDIR: " + Settings.DESTDIR, Logger.LogLevel.Debug)
Logger.Log("---- End Settings ----", Logger.LogLevel.Debug)

Logger.Log("---- Start ----", Logger.LogLevel.Info)
for sourceFilename in os.listdir(Settings.NEXTCLOUDROOT + Settings.SOURCEDIR):
    sourceFilePath = os.path.join(Settings.NEXTCLOUDROOT + Settings.SOURCEDIR, sourceFilename)
    # checking if it is a file
    if not os.path.isfile(sourceFilePath) or not sourceFilename.lower().endswith(".pdf") or sourceFilename.startswith("["): 
        continue
    
    Logger.Log("Process File: " + sourceFilename, Logger.LogLevel.Info)

    # Extrahieren des Texts aus der PDF-Datei
    text = extract_text(sourceFilePath)

    if text is None or len(text) < 50:
        try:
            Logger.Log("File got no text, OCR it", Logger.LogLevel.Warning)
            ocrmypdf.ocr(sourceFilePath, sourceFilePath, language='deu',skip_text=True, deskew=True, rotate_pages=True, progress_bar=False)
            continue
        except: #ToDo: catch correct exceptions
            Logger.Log("Cannot OCR file", Logger.LogLevel.Error)

    fileDate = getDate(text,sourceFilePath)
    Logger.Log("File date: " + fileDate, Logger.LogLevel.Debug)
    
    Logger.Log("Find destdir", Logger.LogLevel.Debug)
    currDestDir = Settings.DESTDIR  
    for path in Settings.SEARCHANDPATH:  
        tags = Settings.SEARCHANDPATH[path]  
        if matches(tags, text):  
            currDestDir = path

    #build destination path
    destFilePath = Settings.NEXTCLOUDROOT + currDestDir + "/[" + fileDate + "]" + sourceFilename
    Logger.Log("DestFilePath: " + destFilePath, Logger.LogLevel.Debug)
    Logger.Log("Move: " + sourceFilename + " to: " + destFilePath, Logger.LogLevel.Info)
    try:
        os.rename(sourceFilePath, destFilePath)
    except OSError as error:
        Logger.Log(str(error), Logger.LogLevel.Error)
Logger.Log("---- End ----", Logger.LogLevel.Info)