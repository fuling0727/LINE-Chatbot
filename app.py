import os
import sys

from flask import Flask, jsonify, request, abort, send_file
#from flask import current_app as app
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=["user", "riddle1", "riddle2","greet","right","giveup","wrong1","wrong1_1","wrong1_2",
    "wrong2","wrong2_1","wrong2_2"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "riddle1",
            "conditions": "is_going_to_riddle1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "riddle2",
            "conditions": "is_going_to_riddle2",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "greet",
            "conditions": "is_going_to_greet",
        },
        {
            "trigger": "advance",
            "source": ["riddle1","riddle2","wrong1","wrong1_1","wrong2","wrong2_1"],
            "dest": "right",
            "conditions": "is_going_to_right",
        },
        {
            "trigger": "advance",
            "source": ["riddle1","riddle2","wrong1","wrong1_1","wrong2","wrong2_1"],
            "dest": "giveup",
            "conditions": "is_going_to_giveup",
        },
        {
            "trigger": "advance",
            "source": "riddle1",
            "dest": "wrong1",
            "conditions": "is_going_to_wrong1",
        },
        {
            "trigger": "advance",
            "source": "wrong1",
            "dest": "wrong1_1",
            "conditions": "is_going_to_wrong1_1",
        },
        {
            "trigger": "advance",
            "source": "wrong1_1",
            "dest": "wrong1_2",
            "conditions": "is_going_to_wrong1_2",
        },
        {
            "trigger": "advance",
            "source": "riddle2",
            "dest": "wrong2",
            "conditions": "is_going_to_wrong2",
        },
        {
            "trigger": "advance",
            "source": "wrong2",
            "dest": "wrong2_1",
            "conditions": "is_going_to_wrong2_1",
        },
        {
            "trigger": "advance",
            "source": "wrong2_1",
            "dest": "wrong2_2",
            "conditions": "is_going_to_wrong2_2",
        },
        {"trigger": "go_back", "source": ["riddle2","greet","right",
        "giveup","wrong1_2","wrong2_2"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


    

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}") 
    # parse webhook body
    try:
        events = parser.parse(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        #line_bot_api.push_message(event.push_token, "Yo")
        if (event.message.text == "貼圖" or event.message.text == "漂亮" or event.message.text == "你好美") and response == False:
            message = StickerSendMessage(
                package_id='1',
                sticker_id='5'
            )
            line_bot_api.reply_message(event.reply_token, message)
        elif (event.message.text == "梗圖" or event.message.text == "醜") and response == False:
            image_url = "https://images2.gamme.com.tw/news2/2018/15/19/qaCVn6WalqaVqKQ.jpg"
            message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
            line_bot_api.reply_message(event.reply_token, message)
        elif response == False:
            send_text_message(event.reply_token, "我不懂你在說什麼...如果你想玩猜謎請輸入 1 或是 2, 如果想看梗圖請輸入 梗圖 ,也可以跟我打招呼或是稱讚我呦~")

    
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
