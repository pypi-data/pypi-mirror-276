import bcrypt
import hashlib

def get_new_salt() -> bytes:
    return bcrypt.gensalt()
    
def hash_passwd(passwd: str, salt: bytes, encoding: str = 'utf-8') -> bytes:
    return bcrypt.hashpw(passwd.encode(encoding), salt)
    
def check_passwd(passwd: str, _hash: bytes, encoding: str = 'utf-8') -> bool:
    return bcrypt.checkpw(passwd.encode(encoding), _hash)
    
class Hasher:
    regexes = {'SHA-256': hashlib.sha256, 'SHA-512': hashlib.sha512}
    
    @staticmethod
    def start_hash(algorithm: str):
        match algorithm:
            case 'SHA-256':
                return hashlib.new('sha256')
            case _:
                return hashlib.new('sha512')
        
    # Could fix the data to use Codecs with DDP transitions!!!
    @classmethod
    def hash_data(cls, option: str, info: str, algorithm: str = 'SHA-512') -> str:
        match option:
            case 'data':
                _hash = start_hash(algorithm)
                _hash.update(info.encode())
                
                return _hash.hexdigest()
            case _: # File hashing
                if errorMsg == "":
                    errorMsg = f"{info} did not convert"
                
                try:
                    with open(info, 'rb') as f:
                        sha = hashlib.sha256()
                        buf = f.read()
                        sha.update(buf)
                        return sha.hexdigest()
                except:
                    return errorMsg
