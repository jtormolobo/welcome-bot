#!/usr/bin/env python3
# Importar la clase necesaria desde Mastodon.py
from mastodon import Mastodon
import os

PROJECT_ROOT= os.path.abspath(os.path.dirname(__file__))

mastodon = Mastodon(
    access_token = '',
    api_base_url = 'https://shrimply.social'
)

def read_id(txtfile):
    if not os.path.exists(txtfile):
        return ""
    with open(txtfile) as fin:
        id = fin.read().strip()
    return id

def read_template(templatefile):
    with open(templatefile) as fin:
        template = fin.read()
    return template

def write_id(txtfile,last_id=""):
    if not last_id:
        return
    with open(txtfile,"w") as fout:
        fout.write(f"{last_id}\n")
    
def process(id_file,templatefile):
    last_id=read_id(id_file)
    template = read_template(templatefile)
    # get notifications
    notifications=mastodon.notifications(since_id=last_id)
    for n in notifications:
        # ignore non registrated users
        if n['type'] != "admin.sign_up":
            continue
        user = n['account']['acct']
        
        mastodon.status_post(template.format(username=f"@{user}"),visibility="direct")

    if notifications:
        last_id=notifications[0].get('id',last_id)

    write_id(id_file,last_id)


if __name__=="__main__":
    process(os.path.join(PROJECT_ROOT,"lastid.txt"),os.path.join(PROJECT_ROOT,"template.txt"))