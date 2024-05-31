from enum import Enum, unique


@unique
class URL(Enum):
    # 主站地址
    DOMAIN = "http://v2.api.juliangip.com"
    # DOMAIN = "http://192.168.10.63:8087"
    # 获取账户余额
    USERS_GETBALANCE = DOMAIN + "/users/getbalance"
    # 获取账户下对应类型的所有正常状态订单信息
    USERS_GETALLORDERS = DOMAIN + "/users/getAllOrders"
    # 获取所属省份可用代理城市信息
    USERS_GETCITY = DOMAIN + "/users/getCity"
    # 动态代理 - - 提取动态代理
    DYNAMIC_GETIPS = DOMAIN + "/dynamic/getips"
    # 动态代理 - - 校验IP可用性
    DYNAMIC_CHECK = DOMAIN + "/dynamic/check"
    # 动态代理 - - 设置代理IP白名单
    DYNAMIC_SETWHITEIP = DOMAIN + "/dynamic/setwhiteip"
    # 动态代理 - - 替换IP白名单
    DYNAMIC_REPLACEWHITEIP = DOMAIN + "/dynamic/replaceWhiteIp"
    # 动态代理 - - 获取IP白名单
    DYNAMIC_GETWHITEIP = DOMAIN + "/dynamic/getwhiteip"
    # 动态代理 - - 获取代理剩余可用时长
    DYNAMIC_REMAIN = DOMAIN + "/dynamic/remain"
    # 动态代理 - - 获取剩余可用时长
    DYNAMIC_BALANCE = DOMAIN + "/dynamic/balance"
    # 独享代理 - - 获取代理详情
    ALONE_GETIPS = DOMAIN + "/alone/getips"
    # 独享代理 - - 设置代理IP白名单
    ALONE_SETWHITEIP = DOMAIN + "/alone/setwhiteip"
    # 独享代理 - - 获取代理IP白名单
    ALONE_GETWHITEIP = DOMAIN + "/alone/getwhiteip"
    # 独享代理 -- 替换IP白名单
    ALONE_REPLACEWHITEIP = DOMAIN + "/alone/replaceWhiteIp"
    # 不限量 -- 获取Ip
    UNLIMITED_GETIPS = DOMAIN + "/unlimited/getips"
    # 不限量 -- 设置白名单
    UNLIMITED_SETWHITEIP = DOMAIN + "/unlimited/setwhiteip"
    # 不限量 -- 获取白名单
    UNLIMITED_GETWHITEIP = DOMAIN + "/unlimited/getwhiteip"
    # 不限量 -- 替换白名单
    UNLIMITED_REPLACEWHITEIP = DOMAIN + "/unlimited/replaceWhiteIp"
    # 按量付费 -- 提取ip
    POSTPAY_GETIPS = DOMAIN + "/postpay/getips"
    # 按量付费 -- 检查ip有效性
    POSTPAY_CHECK = DOMAIN + "/postpay/check"
    # 按量付费 -- 设置代理IP白名单
    POSTPAY_SETWHITEIP = DOMAIN + "/postpay/setwhiteip"
    # 按量付费 -- 获取代理IP白名单
    POSTPAY_GETWHITEIP = DOMAIN + "/postpay/getwhiteip"
    # 按量付费 -- 替换代理IP白名单
    POSTPAY_REPLACEWHITEIP = DOMAIN + "/postpay/replaceWhiteIp"

    # 按量付费(企业版) -- 提取IP
    COMPANY_POSTPAY_GETIPS = DOMAIN + "/company/postpay/getips"
    # 按量付费(企业版) -- 设置代理IP白名单
    COMPANY_POSTPAY_SETWHITEIP = DOMAIN + "/company/postpay/setwhiteip"
    # 按量付费(企业版) -- 获取代理IP白名单
    COMPANY_POSTPAY_GETWHITEIP = DOMAIN + "/company/postpay/getwhiteip"
    # 按量付费(企业版) -- 删除代理IP白名单
    COMPANY_POSTPAY_DELWHITEIP = DOMAIN + "/company/postpay/delwhiteip"