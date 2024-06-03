from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto import Random

import json

def create_rsa_key_object(key_json: dict, public: bool = True):
    if public:
        return RSA.construct((key_json['n'], key_json['e']))
    else:
        return RSA.construct((key_json['n'], key_json['e'], key_json['d'], key_json['p'], key_json['q'], key_json['u']))
        
def verify_signature(rsa_cipher_object, message, signature, others_public_key_obj):
    return rsa_cipher_object.verify_signature(message, signature, others_public_key_obj) 
        
class RSA_Crypto:
    # keys: [pubKey, privKey]
    def __init__(self, keys: list = [], key_size: int = 3076):
        self.key_size = key_size
        
        if len(keys):
            self.pubKey = keys[0]
            self.privKey = keys[1]
            
            self.pubKey_obj = create_rsa_key_object(self.pubKey)
            self.privKey_obj = create_rsa_key_object(self.privKey, public = False)
        else:
            self.pubKey, self.privKey = self.new_keys()
            
            self.pubKey_obj = self.import_key(self.pubKey)
            self.privKey_obj = self.import_key(self.privKey)
            
    def new_keys(self):
        random_generator = Random.new().read
        key = RSA.generate(self.key_size, random_generator)
        private, public = key, key.publickey()
        return public, private
    
    # Convert to PKCS1_OAEP format
    def load_key(self, key):
        return PKCS1_OAEP.new(key)
        
    # Load from file
    def get_key_from_file(self, keyLoc):
        try:
            with open(keyLoc, "rb") as reader:
                return reader.read()
        except:
            return False
    
    # Load from memory      
    def import_key(self, extern_key):
        return RSA.importKey(extern_key.exportKey())
    
    # Encode into bytes
    def format(self, _text):
        if isinstance(_text, bytes):
            return _text
        elif isinstance(_text, dict):
            return json.dumps(_text).encode()
        else:
            return _text.encode()
            
    def encrypt(self, message, other_pubKey):
        other_pubKey_obj = self.import_key(other_pubKey)
        
        cipher = self.load_key(other_pubKey_obj)
        
        message = self.format(message)
        
        return cipher.encrypt(message)
        
    def decrypt(self, cipher_text):
        cipher = self.load_key(self.privKey_obj)
        
        return cipher.decrypt(cipher_text).decode()
        
    def sign_message(self, message):
        message = self.format(message)
        h = SHA256.new(message)
        key = self.privKey_obj
        
        signature = pkcs1_15.new(key).sign(h)
        
        return signature
        
    def verify_signature(self, message, signature, other_pubKey):
        message = self.format(message)
        h = SHA256.new(message)
        other_pubKey_obj = self.import_key(other_pubKey)

        try:
            pkcs1_15.new(other_pubKey_obj).verify(h, signature)
            return True
        except Exception as e:
            print(e)
            return False
    
    def extract_public_key(self):
        key = self.pubKey_obj
        n = key.n
        e = key.e
        
        return {"n": n, "e": e}
        
    def extract_private_key(self):
        key = self.privKey_obj
        n = key.n
        e = key.e
        d = key.d
        p = key.p
        q = key.q
        u = key.u
        
        return {"n": n, "e": e, "d": d, "p": p, "q": q, "u": u}
        
    def export_keys(self):
        return {"public_key": self.extract_public_key(), "private_key": self.extract_private_key()}
            
if __name__ == "__main__":
    rsa_obj = RSA_Crypto()
    print(f"pubKey {rsa_obj.pubKey}")
    print(f"PubKey {rsa_obj.pubKey_obj}")
    
    message = "attack at dawn"
    
    cipher_text = rsa_obj.encrypt(message, rsa_obj.pubKey)
    print(f"cipher_text: {cipher_text}")
    
    print(f"Decrypted: {rsa_obj.decrypt(cipher_text)}")
    
    data = {"username": "jarvis", "result": {"accept": True}}
    
    message = json.dumps(data)
    
    cipher_text = rsa_obj.encrypt(message, rsa_obj.pubKey)
    print(f"cipher_text: {cipher_text}")
    
    print(f"Decrypted: {rsa_obj.decrypt(cipher_text)}")
    
    data = rsa_obj.export_keys()
    
    pub = data["public_key"]
    priv = data["private_key"]
    
    print(pub)
    print(priv)
    
    rsa_obj = RSA_Crypto(keys = [pub, priv])
    print(f"pubKey {rsa_obj.pubKey}")
    print(f"PubKey {rsa_obj.pubKey_obj}")
    
    message = "attack at dawn"
    
    cipher_text = rsa_obj.encrypt(message, rsa_obj.pubKey_obj)
    print(f"cipher_text: {cipher_text}")
    
    print(f"Decrypted: {rsa_obj.decrypt(cipher_text)}")
    
    data = {"username": "jarvis", "result": {"accept": True}}
    
    message = json.dumps(data)
    
    cipher_text = rsa_obj.encrypt(message, rsa_obj.pubKey_obj)
    print(f"cipher_text: {cipher_text}")
    
    print(f"Decrypted: {rsa_obj.decrypt(cipher_text)}")
    
    data = rsa_obj.export_keys()
    
    signature = rsa_obj.sign_message(message)
    print(f"Signature {signature}")
    
    print(f"Verified: {rsa_obj.verify_signature(message, signature, rsa_obj.pubKey_obj)}")
    
