import os
from googleapiclient.discovery import build
import datetime
import tqdm as tq
from colorama import  Back, Fore
import keyboard

# Do not change following 2 lines
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
 
# Set up API credentials
API_KEY = input("Enter The Api Key: ") # Change this to your own key
CHANNEL_ID = input("Enter the Channel ID: ")  # Change this to the Channel Username
 
# Build the YouTube API client
api_service_name = "youtube"
api_version = "v3"
api_key = os.environ.get("API_KEY")
youtube_client = build(api_service_name, api_version, developerKey=API_KEY)

#Tkinter GUI


# Write your code to fetch details using youtube_client
def ChannelInfo(channel_id): # to get global values like subscriber count and video count
    request = youtube_client.channels().list(
        part="statistics",
        id= channel_id
    )
 
    response = request.execute()
    #print(response)
    stats = response["items"][0]["statistics"]
 
    subscriber_count = stats["subscriberCount"]
    video_count = stats["videoCount"]
    info = [subscriber_count , video_count]
    # returning the value subscriver count and video count
    return info

def publishing_freq(channel_id): #to find the publishing frequency videos per month
    request = youtube_client.channels().list(
        part="statistics",
        id= channel_id
    )
    response = request.execute()
    #print(response)
    stats = response["items"][0]["statistics"]
 
    videos = int(stats["videoCount"])
 
    response1 = youtube_client.channels().list(
        part='snippet',
        id=channel_id
    ).execute()
 
    channel_data  = response1["items"][0]["snippet"] 
    creation_date = channel_data.get('publishedAt') # geting the creation date of youtube channel
    creation_date = creation_date.split('T')
    dateX = creation_date[0] .split('-')
    year = int(dateX[0])
    month = int(dateX[1])
    day = int(dateX[2])
 
    st_date = datetime.datetime(year,month,day)
    end_date = datetime.date.today()
    months = (end_date.year - st_date.year) * 12 + (end_date.month - st_date.month) #finding the no. of months from the creation date
 
    publishing_freq = int(videos/months)
    return publishing_freq
 
class Engagment_Rate: #calculate the top10 videos based on engagment rate
    def __init__(self, api_key): # setting up the class 
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
 
 
    def Video_Stats(self, video_id): # getting likes views and publishing time
        request = self.youtube.videos().list(
            part='snippet,statistics',  # Include 'snippet' along with 'statistics'
            id=video_id
        )
        response = request.execute()
 
        if 'items' in response and len(response['items']) > 0:
            item = response['items'][0]
            statistics = item['statistics']
            snippet = item['snippet']  # Extract the 'snippet' information
 
            if 'likeCount' in statistics and 'viewCount' in statistics:
                return {
                    'video_id': video_id,
                    'likes': int(statistics['likeCount']),
                    'views': int(statistics['viewCount']),
                    'publishing_time': snippet['publishedAt'],  # Publishing time of the video
                }
 
        return None

    def Video_ID(self, channel_id):
        video_ids = []
        next_page_token = None

        while True:
            request = self.youtube.search().list(
                part='id',
                maxResults=50,  # Adjust this value if needed
                pageToken=next_page_token
            )
            response = request.execute()
            items = response.get('items', [])
            video_ids.extend([item['id']['videoId'] for item in items])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return video_ids

    
    def Engagment(self, id): #to calculate the engagment rate by values from above functions 
        
 
        video_ids = self.Video_ID(id)
        video_data = []
 
        # Create a tqdm instance to show the progress bar for video data fetching
        with tq.tqdm(total=len(video_ids), desc='Fetching video data', unit='video') as pbar:
            for video_id in video_ids:
                data = self.Video_Stats(video_id)
                if data:
                    likes = data['likes']
                    views = data['views']
                    engagement_rate = likes / views if views > 0 else 0.0
                    data['engagement_rate'] = engagement_rate
                    video_data.append(data)
                pbar.update(1)
 
        return video_data
 
 
def OptimalTime(channel_id): #function to find the optimal publishing time
    video_ids = Engagment_Rate(API_KEY).Video_ID(channel_id)

    # Dictionary to store engagement rates for each 4-hour time slot
    time_slot_engagement = {
        '0-4': [],
        '4-8': [],
        '8-12': [],
        '12-16': [],
        '16-20': [],
        '20-24': [],
    }

    # Create a tqdm instance to show the progress bar for video data fetching
    with tq.tqdm(total=len(video_ids), desc='Calculating engagement rates', unit='video') as pbar:
        for video_id in video_ids:
            data = Engagment_Rate(API_KEY).Video_Stats(video_id)
            if data:
                likes = data['likes']
                views = data['views']
                engagement_rate = likes / views if views > 0 else 0.0
                publishing_time = data['publishing_time']

                # Extract the hour from the publishing time
                hour_of_day = datetime.datetime.strptime(publishing_time, f'%Y-%m-%dT%H:%M:%SZ').hour

                # Update the dictionary with engagement rate for the corresponding time slot
                if 0 <= hour_of_day < 4:
                    time_slot_engagement['0-4'].append(engagement_rate)
                elif 4 <= hour_of_day < 8:
                    time_slot_engagement['4-8'].append(engagement_rate)
                elif 8 <= hour_of_day < 12:
                    time_slot_engagement['8-12'].append(engagement_rate)
                elif 12 <= hour_of_day < 16:
                    time_slot_engagement['12-16'].append(engagement_rate)
                elif 16 <= hour_of_day < 20:
                    time_slot_engagement['16-20'].append(engagement_rate)
                else:
                    time_slot_engagement['20-24'].append(engagement_rate)
            pbar.update(1)

    # Calculate the average engagement rate for each time slot
    average_engagement_by_time = {
        slot: sum(engagement_rates) / len(engagement_rates)
        for slot, engagement_rates in time_slot_engagement.items()
    }

    # Find the time slot with the highest average engagement rate
    optimal_publishing_time = max(average_engagement_by_time, key=average_engagement_by_time.get)

    return optimal_publishing_time



def main(): #execute all above functions 
    #try:
        MainData = Engagment_Rate(API_KEY)
        engagmentRate = MainData.Engagment(CHANNEL_ID)
        engagmentRate.sort(key=lambda x: x['engagement_rate'], reverse=True)
        print('\n')
        timeSlot = OptimalTime(CHANNEL_ID)
        
        
        for data in engagmentRate[:10]:
            print(f"Video ID: {Fore.GREEN+ data['video_id']}, Engagement Rate: {data['engagement_rate']:.2f}")
            
        SubscriberCount = ChannelInfo(CHANNEL_ID)[0]
        VideoCount = ChannelInfo(CHANNEL_ID)[1]
        publishingFreq  = publishing_freq(CHANNEL_ID)
        print(f"subscriberCount:{Fore.GREEN + str(SubscriberCount)}")
        print(f"videoCount: {Fore.GREEN +str(VideoCount)}")
        print(f"PublishingFrequency: {Fore.GREEN + str(publishingFreq)}")
        print(f"Optimal Publishing Time (4-hour Slot):{Fore.GREEN+ str(timeSlot)}")
 
    #except Exception as e:
        #print(Back.RED+ "Sorry the code didn't ran properly check the API key and try again")
 

# final call to execute the code
if  __name__ == '__main__': 
    main()
    input("press any key to continue....")

