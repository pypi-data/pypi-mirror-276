class UnlimitedGetIps(object):
    def __init__(self, key, trade_no, num):
        self.key = key
        self.trade_no = trade_no
        self.num = num

    # 业务秘钥
    key = ""
    # 业务编号
    trade_no = ""
    # 提取数量
    num = ""
    # 代理类型
    pt = ""
    # 返回类型
    result_type = ""
    # 结果分隔符
    split = ""
    # 地区名称
    city_name = ""
    # 邮政编码
    city_code = ""
    # 剩余可用时长
    ip_remain = ""
