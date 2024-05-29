import request.request as rq


# 获取token
def get_token(name, pwd):
    auth_json = {'account': name, 'pwd': pwd}
    token = rq.post_no_token("/capdata/auth", auth_json)
    rq.save_token(token)
    return token
