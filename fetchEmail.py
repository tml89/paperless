import Settings
import Logger
from imap_tools import MailBoxUnencrypted, A


def fetchMail():

    user = Settings.EMAIL
    password = Settings.EMAIL_PASSWORD
    imap_url = Settings.IMAP_URL
    port = Settings.IMAP_PORT

    flags = Settings.FETCHED_TAG

    with MailBoxUnencrypted(imap_url, port).login(user, password, "INBOX") as mailbox:
        for msg in mailbox.fetch(A(no_keyword=Settings.FETCHED_TAG, seen=False), mark_seen=False):
            for att in msg.attachments:
                if not att.content_type.lower().endswith("pdf"):
                    continue
                filename = att.filename.replace("\r\n", "")
                Logger.Log("Save Attachment: " + filename + " from: " + msg.from_,
                           Logger.LogLevel.Info)
                with open(Settings.NEXTCLOUDROOT + Settings.SOURCEDIR + "/" + filename, 'wb') as f:
                    f.write(att.payload)
                    mailbox.flag(msg.uid, flags, True)
                    f.close()
