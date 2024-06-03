class ChatContextModel:
    def __init__(self, **kwargs) -> None:
        self.role = kwargs.get("role", "user")
        self.content = kwargs.get("content")

class ChatResultModel:
    def __init__(self, chat_result):
        self.chat_result = chat_result

    def __str__(self):
        return str(self.chat_result)
    
    def __repr__(self):
        return repr(self.chat_result)

    def __getattr__(self, attr):
        return getattr(self.chat_result, attr)
