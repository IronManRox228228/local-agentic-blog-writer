class SessionMemory:
    def __init__(self):
        self.history = [] # List of {"role": str, "content": str}

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_context(self):
        return self.history

    def clear(self):
        self.history = []