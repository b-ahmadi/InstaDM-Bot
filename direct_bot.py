from instagrapi import Client, exceptions
from json import dump, load
from jdatetime import datetime
from os import getenv
from time import sleep
from rich import print

username = getenv('USERNAME', input(">>> What's username of your account? "))
password = getenv('PASSWORD')
delay = int(getenv('DELAY', '2'))

condations = {
	"Hi": "Hello"
}

try:
    # check for config availability, validity & relativity
    bot = Client(load(open(f'config_{username}.json')))
    assert bot.account_info().username == username.lower(), "Session's irrelevant; please change the username variable to an existing valid config file"
except (FileNotFoundError, exceptions.LoginRequired):
    bot = Client()
    bot.login(username=username, password=password or input(f">>> What's password of {username}? "))
    dump(bot.get_settings(), open(f"config_{username}.json", "w"), indent=4, ensure_ascii=False)


while 1:
	threads = bot.direct_threads(selected_filter="unread")
	pendings = bot.direct_pending_inbox()
	new_msgs = {}
	
	for t in [*threads, *pendings]:
	    if t in pendings:
	    	bot.direct_pending_approve(thread_id=t.id)
	    	t = bot.direct_thread(thread_id=t.pk)
	    	t_last_seen = datetime(1000,1,1)
	    else:
	    	t_last_seen = datetime.fromtimestamp(int(t.last_seen_at[str(bot.user_id)]["timestamp"]) / 1e6)
	
	    contact = str(t.users[0].pk)
	    new_msgs[contact] = []
	
	    for m in t.messages:
	        mtime = datetime.fromtimestamp(m.timestamp.timestamp())
	        if mtime > t_last_seen:
	            new_msgs[contact].append(m)
	            if m.text in condations.keys():
	            	bot.direct_send(condations[m.text], user_ids=[contact])

	sleep(delay*60)
