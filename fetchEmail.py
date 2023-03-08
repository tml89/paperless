import Settings
import Logger
import re
from imap_tools import MailBoxUnencrypted, A


def fileFilter(filename):
    Logger.Log('File Filter for file' + filename, Logger.LogLevel.Debug)
    for x in Settings.FILEFILTE:
        Logger.Log('\tFilter ' + x, Logger.LogLevel.Debug)
        find = re.match(x, filename)
        if find:
            Logger.Log('\t\t ---> gefunden', Logger.LogLevel.Debug)
            return True
    return False


def fetchMail():

    user = Settings.EMAIL
    password = Settings.EMAIL_PASSWORD
    imap_url = Settings.IMAP_URL
    port = Settings.IMAP_PORT

    flags = Settings.FETCHED_TAG

    with MailBoxUnencrypted(imap_url, port).login(user, password, "INBOX") as mailbox:
        for msg in mailbox.fetch(A(no_keyword=Settings.FETCHED_TAG, seen=False), mark_seen=False):
            for att in msg.attachments:
                # only process PDF
                if not att.content_type.lower().endswith("pdf"):
                    continue

                # remove newline
                filename = att.filename.replace("\r\n", "")

                # contiune if file is in filter list
                if fileFilter(filename):
                    continue

                Logger.Log("Save Attachment: " + filename + " from: " + msg.from_,
                           Logger.LogLevel.Info)

                with open(Settings.NEXTCLOUDROOT + Settings.SOURCEDIR + "/" + filename, 'wb') as f:
                    f.write(att.payload)
                    mailbox.flag(msg.uid, flags, True)
                    f.close()
