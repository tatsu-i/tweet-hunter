import os
import time
import fire
import tweepy

class Cli:
    def __init__(self):
        API_KEY = os.environ.get("TWITTER_API_KEY", "")
        API_SECRET_KEY = os.environ.get("TWITTER_API_SECRET_KEY", "")
        ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
        ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def get_all_list(self):
        for twilist in self.api.lists_all():
            print(f"[{twilist.slug}]")
            print("full_name="+twilist.full_name)

    def get_list_member_ids(self, listname, screen_name):
        for member in tweepy.Cursor(self.api.list_members,slug=listname, owner_screen_name=screen_name).items():
            if not member.following and not member.protected:
                member.follow()
                time.sleep(5)
            print (f'"{member.id}", # {member.screen_name}')
            time.sleep(0.3)

    def get_id(self, screen_name):
        user = self.api.get_user(screen_name) 
        ID = user.id_str 
        print("The ID of the user is : " + ID) 

fire.Fire(Cli)
