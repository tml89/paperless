from pypdf import PdfReader
import re
import os
import ocrmypdf
import dateparser

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

print ("NEXTCLOUDDIR: " + NEXTCLOUDDIR)  
print ("SOURCEDIR: " + SOURCEDIR)  
print ("DESTDIR: " + DESTDIR)

def matches(tags, text):  
    found = False  
    for tag in tags:  
        if text.find(tag) < 0:  
            #print('Nicht gefundender Tag: ', tag)  
            found = False  
            break  
        else:  
            #print('Gefundener Tag: ', tag)  
            found = True  
    #print(found)  
    return found

def getDate(text,pdfFile):
    if len(text) > 0:
        for m in re.finditer(DATE_REGEX, text):
                date = dateparser.parse(m.group(0))
                if date is not None:
                    return date.strftime("%Y-%m-%d")

    ##fallback to pdf creation date
    pdf_info = pdfFile.metadata
    return pdf_info.creation_date.strftime("%Y-%m-%d")
    
#----------------------

for filename in os.listdir(NEXTCLOUDDIR + SOURCEDIR):
    f = os.path.join(NEXTCLOUDDIR + SOURCEDIR, filename)
    # checking if it is a file
    if not os.path.isfile(f) or not filename.endswith(".pdf"):# or filename.startswith("["): 
        continue
    
    print (filename)

    # Öffnen der PDF-Datei
    reader = PdfReader(f)
    number_of_pages = len(reader.pages)

    # Extrahieren des Texts aus der PDF-Datei
    text = ''
    for page in reader.pages:
        text += page.extract_text()

    if len(text) <= 0:
        try:
            print ("OCR it!")
            ocrmypdf.ocr(f, f, language='deu',skip_text=True, deskew=True, rotate_pages=True, progress_bar=False)
            continue
        except:
            print ("Cannot OCR File")

    fileDate = getDate(text,reader)
    
    currDestDir = DESTDIR  
    for path in SEARCHANDPATH:  
        tags = SEARCHANDPATH[path]  
        if matches(tags, text):  
            pass#currDestDir = path

    print (NEXTCLOUDDIR + currDestDir + "/[" + fileDate + "]" + filename)  
          
          
        