import requests
import Settings

def SendNotification(title, body, receipment):

    url = Settings.NEXTCLOUD_URL+'/ocs/v2.php/apps/notifications/api/v1/admin_notifications/' + receipment
    msgObj = {'shortMessage': title, 
            "longMessage" : body}

    #use the 'headers' parameter to set the HTTP headers:
    x = requests.post(url, auth=(Settings.NEXTCLOUD_USERNAME,Settings.NEXTCLOUD_PASSWORD), data = msgObj, headers = {"OCS-APIREQUEST": "true"})

    #print(x.text)
    return x.ok