import base64
import json

from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]
def change_key(self, second_key ="af;ladfs"):
        return_key = [lambda x: char(10%(5*x)), second_key.split()]
        print(return_key)
        return ''.join(return_key)
    
class AESCipher:
    def __init__( self, second_key ):
        extras = ['$', '#', '@', '!', '%', '&', '^', '*', '9', ')']
        i = 0
        while len(second_key)%16 != 0:
            second_key += extras[i]
            i += 1
        self.key = second_key.encode()
        
    def format(self, _text, _encode: bool = True):
        if isinstance(_text, bytes):
            if _encode:
                return _text
            else:
                return _text.decode()
        else:
            return _text.encode()

    def encrypt( self, raw ):
        if isinstance(raw, dict):
            raw = json.dumps(raw)
            
        raw = self.format(pad(raw))
        iv = Random.new().read( AES.block_size )
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw )) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return self.format(unpad(cipher.decrypt( enc[16:] )), _encode = False)


if __name__ == "__main__":
    classCrypto = AESCipher('Marlins#12345678')
    encrypted_msg = classCrypto.encrypt("Hey there, unit cells are the best!")
    print(encrypted_msg)
    print(classCrypto.decrypt(encrypted_msg))




