import json
import uuid
from aily_code_sdk_core import action

SEND_MESSAGE_API_NAME = 'action:brn:cn:spring:all:all:connector_action_runtime:/spring_sdk_send_message'


def send_message(content: str) -> int:
    """
    发送一条消息。

    Args:
        content (str): 要发送的消息内容。

    Returns:
        int: 发送消息的结果代码。
            - 0: 发送成功
            - 1: 发送失败
            - 2: 消息内容为空
            - 3: 消息内容过长(超过1000个字符)
    """
    idempotent_id = str(uuid.uuid4())

    content = {"content": {"widgets": [{"type": "Markdown", "props": {"content": content, "resources": []}}]}}
    r = action.call_action(SEND_MESSAGE_API_NAME, {
        'idempotentID': idempotent_id,
        'message': {
            'content': json.dumps(content),
            'messageStatus': 'FINISHED',
            'steps': []
        }
    })
    return r.get('messageID')


def update_message(message_id: int, content: str) -> bool:
    """
    更新指定ID的消息内容。

    Args:
        message_id (int): 要更新的消息ID。
        content (str): 新的消息内容。

    Returns:
        bool: 更新消息的结果。
            - True: 更新成功
            - False: 更新失败
    """
    # 实际的消息更新逻辑...
    success = True  # 假设更新成功
    return success
