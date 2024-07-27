from instagrapi import Client, exceptions
from dotenv import load_dotenv
from json import dump, load
from time import sleep
from os import getenv
from rich import print

load_dotenv()
username = getenv('USERNAME', input(">>> What's username of your account? "))
password = getenv('PASSWORD')
delay = int(getenv('DELAY', '2'))
link = getenv('POST_LINK')

condations = {
	"a": "Hello"
}

try:
    # check for config availability, validity & relativity
    bot = Client(load(open(f'config_{username}.json')))
    assert bot.account_info().username == username.lower(), "Session's irrelevant; please change the username variable to an existing valid config file"
except (FileNotFoundError, exceptions.LoginRequired):
    bot = Client()
    bot.login(username=username, password=password or input(f">>> What's password of {username}? "))
    dump(bot.get_settings(), open(f"config_{username}.json", "w"), indent=4, ensure_ascii=False)

comments = bot.media_comments(bot.media_pk_from_url(link))
answered = []

while 1:
	for comment in comments:
		if comment.text in condations and not comment.user.username in answered:
			bot.direct_send(condations[comment.text], user_ids=[comment.user.pk])
			answered.append(comment.user.username)

	sleep(delay*60)