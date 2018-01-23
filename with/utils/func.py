#coding:utf-8
import random
# 盐值
def getsalt(length=6):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    return "".join(map(lambda i: chars[random.randint(0, len_chars)], range(length)))


def rank_name(length=6):
    chars = '0123456789'
    len_chars = len(chars) - 1
    return "用户" + "".join(map(lambda i: chars[random.randint(0, len_chars)], range(length)))


if __name__ == '__main__':
    print(rank_name(6))