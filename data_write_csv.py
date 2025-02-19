import csv
import googleapiclient.discovery
import isodate

API_KEY = "YOUR API KEY"
CHANNEL_ID = "YOUR YouTube Channel ID"  

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def get_latest_video(channel_id):
    response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1
    ).execute()

    if "items" in response and response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        return video_id
    else:
        print("❌ Video topilmadi! Kanalni tekshiring.")
        return None

def get_video_details(video_id):
    response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()

    if "items" in response and response["items"]:
        item = response["items"][0]
        snippet = item["snippet"]
        statistics = item["statistics"]
        content_details = item["contentDetails"]

        return {
            "Video Title": snippet["title"],
            "Video Length (in seconds)": convert_duration_to_seconds(content_details["duration"]),
            "Upload Date and Time": snippet["publishedAt"],
            "View Count": statistics.get("viewCount", 0),
            "Like Count": statistics.get("likeCount", 0),
            "Comment Count": statistics.get("commentCount", 0),
            "Description": snippet["description"],
            "Tags": ", ".join(snippet.get("tags", [])),
            "Thumbnail URL": snippet["thumbnails"]["high"]["url"],
            "Category": snippet["categoryId"]
        }
    else:
        print("❌ Video ma'lumotlari topilmadi!")
        return None

def convert_duration_to_seconds(duration):
    return int(isodate.parse_duration(duration).total_seconds())

def save_to_csv(video_data, filename="youtube_video.csv"):
    """Videoning ma'lumotlarini CSV faylga saqlash."""
    headers = ["Video Title", "Video Length (in seconds)", "Upload Date and Time",
               "View Count", "Like Count", "Comment Count", "Description",
               "Tags", "Thumbnail URL", "Category"]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerow(video_data)

if __name__ == "__main__":
    video_id = get_latest_video(CHANNEL_ID)
    
    if video_id:
        video_details = get_video_details(video_id)
        
        if video_details:
            save_to_csv(video_details)
            print("✅ Video ma'lumotlari youtube_video.csv fayliga saqlandi!")
