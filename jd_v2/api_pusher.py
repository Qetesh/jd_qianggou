from wxpusher import WxPusher


def send_message(content):
    # 推送token
    PUSH_TOKEN = 'AT_4XxUFvSjSLWTlFhX1nFmIepe1RNoGq8b'

    UIDS = [
        'UID_D77yyDO0pT7K0f1q2UijDTGnGthF',
    ]

    msg = WxPusher.send_message(content,
                                uids=UIDS,
                                token=PUSH_TOKEN)
    return msg
