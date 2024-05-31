from .common.DynamicGetIps import DynamicGetIps
from .common.DynamicCheck import DynamicCheck
from .common.DynamicSetWhiteIp import DynamicSetWhiteIp
from .common.DynamicGetWhiteIp import DynamicGetWhiteIp
from .common.DynamicRemain import DynamicRemain
from .common.DynamicBalance import DynamicBalance
from .common.DynamicReplaceWhiteIp import DynamicReplaceWhiteIp
from .common.UsersGetBalance import UsersGetBalance
from .common.AloneGetIps import AloneGetIps
from .common.AloneSetWhiteIp import AloneSetWhiteIp
from .common.AloneGetWhiteIp import AloneGetWhiteIp
from .common.AloneReplaceWhiteIp import AloneReplaceWhiteIp
from .common.UsersGetAllOrders import UsersGetAllOrders
from .common.UsersGetCity import UsersGetCity
from .common.UnlimitedGetIps import UnlimitedGetIps
from .common.UnlimitedSetWhiteIp import UnlimitedSetWhiteIp
from .common.UnlimitedGetWhiteIp import UnlimitedGetWhiteIp
from .common.UnlimitedReplaceWhiteIp import UnlimitedReplaceWhiteIp
from .common.PostPayGetIps import PostPayGetIps
from .common.PostPayCheck import PostPayCheck
from .common.PostPaySetWhiteIp import PostPaySetWhiteIp
from .common.PostPayGetWhiteIp import PostPayGetWhiteIp
from .common.PostPayReplaceWhiteIp import PostPayReplaceWhiteIp
from .common.CompanyPostPayGetIps import CompanyPostPayGetIps
from .common.CompanyPostPaySetWhiteIp import CompanyPostPaySetWhiteIp
from .common.CompanyPostPayGetWhiteIp import CompanyPostPayGetWhiteIp
from .common.CompanyPostPayDelWhiteIp import CompanyPostPayDelWhiteIp
from .enums.URL import URL
from .ext.StrKit import get_params
import urllib.request
from urllib.parse import unquote


# 动态代理 --提取动态代理
def dynamic_get_ips(getips: DynamicGetIps) -> str:
    dic = getips.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.DYNAMIC_GETIPS.value + params)
    result = unquote(request.read(), "utf-8")
    return result


# 动态代理 -- 校验IP可用性
def dynamic_check(check: DynamicCheck) -> str:
    dic = check.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.DYNAMIC_CHECK.value + params)
    result = unquote(request.read(), "utf-8")
    return result


# 动态代理 -- 设置代理IP白名单
def dynamic_set_white_ip(ip: DynamicSetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.DYNAMIC_SETWHITEIP.value + params)
    result = unquote(request.read(), "utf-8")
    return result

# 动态代理 -- 替换IP白名单
def dynamic_replace_white_ip(ip: DynamicReplaceWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.DYNAMIC_REPLACEWHITEIP.value + params)
    result = unquote(request.read(), "utf-8")
    return result


# 动态代理 -- 获取IP白名单
def dynamic_get_white_ip(ip: DynamicGetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.DYNAMIC_GETWHITEIP.value + params)
    result = unquote(request.read(), "utf-8")
    return result


# 动态代理 -- 获取代理剩余可用时长
def dynamic_remain(remain: DynamicRemain) -> str:
    dic = remain.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.DYNAMIC_REMAIN.value + params)
    result = unquote(request.read(), "utf-8")
    return result


# 动态代理 -- 获取剩余可提取IP数量
def dynamic_balance(balance: DynamicBalance) -> str:
    dic = balance.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.DYNAMIC_BALANCE.value + params)
    result = unquote(request.read(), "utf-8")
    return result

#获取对应产品类型正常状态订单信息
def users_get_allOrders(allorders: UsersGetAllOrders) -> str:
    dic = allorders.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.USERS_GETALLORDERS.value + params)
    result = unquote(request.read(), "utf-8")
    return result

#获取所属省份可用代理城市信息
def user_get_city(cityRequest: UsersGetCity) -> str:
    dic = cityRequest.__dict__
    appKey = dic.get("key")
    params = get_params(dic, appKey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.USERS_GETCITY.value + params)
    result = unquote(request.read(), "utf-8")
    return result

# 获取账户余额
def users_get_balance(balance: UsersGetBalance) -> str:
    dic = balance.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.USERS_GETBALANCE.value + params)
    result = unquote(request.read(), "utf-8")
    return result


# 独享代理 -- 获取代理详情
def alone_get_ips(ips: AloneGetIps) -> str:
    dic = ips.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.ALONE_GETIPS.value + params)
    result = unquote(request.read(), "utf-8")
    return result

# 独享代理 -- 设置代理IP白名单
def alone_set_white_ip(ip: AloneSetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.ALONE_SETWHITEIP.value + params)
    result = unquote(request.read(), "utf-8")
    return result

# 独享代理 -- 替换IP白名单
def alone_replace_white_ip(ip: AloneReplaceWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.ALONE_REPLACEWHITEIP.value + params)
    result = unquote(request.read(), "utf-8")
    return result

# 独享代理 -- 获取代理IP白名单
def alone_get_white_ip(ip: AloneGetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.ALONE_GETWHITEIP.value + params)
    result = unquote(request.read(), "utf-8")
    return result

# 不限量 -- 获取ip
def unlimited_get_ips(ip: UnlimitedGetIps) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.UNLIMITED_GETIPS.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 不限量 -- 设置白名单
def unlimited_set_white_ip(ip: UnlimitedSetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.UNLIMITED_SETWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 不限量 -- 获取白名单
def unlimited_get_white_ip(ip: UnlimitedGetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.UNLIMITED_GETWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 不限量 -- 替换白名单
def unlimited_replace_white_ip(ip: UnlimitedReplaceWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic, appkey)
    params = urllib.parse.quote(params, "?/&=")
    request = urllib.request.urlopen(URL.UNLIMITED_REPLACEWHITEIP.value + params)
    result = unquote(request.read(), "utf-8")
    return result

# 按量付费 -- 提取ip
def postPay_get_ips(ip: PostPayGetIps) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.POSTPAY_GETIPS.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费 -- 检查代理有效性
def postPay_check(ip: PostPayCheck) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.POSTPAY_CHECK.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费 -- 设置白名单
def postPay_set_white_ip(ip: PostPaySetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.POSTPAY_SETWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费 -- 获取白名单
def postPay_get_white_ip(ip: PostPayGetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.POSTPAY_GETWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费 -- 替换白名单
def postPay_replace_white_ip(ip: PostPayReplaceWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.POSTPAY_REPLACEWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费(企业版) -- 提取ip
def company_postpay_get_ips(ip: CompanyPostPayGetIps) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.COMPANY_POSTPAY_GETIPS.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费 -- 设置白名单
def company_postpay_set_white_ip(ip:CompanyPostPaySetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.COMPANY_POSTPAY_SETWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费 -- 获取白名单
def company_postpay_get_white_ip(ip: CompanyPostPayGetWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.COMPANY_POSTPAY_GETWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result

# 按量付费 -- 获取白名单
def company_postpay_del_white_ip(ip: CompanyPostPayDelWhiteIp) -> str:
    dic = ip.__dict__
    appkey = dic.get("key")
    params = get_params(dic,appkey)
    params = urllib.parse.quote(params,"?/&=")
    request = urllib.request.urlopen(URL.COMPANY_POSTPAY_DELWHITEIP.value+params)
    result = unquote(request.read(),"utf-8")
    return result