from html.parser import HTMLParser


class HTMLRemover(HTMLParser):
    def handle_data(self, data):
        if not hasattr(self, "message"):
            self.message = ""
        self.message += data

    def getMessage(self):
        if not hasattr(self, "message"):
            return ""
        return self.message
