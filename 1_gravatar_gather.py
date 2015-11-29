# Gathers a collection of gravatars from GithubArchive timeline and saves
# them along with a cvs file listing repository, actor, avatar image size and
# a guess whether the image is a photo or not


import pandas as pd
import time
import requests
from PIL import Image
from StringIO import StringIO
import re
import os

LIMIT = 1000

query  = """SELECT repository_url, payload_member_avatar_url FROM
        [githubarchive:github.timeline] where payload_member_avatar_url != ''
        LIMIT """ + LIMIT
df = pd.io.gbq.read_gbq(project_id = 'metacommunities', query = query)


def save_avatar(df):
    for i in df.index:
        url = df.ix[i, 'payload_member_avatar_url']
        r = requests.get(url, stream=True)
        image_size = r.headers['content-length']
        im = Image.open(StringIO(r.content))
        name = url.replace('https://avatars.githubusercontent.com/u/', '').replace('?', '').replace('v=3', '') + '.png'
        im.save(str(name))
        df.ix[i, ['image_file', 'image_size']] = [name, image_size]
        print df.ix[i]
    return df


df['image_size'] = 1500
df['image_file'] = ''

save_avatar(df)
df['image_size'] = df['image_size'].astype(int)
df['has_photo'] = df['image_size'] > 2000
df.to_csv('avatar_icon_sample_1000.csv')


def classify_training_set(dir):
    files = os.listdir(dir)
    os.chdir(dir)
    not_icons = []
    for f in files:
        if os.stat(f).st_size > 4000:
            not_icons.append(f)
    return not_icons

photos = classify_training_set('data')

def get_file_sizes(dir):
    files = os.listdir(dir)
    os.chdir(dir)
    not_icons = []
    for f in files:
        not_icons.append(os.stat(f).st_size)
    return not_icons
