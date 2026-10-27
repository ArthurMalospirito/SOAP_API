import bcrypt


def hash_pw(password:str):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(pw_bytes,salt)
    return hash.decode('utf-8')

def verify_pw(password:str,hash_pw:str):
    pw_bytes = password.encode('utf-8')
    hash_bytes = hash_pw.encode('utf-8')
    verify = bcrypt.checkpw(pw_bytes,hash_bytes)
    return verify
