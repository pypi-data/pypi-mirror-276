import websocket
import json

FLOW_END = 2

class Step:
    def __init__(self, name, type, alias_name, node_type):
        self.name = name
        self.type = type
        self.alias_name = alias_name
        self.node_type = node_type

class Header:
    def __init__(self, code, message, sid, status, flow_status, step, flow_progress, flow_data_type, **kwargs):
        self.code = code
        self.message = message
        self.sid = sid
        self.status = status
        self.flow_status = flow_status
        self.step = Step(**step)
        self.flow_progress = flow_progress
        self.flow_data_type = flow_data_type
        for key, value in kwargs.items():
            setattr(self, key, value)

class Text:
    def __init__(self, content, index, role):
        self.content = content
        self.index = index
        self.role = role

class Choices:
    def __init__(self, status, seq, text):
        self.status = status
        self.seq = seq
        self.text = [Text(**t) for t in text]

class UsageText:
    def __init__(self, completion_tokens, question_tokens, prompt_tokens, total_tokens):
        self.completion_tokens = completion_tokens
        self.question_tokens = question_tokens
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens

class Usage:
    def __init__(self, text):
        self.text = UsageText(**text)

class Payload:
    def __init__(self, choices, usage=None):
        self.choices = Choices(**choices)
        if usage:
            self.usage = Usage(**usage)
        else:
            self.usage = None

class Chat:
    def __init__(self, header, payload):
        self.header = Header(**header)
        self.payload = Payload(**payload)

class ChatError(Exception):
    pass

def chat(host, flow_id, question):
    # 连接WebSocket服务器
    try:
        # print(f"url = ws://{host}/api/v1/chat/{flow_id}")
        ws = websocket.create_connection(f"ws://{host}/api/v1/chat/{flow_id}")
    except Exception as e:
        raise ChatError(f"Chat connection error: {str(e)}") from e
    accumulated_content = ""
    try:
        # 发送消息
        message = json.dumps({"inputs": {"__input__": f"{question}"}})
        ws.send(message)

        # 读取消息
        while True:
            try:
                message = ws.recv()
            except Exception as e:
                raise ChatError(f"Chat read message error: {str(e)}") from e

            try:
                c = json.loads(message)
                chat = Chat(**c)
            except json.JSONDecodeError as e:
                raise ChatError(f"Chat unmarshal message error: {str(e)}, content: {message}") from e

            if chat.header.flow_status == FLOW_END:
                if chat.header.code != 0:
                    raise ChatError(f"Code: {chat.header.code}, chat error: {chat.header.message}")
                else:
                    for text in chat.payload.choices.text:
                        accumulated_content += text.content
                if chat.header.status == FLOW_END:
                    break

            if not message:
                raise ChatError("No message is returned for the connection, but the flow status not equals 2")

    finally:
        ws.close()

    return accumulated_content

def run():
    host = "chain-dev.xfyun.cn"
    flow_id = "7202681315132346368"

    import argparse

    parser = argparse.ArgumentParser(description="Chat with WebSocket server.")
    #parser.add_argument("host", help="The host of the WebSocket server")
    #parser.add_argument("flow_id", help="The flow ID for the chat")
    parser.add_argument("queston", help="any question for chat")

    args = parser.parse_args()

    try:
        result = chat(host, flow_id, args.queston)
        print(f"Chat finished with result: {result}")
    except ChatError as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    host = "chain-dev.xfyun.cn"
    flow_id = "7202681315132346368"

    import argparse

    parser = argparse.ArgumentParser(description="Chat with WebSocket server.")
    #parser.add_argument("host", help="The host of the WebSocket server")
    #parser.add_argument("flow_id", help="The flow ID for the chat")
    parser.add_argument("queston", help="any question for chat")

    args = parser.parse_args()

    try:
        result = chat(host, flow_id, args.queston)
        print(f"Chat finished with result: {result}")
    except ChatError as e:
        print(f"An error occurred: {str(e)}")
