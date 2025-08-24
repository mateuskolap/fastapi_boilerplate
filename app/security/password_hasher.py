import bcrypt


def get_hashed_password(plain_password):
    plain_password = plain_password.encode('utf-8')
    hashed = bcrypt.hashpw(plain_password, bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(plain_password, hashed_password):
    plain_password = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed_password)
