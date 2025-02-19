import googleapiclient.discovery

API_KEY = "YOUR API KEY"
USERNAME = "YOUR YouTube Channel Username"  

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def get_channel_id(username):
    response = youtube.search().list(
        part="snippet",
        q=username,
        type="channel",
        maxResults=1
    ).execute()

    if "items" in response and response["items"]:
        return response["items"][0]["id"]["channelId"]
    else:
        print("❌ Kanal topilmadi!")
        return None

channel_id = get_channel_id(USERNAME)
print(f"Kanal ID: {channel_id}")
