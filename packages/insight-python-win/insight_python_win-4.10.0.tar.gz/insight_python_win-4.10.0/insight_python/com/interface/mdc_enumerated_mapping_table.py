class EnumeratedMapping(object):

    @staticmethod
    def table_handle(table_list, table_dict):
        if table_list:
            result_dict = {}
            for i in table_list:
                if table_dict.get(i):
                    result_dict[i] = table_dict[i]
            return result_dict
        else:
            return table_dict

    @staticmethod
    def security_type_map(security_type_list):

        security_type_map = {
            'IndexType': 'index',
            'StockType': 'stock',
            'FundType': 'fund',
            'BondType': 'bond',
            'OptionType': 'option',
            'FuturesType': 'future',
            'SPFuturesType': 'spfuture',
            'WarrantType': 'warrant',
            'RateType': 'rate',
        }

        return EnumeratedMapping.table_handle(security_type_list, security_type_map)

    @staticmethod
    def security_type_num(security_type_list):

        security_type_num = {
            'index': 1,
            'stock': 2,
            'fund': 3,
            'bond': 4,
            'option': 7,
            'future': 8,
            'spfuture': 14,
            'warrant': 6,
            'rate': 10,
        }

        return EnumeratedMapping.table_handle(security_type_list, security_type_num)

    @staticmethod
    def exchange_num(exchange_list):

        exchange_num = {
            'XSHG': 101,  # 上交所
            'XSHE': 102,  # 深交所
            'XBSE': 106,  # 北交所
            'HKSC': 204,  # 港股通
            'CCFX': 301,  # 中金所
            'XSGE': 302,  # 上期所
            'XDCE': 601,  # 大商所
            'XZCE': 602,  # 郑商所
            'CNI': 702,  # 国证指数
            'CSI': 703,  # 中证指数
            'HTIS': 801,  # 华泰INSIGHT

            'XHKG': 203,  # 港交所
            'NASDAQ': 925,  # 纳斯达克
            'ICE': 915,  # 美国洲际交易所
            'CME': 916,  # 美国芝加哥商品交易所
            'CBOT': 917,  # 美国芝加哥商品交易所
            'COMEX': 923,  # 美国纽约商品交易所
            'NYMEX': 922,  # 美国纽约商品交易所
            'LME': 902,  # 英国伦敦金属交易所
            'SGX': 910,  # 新交所
            'LSE': 901,  # 伦交所

        }

        return EnumeratedMapping.table_handle(exchange_list, exchange_num)

    @staticmethod
    def exchange_suffix_map(exchange_list):

        exchange_suffix_map = {
            'XSHG': 'SH',
            'XSHE': 'SZ',
            'CSI': 'CSI',
            'CNI': 'CNI',
            'XBSE': 'BJ',
            'HKSC': 'HKSC',
            'CCFX': 'CF',
            'XSGE': 'SHF',
            'XDCE': 'DCE',
            'XZCE': 'ZCE',
            'HTIS': 'HT',

            'XHKG': 'HK',
            'NASDAQ': 'UW',
            'ICE': 'ICE',
            'CME': 'CME',
            'CBOT': 'CBT',
            'COMEX': 'CMX',
            'NYMEX': 'NYM',
            'LME': 'LME',
            'SGX': 'SG',
            'LSE': 'L',
        }

        return EnumeratedMapping.table_handle(exchange_list, exchange_suffix_map)

    @staticmethod
    def security_sub_type_map():

        return {'01001': '交易所指数', '01002': '亚洲指数', '01003': '国际指数', '01004': '系统分类指数',
                '01005': '用户分类指数', '01006': '期货指数', '01007': '指数现货', '01101': '申万一级行业指数',
                '01102': '申万二级行业指数', '01103': '申万三级行业指数', '01201': '自定义指数 - 概念股指数',
                '01202': '自定义指数 - 行业指数', '01203': '自定义指数 - 策略指数', '02001': 'A股（主板）',
                '02002': '中小板股', '02003': '创业板股', '02004': 'B股', '02005': '国际板',
                '02006': '战略新兴板', '02007': '新三板', '02008': '港股主板', '02009': '港股创业板',
                '02010': '香港上市NASD股票', '02011': '香港扩展板块股票', '02012': '美股',
                '02013': '美国存托凭证ADR', '02014': '英股', '02015': 'CDR（暂只包括CDR）',
                '02016': '两网公司及退市公司A股（股转系统）', '02017': '两网公司及退市公司B股（股转系统）', '02018': '股转系统挂牌公司股票',
                '02019': 'B转H股/H股全流通', '02020': '主板、中小板存托凭证', '02021': '创业板存托凭证', '02022': '北交所（精选层）',
                '02023': '股转系统基础层', '02024': '股转系统创新层', '02025': '股转系统特殊交易业务', '02100': '优先股',
                '02200': '科创板', '03001': '基金（封闭式）', '03002': '未上市开放基金（仅申赎）', '03003': '上市开放基金LOF',
                '03004': '交易型开放式指数基金ETF', '03005': '分级子基金', '03006': '扩展板块基金（港）',
                '03007': '仅申赎基金', '03008': '基础设施基金', '03009': '沪深基金通业务', '04001': '政府债券（国债）',
                '04002': '企业债券', '04003': '金融债券', '04004': '公司债', '04005': '可转债券', '04006': '私募债', '04007': '可交换私募债',
                '04008': '证券公司次级债', '04009': '证券公司短期债', '04010': '可交换公司债', '04011': '债券预发行',
                '04012': '固收平台特定债券', '04013': '定向可转债', '04020': '资产支持证券', '05001': '质押式国债回购',
                '05002': '质押式企债回购', '05003': '买断式债券回购', '05004': '报价回购', '05005': '质押式协议回购', '05006': '三方回购',
                '06001': '企业发行权证', '06002': '备兑权证', '06003': '牛证（moo-cow）',
                '06004': '熊证（bear）', '07001': '个股期权', '07002': 'ETF期权', '08001': '指数期货',
                '08002': '商品期货', '08003': '股票期货', '08004': '债券期货', '08005': '同业拆借利率期货',
                '08006': 'Exchange Fund Note Futures外汇基金票据期货', '08007': 'Exchange For Physicals期货转现货',
                '08009': 'Exchange of Futures For Swaps', '08010': '指数期货连线CX',
                '08011': '指数期货连线CC', '08012': '商品期货连线CX', '08013': '商品期货连线CC',
                '08014': '股票期货连线CX', '08015': '股票期货连线CC', '08016': '期现差价线', '08017': '跨期差价线',
                '08018': '外汇期货', '08019': '贵金属期货', '08100': '上海国际能源交易中心（INE）', '09000': '汇率',
                '10000': '利率', '11000': '贵金属', '12001': '国债（银行间市场TB）', '12002': '政策性金融债（银行间市场PFB）',
                '12003': '央行票据（银行间市场CBB）', '12004': '政府支持机构债券（银行间市场GBAB）', '12005': '短期融资券（银行间市场CP）',
                '12006': '中期票据（银行间市场MTN）', '12007': '企业债（银行间市场CORP）', '12008': '同业存单（银行间市场CD）',
                '12009': '超短期融资券（银行间市场SCP）', '12010': '资产支持证券（银行间市场ABS）',
                '12999': '其它（银行间市场Other）', '13002': '商品现货', '13018': '外汇现货', '13019': '贵金属期货',
                '99001': 'A股新股申购', '99002': 'A股增发', '99003': '新债申购', '99004': '新基金申购',
                '99005': '配股', '99006': '配债', '99010': '集合资产管理计划', '99020': '资产支持证券', '99030': '资金前端控制'}

    @staticmethod
    def trading_phase_code_map():

        return {'0': '开盘前，启动', '1': '开盘集合竞价', '2': '开盘集合竞价阶段结束到连续竞价阶段开始之前', '3': '连续竞价',
                '4': '中午休市', '5': '收盘集合竞价', '6': '已闭市', '7': '盘后交易', '8': '临时停牌', '9': '波动性中断',
                '10': '竞价交易收盘至盘后固定价格交易之前', '11': '盘后固定价格交易', '101': 'Halt in effect (Cross all U.S. equity exchanges)',
                '102': 'Paused across all U.S. equity markets / SROs (Nasdaq-listed securities only)',
                '103': 'Quote only period in effect (Cross all U.S. equity changes)',
                '104': 'Trading on Nasdaq marktet', '200': 'Undefined', '201': 'Normal', '202': 'Halted',
                '203': 'Suspended', '204': 'Opening Delay', '206': 'Closing Delay'}
