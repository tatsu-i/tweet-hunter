import os
import time
import fire
import yaml
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

    def get_list_member_ids(self, listname, screen_name, config_file="/conf/config.yaml"):
        conf = {}
        if os.path.exists(config_file):
            with open(config_file) as f:
                conf = yaml.safe_load(f)
        conf["list"] = conf.get("list", {})
        conf["list"][listname] = conf["list"].get(listname, [])
        for member in tweepy.Cursor(self.api.list_members,slug=listname, owner_screen_name=screen_name).items():
            if not member.following and not member.protected:
                member.follow()
                time.sleep(5)
            conf["list"][listname].append({"id":str(member.id), "name": member.screen_name})
            print (f'"{member.id}", # {member.screen_name}')
            time.sleep(0.1)
        with open(config_file, "w") as f:
            yaml.dump(conf, f)

    def get_id(self, screen_name):
        user = self.api.get_user(screen_name) 
        ID = user.id_str 
        print("The ID of the user is : " + ID) 

fire.Fire(Cli)
