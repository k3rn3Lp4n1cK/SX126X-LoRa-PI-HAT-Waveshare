class Terpreter(object):
    def __init__(self, text):
        self.text = text
        self.current_token = None
    
    def error(self):
        raise Exception('[-] Error parsing Input')

    def get_next_token(self):
        text = self.text
        
        if text == 'help':
            print("[+] Help Menu")
        if text == 'settings':
            print("[+] Settings")

    def expr(self):
        self.current_token = self.get_next_token()

