import os
import requests
import validators
from slack_bolt import App
from slack_sdk import WebClient
from flask import Flask, request
from bs4 import BeautifulSoup
from slack_bolt.adapter.flask import SlackRequestHandler

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SIGNING_SECRET = os.environ.get('SIGNING_SECRET')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
SERVER_KEYWORD = os.environ.get('SERVER_KEYWORD')
MAILBOX_KEYWORD = os.environ.get('MAILBOX_KEYWORD')
MENTION_USER_WITH_MSG = os.environ.get('MENTION_USER_WITH_MSG')

flask_app = Flask(__name__)
app = App(
    signing_secret=os.environ.get('SIGNING_SECRET'),
    token=os.environ.get('SLACK_BOT_TOKEN'),
)
req_handler = SlackRequestHandler(app)
client = WebClient(token=SLACK_BOT_TOKEN)


# Register routes to Flask app
@flask_app.route('/slack/events', methods=['POST'])
def slack_events():
    return req_handler.handle(request)


@app.event('message')
def handle_message_events(body, logger):
    event = body.get('event', {})
    print('------- start ------')
    if 'text' in event:
        text_link = event.get('text')
        text_link = text_link[1:]
        text_link = text_link[:-1]
        content_res = ''
        filter_keyword = ''
        if validators.url(text_link):
            html = requests.get(text_link)
            soup = BeautifulSoup(html.text, 'html.parser')
            entry_data = soup.find_all('div', {'class': 'entry'})
            for entry in entry_data:
                content_res = entry.find('div', {'class': 'entry-body'}).text

            if SERVER_KEYWORD in content_res:
                filter_keyword = '「{0}」'.format(SERVER_KEYWORD)
            if MAILBOX_KEYWORD in content_res:
                filter_keyword = '{0}「{1}」'.format(filter_keyword, MAILBOX_KEYWORD)

            if filter_keyword:
                res = client.chat_postMessage(
                    channel=CHANNEL_ID,
                    thread_ts=event.get('ts'),
                    text=MENTION_USER_WITH_MSG.format(filter_keyword),
                )
                print(res)
    print('------- end ------')


if __name__ == '__main__':
    app.run(debug=True)
