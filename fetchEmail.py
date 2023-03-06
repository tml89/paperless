import Settings
from imap_tools import MailBoxUnencrypted, A, AND, NOT, MailMessageFlags

user = Settings.EMAIL
password = Settings.EMAIL_PASSWORD
imap_url = Settings.IMAP_URL
port = Settings.IMAP_PORT

flags = (MailMessageFlags.SEEN, Settings.FETCHED_TAG)

with MailBoxUnencrypted(imap_url,port).login(user, password, "INBOX") as mailbox:
    for msg in mailbox.fetch(A(no_keyword=Settings.FETCHED_TAG, seen=False )):
        print(msg.date, msg.subject, len(msg.text or msg.html))
        for att in msg.attachments:
           if not att.content_type.lower().endswith("pdf"):
              continue
           print(att.filename, att.content_type)
           with open(Settings.NEXTCLOUDROOT + Settings.SOURCEDIR + "/" + att.filename, 'wb') as f:
            pass#f.write(att.payload)
            mailbox.flag(msg.uid, flags, True)    

