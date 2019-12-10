import time
import base64
import hmac
import redis
import datetime

def generate_token(user_id, expire=5):
    """
    生成token
    :param user_id:用户名id
    :param expire:Token过期时间，单位为秒，预设为12小时:43200s
    :return:token
    """
    user_id_byte = user_id.encode("utf8")
    salt_str = 'ProjectManagement'
    salt_byte = salt_str.encode("utf-8")
    times_str = str(time.time() + expire)
    times_salt_byte = times_str.encode("utf-8") + salt_byte
    sha256_hashcode = hmac.new(user_id_byte, times_salt_byte, 'sha256').hexdigest()
    token_str = user_id + ":" + ":" + times_str + ':' + sha256_hashcode
    b64_token = base64.urlsafe_b64encode(token_str.encode("utf-8"))
    return b64_token.decode("utf-8")


def certify_token(token):
    """
    验证token自身正确性以及是否过期
    :param token:需要验证的token
    :return:token正确且未过期返回True，否则返False
    """
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    # 验证token格式：user_id + 时间戳 + hash码
    if len(token_list) != 4:
        return False
    user_id = token_list[0]
    time_str = token_list[1]
    user_id_byte = user_id.encode("utf-8")

    salt_str = 'ProjectManagement'
    salt_byte = salt_str.encode("utf-8")
    time_salt_byte = time_str.encode('utf-8') + salt_byte
    # 验证是否过期
    if float(time_str) < time.time():
        return False
    need_verify_sha256_hashcode = token_list[3]
    sha256_hashcode = hmac.new(user_id_byte, time_salt_byte, 'sha256').hexdigest()
    if need_verify_sha256_hashcode != sha256_hashcode:
        # token无效
        return False
    else:
        # token有效
        return True


def get_user_id_from_token(token):
    """
    从token中获取用户id
    :param token:
    :return:
    """
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) == 3:
        return token_list[0]
    else:
        return ""


def get_expire_time(token):
    """
    从token获取过期时间
    :param token:
    :return:
    """
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) == 4:
        return token_list[1]
    else:
        return ""


def get_redis_Connection():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
    red = redis.Redis(connection_pool=pool)
    return red


def certify_user_in_Redis(token):
    """
    验证该token是否在登录白名单中
    :param token:
    :return:
    """
    red = get_redis_Connection()
    user_id = get_user_id_from_token(token)
    value = red.get(user_id)
    if value is None:
        return False
    elif value == token:
        return True
    else:
        return False


user_id = "yangliyao"
group_id = "0"
token = generate_token(user_id)
redis_connection = get_redis_Connection()
redis_connection.set("a", "a")
while True:

    a = redis_connection.get("a")
# a = redis_connection.get("1234512321")
# if a is None:
#     print("a is none")
# print(a)
#
# print(get_group_id_from_token(token))
