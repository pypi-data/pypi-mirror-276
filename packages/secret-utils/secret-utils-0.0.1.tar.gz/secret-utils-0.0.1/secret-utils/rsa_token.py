import json

from datetime import datetime

from .aes import AESCipher
from .rsa_crypto import RSA_Crypto, create_rsa_key_object
        
class RSA_Token_Encryption:
    def __init__(self, rsa_key_pair: dict, others_public_key: str, aes_key: str, auth_server_code: int, time_of_use_seconds: int, uuid: str = "", hardward_id: str = "", ip_address: str = ""):
        ## Log uuid, aes_key, hardware_id, ip_address
        
        #pub = create_rsa_key_object(rsa_key_pair["public_key"])
        #priv = create_rsa_key_object(rsa_key_pair["private_key"])
        self.rsa_cipher = RSA_Crypto(keys = [rsa_key_pair["public_key"], rsa_key_pair["private_key"]])
        
        self.token = {"data": {"code": auth_server_code, "aes_key": aes_key, "time_of_use_seconds": time_of_use_seconds, "timestamp": datetime.now().strftime("%m-%d-%y %H:%M:%S")}}
        
        self.others_public_key_obj = create_rsa_key_object(others_public_key)
        
    def sign_token(self):        
        self.token["signature"] = self.rsa_cipher.sign_message(self.token["data"])
        
    # Split this from instantiation in case in task group
    def encrypt_token(self):
        if "signature" not in self.token.keys():
            self.sign_token()
        
        message = json.dumps(self.token["data"])
        self.token["data"] = self.rsa_cipher.encrypt(message, self.others_public_key_obj)
        
        return self.token
        #encrypted_info = self.rsa_cipher.encrypt(message, self.others_public_key_obj)
        #token = {"data": encrypted_info, "signature": self.token["signature"]}
        
        #return token
        
class RSA_Token_Decryption:
    def __init__(self, rsa_key_pair: dict, others_public_key: str, encrypted_token: str, uuid: str = ""):
        # log message uuid, others_public_key
        
        self.pub = rsa_key_pair["public_key"]
        self.priv = rsa_key_pair["private_key"]
        self.rsa_cipher = RSA_Crypto(keys = [self.pub, self.priv])
        
        self.token = encrypted_token
        self.others_public_key_obj = create_rsa_key_object(others_public_key)
        self.uuid = uuid
        
    # Split due to task group
    def decrypt_token(self):
        self.token["data"] = json.loads(self.rsa_cipher.decrypt(self.token["data"]))
        
    # Split due to task group
    def verify_token(self):
        data = json.dumps(self.token["data"])

        return self.rsa_cipher.verify_signature(data, self.token["signature"], self.others_public_key_obj) 

    def all_in_one(self):
        self.decrypt_token()
        result = self.verify_token()

        if self.verify_token():
            return self.token["data"]
        else:
            return False
            
if __name__ == "__main__":
        rsa_obj_1 = RSA_Crypto()
        rsa_obj_2 = RSA_Crypto()
        
        key_pair_1 = rsa_obj_1.export_keys()
        key_pair_2 = rsa_obj_1.export_keys()
        
        print(f"{key_pair_1} {key_pair_2}")
        
        rsa_token_1 = RSA_Token_Encryption(key_pair_1, key_pair_2["public_key"], "Marlins#12345", 111, 86400)
        
        encrypted_token = rsa_token_1.encrypt_token()
        rsa_token_2 = RSA_Token_Decryption(key_pair_1, key_pair_2["public_key"], encrypted_token)
        
        print(rsa_token_2.all_in_one())
        
