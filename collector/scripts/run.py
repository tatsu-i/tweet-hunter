import os
import json
import yaml
import tweepy
from datetime import timedelta
from elasticsearch import Elasticsearch
from elasticsearch_dsl import UpdateByQuery

API_KEY = os.environ.get("TWITTER_API_KEY", "")
API_SECRET_KEY = os.environ.get("TWITTER_API_SECRET_KEY", "")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

es = Elasticsearch(hosts=[{"host": "elasticsearch", "port": 9200}])
with open("/scripts/template.json", "r") as f:
    print("update template")
    es.indices.put_template(name="tweet", body=json.load(f))

follow = []
conf = {}
with open("/conf/config.yaml") as f:
    conf = yaml.safe_load(f)
    for l in conf["list"].keys():
        for user in conf["list"][l]:
            id_str = user["id"]
            username = user["name"]
            follow.append(id_str)
            ubq = UpdateByQuery(using=es, index="tweet*")
            query = (
                ubq.query("match", user__id_str__keyword=id_str)
                .script(
                    source="""
                        int i = 0;
                        int found = 0;
                        if (ctx._source.list_name == null){
                            ctx._source.list_name = [];
                        }
                        for(i = 0; i < ctx._source.list_name.size(); i++){
                            if (ctx._source.list_name[i] == params.list_name){
                                found = 1;
                                break;
                            }
                        }
                        if (found == 0){
                            ctx._source.list_name.add(params.list_name);
                        }
                        ctx._source.user.screen_name = params.username;
                    """,
                    params={"list_name": l, "username": username}
                )
            )
            resp = query.execute()

# StreamListenerを継承するクラスListener作成
class Listener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            body = status._json
            body["@timestamp"] = status.created_at
            body["list_name"] = []
            for l in conf["list"].keys():
                for user in conf["list"][l]:
                    id_str = user["id"]
                    if body["user"]["id_str"] == id_str:
                        body["list_name"].append(l)
            es.index("tweet", body=body)
        except Exception as e:
            print(e)
        return True

    def on_delete(self, status_id, user_id):
        ubq = UpdateByQuery(using=es, index="tweet*")
        query = (
            ubq.query("match", id_str__keyword=str(status_id))
            .query("match", user__id_str__keyword=str(user_id))
            .script(source="ctx._source.delete = true")
        )
        resp = query.execute()
        print(f"deleted {status_id} {user_id} {resp.to_dict()}")
        return

    def on_error(self, status_code):
        print("エラー発生: " + str(status_code))
        return True

    def on_timeout(self):
        print("Timeout...")
        return True


# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Listenerクラスのインスタンス
listener = Listener()
# 受信開始
stream = tweepy.Stream(auth, listener)

print(f"start collect stream {len(follow)} users")
stream.filter(follow=follow)
