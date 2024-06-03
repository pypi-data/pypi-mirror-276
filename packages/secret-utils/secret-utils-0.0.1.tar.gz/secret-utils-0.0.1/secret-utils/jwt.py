import hashlib
import codecs
import base64
import json
import time

class JWT:
    def __init__(self, user, secret, algo = 'sha256'):
        self.user = user
        self.secret = secret
        self.algo = algo

    def _hmac(self, password, salt = "HeyThere!", number = 1000000):
        password = bytes(password, 'utf-8')
        salt = bytes(salt, 'utf-8')

        return self.hex2b64(hashlib.pbkdf2_hmac(self.algo, password, salt, number).hex())

    def hex2b64(self, _hex):
        return codecs.encode(codecs.decode(_hex, 'hex'), 'base64').decode()

    def b64_Header(self, typ = 'data'):
        data = json.dumps({ "alg" : self.algo, "typ": typ })
        return base64.b64encode(bytes(data, 'utf-8')).decode('utf-8')
    
    def b64_payload(self, now):
        data = json.dumps({ "loggedInAs" : self.user, "iat": now})
        return base64.b64encode(bytes(data, 'utf-8')).decode('utf-8')

    def b64_signature(self, b64_header, b64_payload, salt):
        message = b64_header + "." + b64_payload + self.secret
        signature = self._hmac(message, salt=salt)
        return signature

    def generate(self, data, salt: str):
        header = self.b64_Header()
        payload = self.b64_payload(data)
        signature = self.b64_signature(header, payload, salt)

        b64_token = header + "." + payload + "." + signature
        
        return b64_token

if __name__ == "__main__":
    newToken = JWT("parzival", "cisco123")
    
    print(newToken.generate(time.time(), 'hello'))
