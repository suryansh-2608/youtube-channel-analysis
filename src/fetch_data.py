import requests
import pandas as pd

API_KEY = "YOUR_API_KEY"

BASE_URL = "https://www.googleapis.com/youtube/v3/"

def get_channel_stats(channel_id):
    url = BASE_URL + "channels"
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": channel_id,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "items" not in data:
        raise Exception("No channel found with the given ID.")
    
    channel_data = {
        "Channel Name": data["items"][0]["snippet"]["title"],
        "Subscribers": data["items"][0]["statistics"]["subscriberCount"],
        "Total Views": data["items"][0]["statistics"]["viewCount"],
        "Total Videos": data["items"][0]["statistics"]["videoCount"],
        "Playlist ID": data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    }
    return channel_data

chanel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
channel_stats = get_channel_stats(chanel_id)

df = pd.DataFrame([channel_stats])

df.to_csv("../data/channel_stats.csv", index=False)

print("Channel stats fetched and saved successfully!")

def get_video_ids(playlist_id):
    url = BASE_URL + "playlistItems"
    video_ids = []

    next_page_token = None
    while True:
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,
            "pageToken": next_page_token,
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()

        for item in data["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])

        next_page_token = data.get("nextPageToken")

        if next_page_token is None:
            break

    return video_ids

def get_video_details(video_ids):
    url = BASE_URL + "videos"
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        params = {
            "part": "snippet,statistics",
            "id": ",".join(video_ids[i:i+50]),
            "key": API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()

        for video in data["items"]:
            video_stat = {
                "Video Title": video["snippet"]["title"],
                "Published Date": video["snippet"]["publishedAt"],
                "Views": video["statistics"].get("viewCount", 0),
                "Likes": video["statistics"].get("likeCount", 0),
                "Comments": video["statistics"].get("commentCount", 0),
            }
            all_video_stats.append(video_stat)
    return all_video_stats

playlist_id = channel_stats["Playlist ID"]
video_ids = get_video_ids(playlist_id)

print(f"Total videos fetched: {len(video_ids)}")

video_details = get_video_details(video_ids)

video_df = pd.DataFrame(video_details)

video_df.to_csv("../data/video_data.csv", index=False)

print("Video data fetched and saved successfully!")
