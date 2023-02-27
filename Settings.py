import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

NEXTCLOUD_URL = os.environ.get('NEXTCLOUD_URL')
NEXTCLOUD_USERNAME = os.getenv('NEXTCLOUD_USERNAME')
NEXTCLOUD_PASSWORD = os.getenv('NEXTCLOUD_PASSWORD')

#    Info = 1
#    Warning = 2
#    Error = 3
#    Debug = 4
LOGLEVEL = 3

NEXTCLOUDROOT =  "/mnt/nextcloudSync/"  
SOURCEDIR = "Inbox"  
DESTDIR = "Inbox"

SEARCHANDPATH =	{  
  "Dokumente/Hetzner/": ["Hetzner", "Rechnung"],  
  "Dokumente/Allianz/Private Krankenversicherung/Leistungsabrechnung": ["AK-9447498434","Abrechnung","Leistungsauftrag","AMP100UV"],  
  "Emma/PKV/Leistungsabrechnung": ["AK-9447498434","Abrechnung","Leistungsauftrag","AMP90PU"],  
  "Dokumente/Klarmobil/Rechnung" : ["klarmobil", "Vertragsabrechnungen"],  
  "Dokumente/Verdienstabrechnung/2023" : ["S-Payment", "Verdienstabrechnung", "2023"],
  "Dokumente/1&1 DSL/Rechnungen" :  ["1&1 Telecom GmbH", "49057076", "Sammelrechnung"],
  "Dokumente/Kreissparkasse Tübingen/Kontoauszüge" : ["Kontoauszug", "Kreissparkasse Tübingen"],
  "Dokumente/Kreissparkasse Tübingen/Kreditkartenabrechnung" : ["BCS Kartenservice", "Abrechnung" , "Verfügungsrahmen"] 
}

IGNORE_DATES = {
    datetime.datetime(1989, 12, 20),
    datetime.datetime(1989, 10, 8),
    datetime.datetime(2021, 5, 21)
}