from urllib import request
from html.parser import HTMLParser
from hashlib import sha256

class ClientHTMLParser(HTMLParser):
    
    is_relevant = False
    current_msg = ""

    # when it reaches desired tag, we 
    # turn our data catcher on
    def handle_starttag(self, tag, attrs):
        if tag == "textarea":
            self.is_relevant = True

    # when it reaches desired tag end, 
    # we turn our data catcher off
    def handle_endtag(self, tag):
        if tag == "textarea":
            self.is_relevant = False

    # data catcher in action
    def handle_data(self, data):
        if self.is_relevant:
            self.current_msg = data

class ClientHandler:
    """
        It will handle lower level stuff 
        like parsing html document and
        sending POST and GET requests 
        to Client, so Client will be
        able to send and read chat 
        messages.
    """
    # hold html parser reference for 
    # proper dontpad reading
    html_parser = None


    def __init__(self):
        self.html_parser = ClientHTMLParser()

    def read(self, url):
        """
        Returns an HTTPResponse object
        """
        self.html_parser.feed(
            request.urlopen(
                request.Request(
                    url, 
                    headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, 
                    method="GET"
                )
            ).read().decode("utf-8")
        )
        return self.html_parser.current_msg
    
    def write(self, url, data, append=True):
        if append:
            self.html_parser.feed(self.read(url))
            local_data = ("text=" + self.html_parser.current_msg + "\n" + data).encode("utf-8")
        else:
            local_data = ("text=" + data).encode("utf-8")

        return request.urlopen(
            request.Request(
                url, 
                headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, 
                data = local_data, 
                method = "POST"
            )
        )

class Client:

    client_handler = None
    url = ""
    username = ""
    
    def __init__(self, username):
        self.client_handler = ClientHandler()
        self.username = username
        hashed_user = sha256(username.encode("utf-8")).hexdigest()
        self.url = "http://dontpad.com/" + hashed_user
        print("Messages storage address: ", self.url)

    def send_msg(self, msg, append=True):
        prologue = self.username + ": "
        self.client_handler.write(self.url, prologue + msg, append)
    
    def read_msg(self):
        return self.client_handler.read(self.url)


msg = "Sup, buddies, y'all good? Tested successfully."

c = Client("testing")
c.send_msg(msg, append=False)

retrieved_msg = c.read_msg()
assert retrieved_msg == c.username + ": " + msg, "diff between \n" + c.username + ": " + msg + " and " + retrieved_msg