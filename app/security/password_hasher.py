import bcrypt


def get_hashed_password(plain_password):
    return bcrypt.hashpw(plain_password, bcrypt.gensalt())


def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password, hashed_password)
