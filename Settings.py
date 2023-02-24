import datetime
#    Info = 1
#    Warning = 2
#    Error = 3
#    Debug = 4
LOGLEVEL = 3

NEXTCLOUDROOT =  "/home/tim/Downloads/Nextcloud/" #"/mnt/nextcloudSync/"  
SOURCEDIR = "Inbox/consume"  
DESTDIR = "Inbox"

SEARCHANDPATH =	{  
  "Dokumente/Hetzner/": ["Hetzner", "Rechnung"],  
  "Dokumente/Allianz/Private Krankenversicherung/Leistungsabrechnung": ["AK-9447498434","Abrechnung","Leistungsauftrag","AMP100UV"],  
  "Emma/PKV/Leistungsabrechnung": ["AK-9447498434","Abrechnung","Leistungsauftrag","AMP90PU"],  
  "Dokumente/Klarmobil/Rechnung" : ["klarmobil", "Vertragsabrechnungen"],  
  "Dokumente/Verdienstabrechnung/2023" : ["S-Payment", "Verdienstabrechnung", "2023"] 
}

IGNORE_DATES = {
    datetime.datetime(1989, 12, 20),
    datetime.datetime(1989, 10, 8),
    datetime.datetime(2021, 5, 21)
}