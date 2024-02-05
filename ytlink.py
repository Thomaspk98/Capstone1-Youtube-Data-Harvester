import googleapiclient.discovery
import json
import pprint
import isodate

class scrapYT():

    api_service_name = "youtube"
    api_version = "v3"
    myAPIkey = "AIzaSyDouJMzVUZUSs4wcJjG2MGx7h1JBw3v734"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = myAPIkey)

    #input video ID, get list of comment threads in video

    def commentbyVID(self,vid,number=10):
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=vid,
            maxResults=number,
            order="relevance" 
        )

        response = request.execute()
        resp={}

        for x in range(number):
            resid=f'com{x}'
            comment=response['items'][x]

            comID=comment['id']
            vidID=comment['snippet']['topLevelComment']['snippet']['videoId']
            comtext=comment['snippet']['topLevelComment']['snippet']['textOriginal']
            comauthor=comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comPD=comment['snippet']['topLevelComment']['snippet']['publishedAt']            
            
            item={'Comment ID':comID,
                  'Video ID':vidID,
                  'Text':comtext,
                  'Author':comauthor,
                  'Published on':comPD
                  }
            resp[resid]=item

        return(resp)

    #input channel ID, get channel details
    def channelbyID(self,cID,number=1):
        request = self.youtube.channels().list(
            part="snippet,statistics,status",
            id=cID,
            maxResults=number
        )
        
        response = request.execute()
        channel=response['items'][0]

        chID=channel['id']
        chName=channel['snippet']['title']
        chDes=channel['snippet']['description']
        chSubs=channel['statistics']['subscriberCount']
        chViews=channel['statistics']['viewCount']
        chStatus=channel['status']['privacyStatus']

        resp={'Channel ID':chID,
              'CHannel Name':chName,
              'Channel Description':chDes,
              'Subscriber Count':chSubs,
              'Channel Views':chViews,
              'Channel Status':chStatus
              }


        return(resp)
    
    #get video ID
    def videobyID(self): 
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id="R83W2XR3IC8"
        )
        response = request.execute()

        video = response['items'][0]

        viID=video['id']
        chID=video['snippet']['channelId']
        playID=video['snippet']['playlistId'] if 'playlistId' in video['snippet'] else None
        viName=video['snippet']['title']
        pubDate=video['snippet']['publishedAt']
        viewCount=video['statistics']['viewCount']
        likeCount=video['statistics']['likeCount']
        comCount=video['statistics']['commentCount']
        dur=str(isodate.parse_duration(video['contentDetails']['duration']))
        thumb=video['snippet']['thumbnails']['medium']['url']

        resp = {
            'Video ID': viID,
            'Channel ID': chID,
            'Playlist ID': playID,
            'Video Name': viName,
            'Published Date': pubDate,
            'View Count': viewCount,
            'Like Count': likeCount,
            'Comment Count': comCount,
            'Duration': dur,
            'Thumbnail': thumb
        }


        return(resp)    

    #get channel ID
    def playlistbyCID(self, cID, number=10):
        request = self.youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=cID,
            maxResults=number

        )
        response = request.execute()
        resp = {}

        for x in range(number):
            playlist=response['items'][x]

            playlist_id=playlist['id']
            channel_id=playlist['snippet']['channelId']
            playlist_name=playlist['snippet']['title']
            playCount=playlist['contentDetails']['itemCount']

            resp[f'res{x}'] = {
                'Playlist ID': playlist_id,
                'Channel ID': channel_id,
                'Playlist Name': playlist_name,
                'Number of Videos':playCount,
            }

        return(resp)


    #get playlist ID
    def playlistitemsbyPID(self):
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=20,
            playlistId="PLBCF2DAC6FFB574DE"
        )
        response = request.execute()
        return(response)
    
    #get: channel ID, max results, search query, search type(Channel, Video or Playlist)
    def search(self,s_query,cid="",number=5,s_order="relevance",s_type="channel"):
        request = self.youtube.search().list(
            part="snippet",
            q=s_query,
            channelId=cid,
            maxResults=number,
            order=s_order,            
            type=s_type
        )
        
        response = request.execute()
        resp={}

        if s_type=="channel":
            for x in range(number):
                resid=f'res{x}'
                search=response['items'][x]['snippet']
                
                chID=search['channelId']
                chName=search['channelTitle']
                chThumb=search['thumbnails']['medium']['url']

                item={'Channel ID':chID,
                      'Channel Name':chName,
                      'Thumbnail':chThumb
                      }
                
                resp[resid]=item

            return(resp)
        
        if s_type=="video":
            for x in range(number):
                resid=f'res{x}'
                search=response['items'][x]['snippet']

                chID=search['channelId']
                chName=search['channelTitle']
                vID=response['items'][x]['id']['videoId']
                vName=search['title']
                vThumb=search['thumbnails']['medium']['url']

                item={'Channel ID':chID,
                      'Channel Name':chName,
                      'Video ID':vID,
                      'Name':vName,
                      'Thumbnail':vThumb
                      }
                
                resp[resid]=item
            return(resp)



yt=scrapYT()
data=yt.playlistbyCID('UCeeFfhMcJa1kjtfZAGskOCA')

print(json.dumps(data,indent=4))

