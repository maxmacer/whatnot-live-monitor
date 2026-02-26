import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from config import REQUESTS_TIMEOUT

class Whatnot:
    def __init__(self):
        self.GET_STREAM_URL = 'https://api.whatnot.com/graphql/?operationName=GetLivestreams'
        self.GET_STREAM_HEADERS = {'Host':'api.whatnot.com','apollographql-client-name':'com.whatnot-apollo-ios'}
            
    def stream_scrape(self, user: str):
        payload = {
          "operationName": "GetLivestreams",
          "query": "query GetLivestreams($id: ID, $username: String, $after: String, $size: Int, $statuses: [LiveStreamStatus!]) {\n  getUser(id: $id, username: $username) {\n    livestreams(after: $after, first: $size, statuses: $statuses) {\n      edges {\n        node {\n          id\n          title\n          status\n          startTime\n          activeViewers\n          streamService\n          streamAgoraAppId\n          thumbnail {\n            smallImage: url(width: 414, height: 640, format: WEBP, fit: COVER)\n            biggerImage: url(width: 642, height: 992, format: WEBP, fit: COVER)\n            fullSizeImage: url(format: WEBP, fit: COVER)\n          }\n          user {\n            username\n            id\n            profileImage {\n              bucket\n              key\n            }\n          }\n          tags {\n            label\n          }\n        }\n      }\n    }\n  }\n}",
          "variables": {
            "after": None,
            "size": 10,
            "statuses": ["PLAYING"],
            "username": user
          }
        }
        
        try:
            r = requests.post(url=self.GET_STREAM_URL,headers=self.GET_STREAM_HEADERS,json=payload,timeout=REQUESTS_TIMEOUT)
            r.raise_for_status()
            return r.json()
        except HTTPError:
            print(f'[-] Scrape Request Failed With Status Code: {r.status_code}')
        except Timeout:
            print('[-] Scrape Request Timed Out')
        except (RequestException, Exception) as e:
            print(f'[-] Scrape Request Failed With Reason: {str(e)}')
        return None
    
    def check_if_user_live(self, user: str) -> dict:
        response = self.stream_scrape(user)
        default_response = {'live': False, 'details': {}, 'error': False}

        if not response:
            return {**default_response, 'error':True}
        
        stream_data = (response.get('data',{})
                               .get('getUser',{})
                               .get('livestreams',{})
                               .get('edges',[]))
        
        if stream_data:
            stream_details = stream_data[0].get('node',{})
            return {**default_response, 'live':True, 'details':stream_details}
        else:
            return default_response