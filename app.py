import os

from services import Conf ,check_password
from methods import grab_pic, stripping

from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

### data 
app = Flask(__name__) # flask conf
conf = Conf('confs/conf_line_bot_init.json') # reading conf.json to create Conf class
    # status
dev_debugging_in_process = False
get_author=False

    # line server conf var
line_bot_api = LineBotApi(conf['Channel_Access_Token']) # Channel Access Token
handler = WebhookHandler(conf['Channel_Secret']) # Channel Secret

    # available bot command
bot_command = {
    "help":"get some help.",
    "give me cat pic":"smoke some CAT.",
    "give me WHATEVER pic":"WHATEVER."
}
### data

### methods
def choose_message(event):
    global dev_debugging_in_process 
    global get_author
    global bot_command
    
    if (get_author == False) and (event.message.text == 'Apply author'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            'please enter password. get_author is {status}'.format(status = get_author)))
    elif (event.message.text == "give me cat pic") and (dev_debugging_in_process == False):
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(
            original_content_url='https://i.imgur.com/{id}.jpg'.format(id=grab_pic.grab_pic_link()),
            preview_image_url='https://i.imgur.com/{id}.jpg'.format(id=grab_pic.grab_pic_link())))
        return None # send cat pic from http://imgur.com by web crawler (spider)
    elif (stripping.is_input_have_words_in_index(event.message.text)) and (dev_debugging_in_process == False):
        text = event.message.text
        if grab_pic.grab_pic_link(text):
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                original_content_url='https://i.imgur.com/{id}.jpg'.format(
                    id=grab_pic.grab_pic_link(stripping.get_the_targetWord_in_string(text))),
                preview_image_url='https://i.imgur.com/{id}.jpg'.format(
                    id=grab_pic.grab_pic_link(stripping.get_the_targetWord_in_string(text)))))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='I don\'t have any of them...'))
        return None # send specific type of pic from http://imgur.com by web crawler (spider)
    elif event.message.text in ['help me','help me bruh','help me bro','h','-h']:
        reply_list=list(bot_command)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(bot_command[reply_list[0]],
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label=bot_command[reply_list[0]], text=reply_list[0])),
                                   QuickReplyButton(action=MessageAction(label=bot_command[reply_list[1]], text=reply_list[1])),
                                   QuickReplyButton(action=MessageAction(label=bot_command[reply_list[2]], text=reply_list[2])),
                                   QuickReplyButton(action=MessageAction(label=bot_command[reply_list[0]], text=reply_list[0])),
                                   QuickReplyButton(action=MessageAction(label=bot_command[reply_list[1]], text=reply_list[1])),
                                   QuickReplyButton(action=MessageAction(label=bot_command[reply_list[2]], text=reply_list[2]))
                               ]))
            )
        return None
    elif event.message.text == 'help':
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(
            original_content_url='https://i.imgur.com/DJIkoRf.gif',
            preview_image_url='https://i.imgur.com/DJIkoRf.gif'
        ))
        return None
    else: 
        return None

def choose_author_message(event):
    global dev_debugging_in_process 
    global get_author
    status_text='You are now in ADMIN mode. get_author is {status} . '.format(status = get_author)
    if event.message.text == 'admin:debug mode on' and get_author == True:
        dev_debugging_in_process = True
        text = 'dev_debugging_in_process is {status}'.format(
            status=dev_debugging_in_process)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=status_text+text))
        return None # set the availablility 
    elif event.message.text == 'admin:debug mode off' and get_author == True:
        dev_debugging_in_process = False
        text = 'dev_debugging_in_process is {status}'.format(
            status=dev_debugging_in_process)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=status_text+text))
        return None # set the availablility
    elif (event.message.text == 'break admin mode') and (get_author == True):
        get_author = False
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            'Getting out from ADMIN mode . get_author is {status}'.format(status = get_author)))
        return None
    else:
        return None
### methods

line_bot_api.broadcast(TextSendMessage(text='im ready! by global')) # boardcast when already deployed

# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息: 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text # accept input message
    global get_author
    print("get_author = ", get_author)
    print('dev_debugging_in_process = ', dev_debugging_in_process)
    if get_author == False :
        get_author = check_password.check_pas(event.message.text)
    elif get_author == True:
        choose_author_message(event) # check authority and password 
    
    if dev_debugging_in_process == True:
        text = "no service"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        return None # send 'no service' when i want all service be not available
    else:
        choose_message(event)
        return None # send normal reply
    
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
# server configure