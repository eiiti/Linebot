"""
オウム返し Line Bot
"""

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
)

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))


def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """ TextMessage handler """
    input_text = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello World'))
#        TextSendMessage(text=input_text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # ユーザーから送られてきた画像を一時ファイルとして保存
    message_content = line_bot_api.get_message_content(event.message.id)
    file_path = "/tmp/sent-image.jpg"
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # Rekognition で感情分析する

    # 返答を送信する

    # file_path の画像を削除
    os.remove(file_path)
