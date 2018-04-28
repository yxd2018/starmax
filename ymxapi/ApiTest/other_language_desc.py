#!/usr/bin/env python
# -*- coding:utf-8 -*-
#制作:温赫男

'''
其他语种的描述信息
'''
from django.db.models import Q

from sysproduct.models import SpuDescriptionLanguage
from pro_db_models.models.market_channel_models import SysMarketProductMap
from order_statistic.models import SkuDaysStatistic,SkuStatistic
from sale_amazon.models import Amazonstore, Amazonsummary, AmazonCharger, AmazonAccount, amazonasintrack
from maindefine import COUNTRY
#from django.db import models
import datetime
from utils import misc
from sysproduct.platform_info import *
from django.db.models import Count, Avg, Max, Min, Sum
import enum
from sysproduct.models import *
from warehouse.models import Warehouse,SkuWarehouseInventory
import pytz
from utils import misc
import bottlenose
# import logging
# bottlenose.api.log.level = logging.DEBUG
#
# handle = logging.StreamHandler()
# handle.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter(
#     '%(asctime)s - %(funcName)s - %(lineno)d- %(message)s')
# handle.setFormatter(formatter)
#
# if not  bottlenose.api.log.handlers:
#     bottlenose.api.log.addHandler(handle)


from django.db import models
from sale_amazon.models.listing import *
from amazon.api import AmazonAPI
from sale_amazon.models import Amazonstore, amazonbrand
from utils import misc
class _Report_Info(str):
    c_Code = 0
    def __new__(cls,msg):
        cls.c_Code +=1
        codeid = cls.c_Code
        self = str.__new__(cls, codeid)
        self.m_CodeID = codeid
        self.m_Msg = msg


        self.m_Num = 0
        self.m_Data = {}
        return self

    @property
    def num(self):
        return self.m_Num

    @num.setter
    def num(self, value):
        self.m_Num = value

    @property
    def data(self):
        return self.m_Data

    # 保存报告
    # 库存总sku数
    # 可上架的sku数
    # 共保存asin数量
    # 描述为空数量
    # 文字少于30个字符数量
    # 全英文描述数量
    # 合并后spu数量
    #
    # 日本站：
    # 描述中不包含日文描述数量
    # 需要翻译的数量
class REPORTINFO(_Report_Info,enum.Enum):
    ALL_SYS_SKU = "系统全部spu数量."
    All_SKU_REDUCE_NOSTOCK = "去掉没库存并且非采购状态的spu后的剩余数量"
    All_SKU_REDUCE_NOSALE =  "去掉销量为0的spu后的剩余数量"

    #ALL_ASINS =  "系统的总asin数量"
    #ALL_ASINS_CANPUSH = "可上架状态的asin数量"
    ASIN_DOWN = "抓取到的asin总数"
    ALL_SPU = "需要导入的SPU总数"
    ALL_SPU_DOWN = "下载到的SPU总数"
    ALL_SPU_REDUCE_NO_DESC = "去掉描述为空的spu后剩余数量"
    DESCLEN_LT30 = "描述长度少于30的spu"

    SPU_INSERT = "插入SPU"
    SPU_UPDATE = "更新SPU"


    US_SPU_COUNT = "美国站spu总量"
    US_SPU_REDUCE_NOSTOCK = "去掉没库存并且非采购状态的spu剩余数量"
    US_SPU_REDUCE_DOWN = "去掉已经下载的数据"
    US_SPU_NO_EN_DESC = "有英文描述的剩余"
    US_SPU_ERR_TRANS = "翻译失败个数"

    TITLE_LENS = "标题长度"
    FETURE_LENS = "短描总长度"
    DESC_LENS = "描述正文总长度"

    HASTRANSD_TIME = "重复翻译"

    AMA_PRODUCTS_PUSHED = "已经有映射的asin数(%s),sku数(%s),spu数(%s)"
    AMA_PRODUCTS_DOWNED = "过滤掉拿不到asin的asin数(%s),sku数(%s),spu数(%s)"
    AMA_PRODUCTS_REDUCE = "过滤掉描述长度<30的asin数(%s),sku数(%s),spu数(%s)"
    AMA_PRODUCTS_SAVED = "抓取信息导入系统的spu数"

    ALL_PRODUCTS = "系统全部spu数量"

    SALED_PRODUCTS = "减去系统没有的销量的产品"
    SALED_PRODUCTS_NOTUSED = "减去日本站已存在的SPU"
    SALED_PRODUCTS_DESCGT30 = "减去描述长度小于30的SPU"
    SALED_PRODUCTS_TRAN_TIME = "需要翻译的spu数"
    SALED_PRODUCTS_TRAN_COUNT = "需要翻译的字符数"

    HASSTOCK_PRODUCTS = "减去系统没有库存的SPU"
    HASSTOCK_PRODUCTS_NOTUSED = "减去日本站已存在的SPU"
    HASSTOCK_PRODUCTS_DESCGT30 = "减去描述长度小于30的SPU"
    HASSTOCK_PRODUCTS_TRAN_TIME = "需要翻译的spu数"
    HASSTOCK_PRODUCTS_TRAN_COUNT = "需要翻译的字符数"


    PUSHABLE_PRODUCTS = "减去系统没有库存的SPU"
    PUSHABLE_PRODUCTS_NOSALE = "减去没销量的,剩余spu"

    PUSHABLE_PRODUCTS_NOTUSED = "减去日本站已存在的SPU"
    PUSHABLE_PRODUCTS_DESCGT30 = "减去描述长度小于30的SPU"
    PUSHABLE_PRODUCTS_TRAN_TIME = "需要翻译的spu数"
    PUSHABLE_PRODUCTS_TRAN_COUNT = "需要翻译的字符数"
# 1 已经有映射的asin数，sku数，spu数
# 2 过滤掉拿不到asin数，sku数，spu数
# 3 过滤掉描述长度<30 asin数，sku数，spu数
# 4 抓取信息导入系统的spu数
# 5 系统有库存有销量的产品spu数
# 6 需要翻译的spu数：
# 7 需要翻译的字符数：
# 8 系统可上架的产品spu数：
# 9 需要翻译的spu数
# 10 需要翻译的字符数
    @classmethod
    def NewReport(cls):
        alldata = []
        # items = [
        #     cls.AMA_PRODUCTS_PUSHED,
        #     cls.AMA_PRODUCTS_DOWNED,
        #     cls.AMA_PRODUCTS_REDUCE,
        # ]
        # keys = [
        #     "asin",
        #     "sku",
        #     "spu",
        #
        # ]

        # for item in items:
        #     info = item.m_Msg%(item.data["asin"],item.data["sku"],item.data["spu"])
        #     alldata.append(info)
        #     #cls.AMA_PRODUCTS_REDUCE,
        # #alldata.append(cls.AMA_PRODUCTS_REDUCE.GetValue())
        # alldata.append(cls.AMA_PRODUCTS_SAVED.GetValue())
        # alldata.append("-------------")
        #
        #
        # items = [
        #     cls.ALL_PRODUCTS,
        #     cls.SALED_PRODUCTS,
        #     cls.SALED_PRODUCTS_NOTUSED,
        #     cls.SALED_PRODUCTS_DESCGT30,
        #     cls.SALED_PRODUCTS_TRAN_TIME,
        #     cls.SALED_PRODUCTS_TRAN_COUNT,
        #
        # ]
        # for item in items:
        #     print id(item),3132123,item.num
        #     alldata.append(item.GetValue())
        #
        # alldata.append("-------------")
        #
        #
        # items = [
        #     cls.ALL_PRODUCTS,
        #     cls.HASSTOCK_PRODUCTS,
        #     cls.HASSTOCK_PRODUCTS_NOSALE,
        #     # cls.SALED_PRODUCTS_NOSTOCK,
        #     cls.HASSTOCK_PRODUCTS_DESCGT30,
        #     cls.HASSTOCK_PRODUCTS_TRAN_TIME,
        #     cls.HASSTOCK_PRODUCTS_TRAN_COUNT,
        # ]
        # for item in items:
        #     alldata.append(item.GetValue())
        #
        # alldata.append("-------------")


        items = [
            cls.ALL_PRODUCTS,
            cls.PUSHABLE_PRODUCTS,
            cls.PUSHABLE_PRODUCTS_NOSALE,
            cls.PUSHABLE_PRODUCTS_NOTUSED,
            # cls.SALED_PRODUCTS_NOSTOCK,
            cls.PUSHABLE_PRODUCTS_DESCGT30,
            cls.PUSHABLE_PRODUCTS_TRAN_TIME,
            cls.PUSHABLE_PRODUCTS_TRAN_COUNT,
        ]
        for item in items:
            alldata.append(item.GetValue())

    #    alldata.append("-------------")

        return alldata

    @classmethod
    def Clear(cls):
        for info in cls.GetItems():
            info.num=0
            info.data.clear()
#            print info

    @classmethod
    def GetItems(cls):
        return [
        cls.ALL_SYS_SKU,
        cls.All_SKU_REDUCE_NOSTOCK,
        #cls.All_SKU_REDUCE_NOSALE,


        #cls.ASIN_DOWN,
        cls.ALL_SPU_DOWN,
        #cls.ALL_SPU_REDUCE_NO_DESC,
        cls.DESCLEN_LT30,

        cls.SPU_INSERT,
        cls.SPU_UPDATE,
        ]

    @classmethod
    def DoReport1(cls):
        lans = ["jp", ]
        items = [
            cls.US_SPU_COUNT,
            cls.US_SPU_REDUCE_NOSTOCK,
            cls.US_SPU_REDUCE_DOWN,
            cls.US_SPU_NO_EN_DESC,
            #cls.US_SPU_ERR_TRANS,

            cls.TITLE_LENS ,
            cls.FETURE_LENS ,
            cls.DESC_LENS ,

            #cls.HASTRANSD_TIME ,


            # cls.SPU_INSERT,
            # cls.SPU_UPDATE,
        ]

        #lans = ["es",]
        # for info in items:
        #     info.num = sum(info.data.values())
        #
        data = []
        # for info in items:
        #     data.append(info.GetValue())
        # data.append("----------------")
        for lan in lans:
            for info in items:
                data.append(info.GetValue(lan))
            data.append("----------------")

        data.append(REPORTINFO.HASTRANSD_TIME.GetValue("次数"))
        data.append(REPORTINFO.HASTRANSD_COUNT.GetValue("字符"))

        return data

    @classmethod
    def DoReport(cls):
        lans = ["de", "jp", "es", "it", "fr"]
        #lans = ["es",]
        for info in cls.GetItems():
            info.num = sum(info.data.values())

        data = []
        for info in cls.GetItems():
            data.append(info.GetValue())
        data.append("----------------")
        for lan in lans:
            for info in cls.GetItems():
               data.append(info.GetValue(lan))
            data.append("----------------")
        return data
            #data.append()

    def __str__(self):
        return self.GetValue()

    def GetValue(self,lan=""):

        if lan=="all":
            alldata = []
            for key,value in self.m_Data.items():
                alldata.append("%s<%s>:%s"%(self.m_Msg,key,value))
            return "\n".join(alldata)
        elif lan:
            return  "%s<%s>:%s"%(self.m_Msg,lan,self.m_Data.get(lan,""))
        else:
            return "%s:%s"%(self.m_Msg,self.m_Num)

def GetMarketID(lan):
    dn = {
        "de": 8,
        "jp": 5,
        "es": 10,
        "it": 11,
        "fr": 12,
        "us": 2,
    }

    market_id = dn.get(lan,"")
    return market_id

# class CReport(object):
#     def __init__(self):
#         self.m_All_Sys_Sku_Count = 0#库存总sku数
#         self.m_All_Sys_Sku_Count_Reduce_NoSale = 0# 销量为0的sku
#         self.m_All_Sys_Sku_Count_Reduce_NoStock = 0#有库存sku或可采购
#         self.m_All_Asin_Count = 0

class CSysAsin(SysMarketProductMap):
    # market_product = models.ForeignKey(MarketProductsCandidates,null=True,db_column='market_product_id',db_constraint=False,on_delete=models.DO_NOTHING, help_text='市场产品id')
    # item_id = models.CharField(max_length=50,null=True,db_index=True,help_text='各个平台的产品编码')
    # sku = models.ForeignKey(SkuProduct,db_column='sku_id' ,related_name="sku_product_map",null=True, help_text='对应的sku产品')
    # market = models.ForeignKey(Market, related_name="market_map",null=True)
    # # 产品映射加入系统信息
    # create_time = models.DateTimeField(default=timezone.now)
    # create_user = models.ForeignKey(settings.AUTH_USER_MODEL,db_constraint=False, null=True, related_name='product_map_create_user')
    # update_time = models.DateTimeField(default=timezone.now)
    # update_user = models.ForeignKey(settings.AUTH_USER_MODEL,db_constraint=False, null=True, related_name='product_map_update_user')
    # default_map = models.BooleanField(default=False,help_text='以第一次添加的为默认映射关系,主要针对同一市场,一个sku有多个映射的情况')
    class Meta:
        proxy = True

    @classmethod
    def Bluk_Set_Category(cls):
        misc.CLog.Clear()
        with open('amazon_us.csv', 'r') as f:
            alldata = f.read().splitlines()
            misc.CLog.SetSpace(100,len(alldata)-1)
            for relationstr in alldata[1:]:
                data = relationstr.split(",")
                misc.CLog.PrintSpace("写入品类")
                try:
                    asin,category_id = data
                except:
                    #print data,22222
                    continue
                info = cls.objects.filter(item_id=asin).filter(market=2).first()
                if info:
                    info.category_id = category_id
                    info.save()

    @classmethod
    def Bluk_Set_Pro_Category(cls):
        class _tmp_table(models.Model):
            id = models.AutoField(primary_key=True)
            category_id = models.CharField(max_length=20)
            asin = models.CharField(max_length=20)

            class Meta:
                managed = False
                db_table = 'channel_product_map_forupdate'


        def _create_tmp():
            from django.db import connection, transaction
            cursor = connection.cursor()

            sql = """
            DROP TABLE IF EXISTS `channel_product_map_forupdate`;
            CREATE TABLE `channel_product_map_forupdate` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `asin` varchar(16) DEFAULT NULL DEFAULT '',
              `category_id` varchar(16) NOT NULL DEFAULT '',
              PRIMARY KEY (`id`),
              KEY `channel_product_map_category_id` (`category_id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
            """
            #
            cursor.execute(sql)

        def _drop_tmp():
            from django.db import connection, transaction
            cursor = connection.cursor()
            sql = """
            DROP TABLE `channel_product_map_forupdate`;
            """
            cursor.execute(sql)

        def _update_relation():
            from django.db import connection, transaction
            cursor = connection.cursor()
            sql = """
            update channel_product_map_forupdate s,channel_product_map t set t.category_id = s.category_id  where s.asin = t.item_id  and t.market_id = 2;
            """
            cursor.execute(sql)



        _create_tmp()

        alldata1 = []
        misc.CLog.Clear()
        with open('upload/amazon/amazon_us.csv', 'r') as f:
            alldata = f.read().splitlines()
            misc.CLog.SetSpace(10000,len(alldata)-1)
            for relationstr in alldata[1:]:
                data = relationstr.split(",")
                misc.CLog.PrintSpace("读入品类信息")
                try:
                    asin,category_id = data
                except:
                    #print data,22222
                    continue
                info = _tmp_table()
                info.asin = asin
                info.category_id = category_id
                #print info.asin,info.category_id
                alldata1.append(info)
        misc.CLog.Print("开始写入")
        _tmp_table.objects.bulk_create(alldata1)
        misc.CLog.Print("写入完毕")
        _update_relation()
        misc.CLog.Print("更新关系")
        _drop_tmp()
        misc.CLog.Print("清理临时表")




    @classmethod
    def GetAsinList(cls,lan):
        oQuery = cls.GetAsinListQuery(lan)
        alldata = []
        for data in oQuery.all().values("item_id"):
            alldata.append(data["item_id"])

        return alldata

    @classmethod
    def GetAsinListQuery(cls,lan):
        market_id = GetMarketID(lan)
        oQuery = cls.objects.filter(market=market_id)

        ct = cls._GetSpuCount(oQuery.values("sku_id"))
        REPORTINFO.ALL_SYS_SKU.data[lan] = ct

        hasstore_products = SkuWarehouseInventory.objects.values("sku_id").annotate(allct=Sum('on_hand_qty')).filter(
                allct__gt=1).values("sku_id")
        query_select = Q(purchase_ok=1) | Q(id__in=hasstore_products)
        allproducts = SkuProduct.objects.filter(query_select).values("id")
        oQuery = oQuery.filter(sku__in=allproducts)

        ct = cls._GetSpuCount(oQuery.values("sku_id"))
        REPORTINFO.All_SKU_REDUCE_NOSTOCK.data[lan] = ct
        #REPORTINFO.All_SKU_REDUCE_NOSTOCK.data[lan]=oQuery.count()

        #SaledProducts = SkuDaysStatistic.objects.values("sku").filter(total_qty__gt=0).values("sku")
        return oQuery

    @classmethod
    def _GetSpuCount(cls,sku_list):
        ct = SkuProduct.objects.filter(id__in=sku_list).values("spu_id").distinct().count()
        return ct

    # @classmethod
    # def GetSpuList_ExtDone(cls,lan):
    #
    #     market_id = GetMarketID("us")
    #     oQuery = cls.objects.filter(market=market_id)
    #     ct = cls._GetSpuCount(oQuery.values("sku_id"))
    #     REPORTINFO.US_SPU_COUNT.data[lan] = ct
    #
    #     hasstore_products = SkuWarehouseInventory.objects.values("sku_id").annotate(allct=Sum('on_hand_qty')).filter(
    #             allct__gt=1).values("sku_id")
    #     query_select = Q(purchase_ok=1) | Q(id__in=hasstore_products)
    #     allproducts = SkuProduct.objects.filter(query_select).values("id")
    #     oQuery = oQuery.filter(sku__in=allproducts)
    #
    #     ct = cls._GetSpuCount(oQuery.values("sku_id"))
    #     REPORTINFO.US_SPU_REDUCE_NOSTOCK.data[lan] = ct
    #
    #     # all_spu_list = SkuProduct.objects
    #     # all_spu_list = all_spu_list.filter(id__in=oQuery.values("sku_id"))
    #
    #     done_spu_list = CSpuDesc.GetDoned_Spu_List(lan)
    #     all_sku_list = SkuProduct.objects.exclude(spu__in=done_spu_list).values("id")
    #     oQuery = oQuery.filter(sku__in=all_sku_list)
    #
    #     ct = cls._GetSpuCount(oQuery.values("sku_id"))
    #     REPORTINFO.US_SPU_REDUCE_DOWN.data[lan] = ct
    #     #print oQuery.query
    #     #print "--------"
    #     #print SkuProduct.objects.exclude(id__in=oQuery.values_list("sku",flat=True)).values_list("spu",flat=True).distinct().query
    #     return SkuProduct.objects.filter(id__in=oQuery.values_list("sku",flat=True)).values_list("spu",flat=True).distinct()

    @classmethod
    def GetSpuList_ExtDone(cls,lan):

        # market_id = GetMarketID("us")
        # oQuery = cls.objects.filter(market=market_id)
        oQuery = SkuProduct.objects.filter()

        ct = cls._GetSpuCount(oQuery.values("id"))
        REPORTINFO.US_SPU_COUNT.data[lan] = ct

        hasstore_products = SkuWarehouseInventory.objects.values("sku_id").annotate(allct=Sum('on_hand_qty')).filter(
                allct__gt=1).values("sku_id")
        query_select = Q(purchase_ok=1) | Q(id__in=hasstore_products)
        allproducts = SkuProduct.objects.filter(query_select).values("id")
        oQuery = oQuery.filter(id__in=allproducts)

        ct = cls._GetSpuCount(oQuery.values("id"))
        REPORTINFO.US_SPU_REDUCE_NOSTOCK.data[lan] = ct

        # all_spu_list = SkuProduct.objects
        # all_spu_list = all_spu_list.filter(id__in=oQuery.values("sku_id"))

        done_spu_list = CSpuDesc.GetDoned_Spu_List(lan)
        all_sku_list = SkuProduct.objects.exclude(spu__in=done_spu_list).values("id")
        oQuery = oQuery.filter(id__in=all_sku_list)

        ct = cls._GetSpuCount(oQuery.values("id"))
        REPORTINFO.US_SPU_REDUCE_DOWN.data[lan] = ct
        #print oQuery.query
        #print "--------"
        #print SkuProduct.objects.exclude(id__in=oQuery.values_list("sku",flat=True)).values_list("spu",flat=True).distinct().query
        return SkuProduct.objects.filter(id__in=oQuery.values_list("id",flat=True)).values_list("spu",flat=True).distinct()


class CSpuDesc(SpuDescriptionLanguage):
    #
    # spu_id = models.IntegerField()
    # language = models.SmallIntegerField()
    # description = models.TextField()
    # feature = models.TextField()
    # attr_detail = models.TextField()
    # product_list = models.CharField(max_length=300)
    # create_time = models.DateTimeField()
    # write_time = models.DateTimeField()
    # version = models.IntegerField()
    # source  = models.IntegerField()
    class Meta:
        proxy = True

    @classmethod
    def DoSave(cls):
        pass

    @classmethod
    def GetDoned_Spu_List(cls,lan):
        oQuery = cls.objects.filter(language=lan)
        #oQuery = oQuery.filter(source=SOURCE.AMAZON_INFO)
        return oQuery.values("spu_id")


    @classmethod
    def Bluk_Add(cls,alldata,lan,source):
        REPORTINFO.SPU_INSERT.data[lan] = 0
        REPORTINFO.SPU_UPDATE.data[lan] = 0

        for data in alldata:
            oQuery = cls.objects.filter(spu_id=data["spu_id"]).filter(language=lan)
            #print oQuery.query
            info = oQuery.first()
            if not info:
                info = cls()
                info.create_time = datetime.utcnow().replace(tzinfo=pytz.utc)
                info.spu_id = data["spu_id"]
                info.language = lan
                REPORTINFO.SPU_INSERT.data[lan] += 1
            else:
                REPORTINFO.SPU_UPDATE.data[lan]+=1
                continue#只插入不更新
            info.spu_id = data["spu_id"]
            info.write_time = datetime.utcnow().replace(tzinfo=pytz.utc)
            #if not info.version:
            #    info.version = 0
            info.version = 1
            info.title = data["title"]
            info.source = source
            info.feature = data["feature"]
            info.description = data["description"]
            info.save()






class SOURCE(object):
    AMAZON_INFO = 0 #亚马逊小语种站点
    AMAZON_US_INFO_TRANS = 1 #亚马逊美国站自动翻译信息
    LISTING = 2 #listing数据抓取

# def LoadAmazon_Info_Path(path):
#     import os
#     '''
#     便历目录
#     :param path:
#     :return:
#     '''
#     source = SOURCE.AMAZON_INFO
#     rootpath = "mount/amazon_info"
#     for filename in os.listdir(rootpath):
#         alldata = []



def DownProductInfo():
    '''
    下载一个产品
    :return: 
    '''


g_Asin2Spu_Cache = {}
def Asin2Spu(asin):
    global g_Asin2Spu_Cache
    '''
    asin转spu
    :param asin: 
    :return: 
    '''

    if asin in g_Asin2Spu_Cache:
        return g_Asin2Spu_Cache[asin]
    info = CSysAsin.objects.filter(item_id=asin).values("sku_id").first()
    spu_id = None

    if info:
        sku_id = info["sku_id"]
        info = SkuProduct.objects.filter(id=sku_id).values("spu_id").first()
        if info:
            spu_id = info["spu_id"]
    g_Asin2Spu_Cache[asin]=spu_id
    return spu_id

g_Asin2SpuSku_Cache = {}
def Asin2SpuSku(asin):
    global g_Asin2Spu_Cache
    if asin in g_Asin2SpuSku_Cache:
        return g_Asin2SpuSku_Cache[asin]
    info = CSysAsin.objects.filter(item_id=asin).values("sku_id").first()
    spu_id = None
    sku_id = None
    if info:
        sku_id = info["sku_id"]
        info = SkuProduct.objects.filter(id=sku_id).values("spu_id").first()
        if info:
            spu_id = info["spu_id"]
    g_Asin2SpuSku_Cache[asin]=spu_id,sku_id
    return spu_id,sku_id

def ImportXls(filename):
    '''
    引入一个数据文件
    :param filename: 
    :return: 
    '''
    alldata = []
    import xlrd
    bk = xlrd.open_workbook(filename)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        return [],"文件找不到<Sheet1>分页"
    # 获取行数
    nrows = sh.nrows
    # 获取列数
    ncols = sh.ncols
    print "nrows %d, ncols %d" % (nrows, ncols)
    # 获取第一行第一列数据
    cell_value = sh.cell_value(1, 1)
    row_list = []
    # 获取各行数据
    for row in range(1, nrows):
        row_data = sh.row_values(row)
        row_list.append(row_data)
    return row_list

class _CTime(object):
    c_LastTime = 0
    @classmethod
    def Clear(cls):
        import time
        cls.c_LastTime = time.time()

    @classmethod
    def PrintSpace(cls,msg):
        import time
        now = time.time()
        print msg,"---",now-cls.c_LastTime
        #cls.c_LastTime = time.time()

def main1():
    _CTime.Clear()
    lans = ["jp", ]

    transcache = {}

    for lan in lans:
        REPORTINFO.TITLE_LENS.data[lan] = 0
        REPORTINFO.FETURE_LENS.data[lan] = 0
        REPORTINFO.DESC_LENS.data[lan] = 0

        REPORTINFO.HASTRANSD_TIME.data["次数"] = 0
        REPORTINFO.HASTRANSD_TIME.data["字符"] = 0

        spu_list = CSysAsin.GetSpuList_ExtDone(lan)
        alldata = []
        REPORTINFO.US_SPU_NO_EN_DESC.data[lan] = len(spu_list)
        REPORTINFO.US_SPU_ERR_TRANS.data[lan] = 0
        ct = 0
        allct = len(spu_list)



        for spu_id in spu_list:
            product = SpuProduct.objects.filter(id = spu_id).values("title").first()
            title = product["title"]

            ct += 1
            if ct %1000==0:
                _CTime.PrintSpace("%s/%s"%(ct,allct))

            extinfo =SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
            if not extinfo:
                REPORTINFO.US_SPU_NO_EN_DESC.data[lan] -= 1
                continue
            description = extinfo["description"]
            feature = extinfo["feature"]
            texts = [title,description,feature]


            if title not in transcache:
                transcache[title] = 1
                REPORTINFO.TITLE_LENS.data[lan] += len(title)
            else:
                REPORTINFO.HASTRANSD_TIME.data["次数"] +=1
                REPORTINFO.HASTRANSD_TIME.data["字符"] += len(title)


            if feature not in transcache:
                transcache[feature] = 1
                REPORTINFO.FETURE_LENS.data[lan] += len(feature)
            else:
                REPORTINFO.HASTRANSD_TIME.data["字符"] += len(feature)
                REPORTINFO.HASTRANSD_TIME.data["次数"] += 1


            if description not in transcache:
                transcache[description] = 1
                REPORTINFO.DESC_LENS.data[lan] += len(description)
            else:
                REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
                REPORTINFO.HASTRANSD_TIME.data["字符"] += len(description)


            #REPORTINFO.DESC_LENS.data[lan] += len(description)

            #REPORTINFO.HASTRANSD_TIME = += len(title)

            #dn = misc.EN2JP(texts=texts)
            # newdata = {}
            # try:
            #     newdata["title"] = dn[title]
            #     newdata["description"] = dn[description]
            #     newdata["feature"] = dn[feature]
            # except:
            #     REPORTINFO.US_SPU_ERR_TRANS.data[lan] += 1
            #     continue
            # try:
            #     newdata["feature"] = dn[feature]
            # except:
            #     newdata["feature"] = ""


            #newdata["spu_id"] = spu_id
            #alldata.append(newdata)
        #CSpuDesc.Bluk_Add(alldata, lan, SOURCE.AMAZON_US_INFO_TRANS)

    print "\n".join(REPORTINFO.DoReport1())

def DownDesc():
    def _GetProduct(lan):
        dn = {
            "de": 8,
            "jp": 5,
            "es": 10,
            "it": 11,
            "fr": 12,
        }
        market_id = dn[lan]
        products = SysMarketProductMap.objects.filter(market_id=market_id).values("item_id").all()
        for product in products:
            yield product["item_id"]

    amazon_dict = {}
    # amazon_dict["it"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu",
    #                                         "oucher308-22", region="IT", Timeout=5, MaxQPS=1)oucher3@163.com
    #amazon_dict["it"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu", "oucher308-22",
    #                               region="IT", Timeout=5, MaxQPS=1)
    #amazon_dict["it"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher309-21",
    #                          region="IT", Timeout=5, MaxQPS=1)

    # amazon_dict["it"] = AmazonAPI("AKIAIADF3FDWG2EADWCA", "hCenHr3RzMYRsNmbXSiyywVknBS58AhN/llkujT", "oucher309-21",
    #                          region="IT", Timeout=5, MaxQPS=1)#43800052@qq.com
#########################################

    # amazon_dict["it"] = AmazonAPI("AKIAIGEGIKE7YTTY4GRQ", "ccF+1I42wYE5bs2TUmi+ghJXcSTqoS3Nn6lgbjr6", "oucher33-21",
    #                               region="IT", Timeout=5, MaxQPS=1)
    amazon_dict["it"] = AmazonAPI("AKIAINRPVKEXVQ65GN6A", "qo4GbATKZqDBpsVrFM6v3p/Y0DA5D/NogrCkyRIy", "oucher3-21",
                                  region="IT", Timeout=5, MaxQPS=1)
    amazon_dict["es"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher0e-21",
                                  region="ES", Timeout=5, MaxQPS=1)
    amazon_dict["fr"] = AmazonAPI("AKIAISQ5EL7RGVOIKCPQ", "KWZaLFPu3VY6nWKKBLldEKqTQzuFT2ahdr3VHNTy", "oucher3-21",
                                   region="FR", Timeout=5, MaxQPS=1)
    #amazon_dict["fr"] = AmazonAPI("AKIAJTJ6H6FMQPM5TSUQ", "JuVg/qCoJsQq9y3LHQnhmHCxb4VfqVAFMEBb+gih", "oucher3-21",
    #                               region="FR", Timeout=5, MaxQPS=1)
    #
    # amazon_dict["fr"] = AmazonAPI("AKIAII4O6ZBEJ6YJFX2Q", "q3euQaWkYlJQChvxc7/pblwq0F9jWWMbzv479a+/", "home0d81-21",
    #                               region="FR", Timeout=5, MaxQPS=1)


    amazon_dict["de"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher0e-21",
                                  region="DE", Timeout=5, MaxQPS=1)

    amazon_dict["jp"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu",
                                           "oucher308-22", region="JP", Timeout=5, MaxQPS=1)

    import socket
    socket.setdefaulttimeout(5)

    def _GetProducts(lan):
        ct = 0
        ct1 = 0
        alldata = []
        alldata.append(["asin", "title", "featurestr", "desc", "publisher", "detail_page_url"])

        amazon = amazon_dict[lan]

        product = _GetProduct(lan)
        flag = True
        while flag:
            items = []
            for i in range(10):
                try:
                    asin = product.next()
                except:
                    flag = False
                    break
                if asin:
                    items.append(asin)
                ct += 1

            if not items:
                break

            itemstr = ",".join(items)

            _CTime.PrintSpace(",".join(("分析<%s>"%lan, "%s/%s"%(ct, ct1), itemstr)))
            data = []
            import time
            time.sleep(1)
            try:
                amzproducts = amazon.lookup(ItemId=itemstr, ResponseGroup="Medium", Timeout=5)
            except Exception as e:
                print e
                continue
            if type(amzproducts) == list:
                pass
            else:
                amzproducts = [amzproducts]

            for amzproduct in amzproducts:
                ct1 += 1
                asin = amzproduct.asin
                title = amzproduct.title
                featurestr = ",".join(amzproduct.features)
                desc = amzproduct.editorial_review
                publisher = amzproduct.publisher
                detail_page_url = amzproduct.detail_page_url
                #data = [asin, title, featurestr, desc, publisher, detail_page_url]
                data = [asin, title, featurestr, desc, publisher, detail_page_url]
                alldata.append(data)

        _CTime.PrintSpace("执行结束")
        misc.save_data_xls(alldata, "amazon_%s.xls" % lan)
        misc.save_data_csv(alldata, "amazon_%s.csv" % lan)
        return ct, ct1
        # print product.asin_id,amzproduct.editorial_review
        # newdata[product.asin_id] = amzproduct.editorial_review
        # with open('./detail.txt', 'a') as f:
        #     f.write(json_encode(newdata, indent=4))
        # ct +=1

    alldata = []
    allct = 0
    allct1 = 1
    for lan in amazon_dict:
        ct, ct1 = _GetProducts(lan)
        allct += ct
        allct1 += ct1
        alldata.append(("<%s>下载了%s/%s" % (lan, ct1, ct)))

    _CTime.PrintSpace("下载完毕")
    print "共完成:%s/%s" % (allct1, allct)
    print "\n".join(alldata)


def DownNodeIDs():
    def _GetProduct(lan):
        dn = {
            "us": 2,
        }
        market_id = dn[lan]
        products = SysMarketProductMap.objects.filter(market_id=market_id).values("item_id").all()
        for product in products:
            yield product["item_id"]

    amazon_dict = {}
    # amazon_dict["it"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu",
    #                                         "oucher308-22", region="IT", Timeout=5, MaxQPS=1)oucher3@163.com
    #amazon_dict["it"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu", "oucher308-22",
    #                               region="IT", Timeout=5, MaxQPS=1)
    #amazon_dict["it"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher309-21",
    #                          region="IT", Timeout=5, MaxQPS=1)

    # amazon_dict["it"] = AmazonAPI("AKIAIADF3FDWG2EADWCA", "hCenHr3RzMYRsNmbXSiyywVknBS58AhN/llkujT", "oucher309-21",
    #                          region="IT", Timeout=5, MaxQPS=1)#43800052@qq.com
#########################################

    # amazon_dict["it"] = AmazonAPI("AKIAIGEGIKE7YTTY4GRQ", "ccF+1I42wYE5bs2TUmi+ghJXcSTqoS3Nn6lgbjr6", "oucher33-21",
    #                               region="IT", Timeout=5, MaxQPS=1)
    # amazon_dict["es"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher0e-21",
    #                               region="ES", Timeout=5, MaxQPS=1)
    # # amazon_dict["fr"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher3-21",
    # #                               region="FR", Timeout=5, MaxQPS=1)
    # amazon_dict["fr"] = AmazonAPI("AKIAJTJ6H6FMQPM5TSUQ", "JuVg/qCoJsQq9y3LHQnhmHCxb4VfqVAFMEBb+gih", "oucher3-21",
    #                               region="FR", Timeout=5, MaxQPS=1)
    #
    # amazon_dict["us"] = AmazonAPI("AKIAJGLFK6P37DXE4GOQ", "CKJUOQlcQ3Ar8wH9lIBKtePt5WxzWspePL3c/QsD", "oucher0e-21",
    #                               region="US", Timeout=5, MaxQPS=1)
   # amazon_dict["us"] = AmazonAPI("AKIAIGEGIKE7YTTY4GRQ", "ccF+1I42wYE5bs2TUmi+ghJXcSTqoS3Nn6lgbjr6", "oucher0e-21",
  #                                region="US", Timeout=5, MaxQPS=1)
    amazon_dict["us"] = AmazonAPI("AKIAJEXGSZ6O2Y6GCVGA", "D801IPdV5loOr29fW46/nVELHtsQZaWjh1M1Z1l3", "oucher309-21",
                             region="US", Timeout=5, MaxQPS=1)#43800052@qq.com
    #
    # amazon_dict["jp"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu",
    #                                        "oucher308-22", region="JP", Timeout=5, MaxQPS=1)
    # amazon_dict["us"] = AmazonAPI("AKIAJEHY7PZI24XSZ7GA", "al5M1gd5UVbDyjihIzF6kn/47ok7M4S29546vqRu",
    #                                        "oucher308-22", region="US", Timeout=5, MaxQPS=1)
    import socket
    socket.setdefaulttimeout(5)

    needdownparent = []
    def _GetProducts(lan):
        ct = 0
        ct1 = 0
        alldata = []
        alldata.append(["asin", "title", "featurestr", "desc", "publisher", "detail_page_url"])

        amazon = amazon_dict[lan]

        product = _GetProduct(lan)
        flag = True
        while flag:
            items = []
            for i in range(10):
                try:
                    asin = product.next()
                except:
                    flag = False
                    break
                if asin:
                    items.append(asin)
                ct += 1

            if not items:
                break

            itemstr = ",".join(items)

            _CTime.PrintSpace(",".join(("分析<%s>"%lan, "%s/%s"%(ct, ct1), itemstr,str(len(needdownparent)))))
            data = []
            import time
            time.sleep(1)
            try:
                amzproducts = amazon.lookup(ItemId=itemstr, ResponseGroup="BrowseNodes", Timeout=5)
            except Exception as e:
                print e
                continue
            if type(amzproducts) == list:
                pass
            else:
                amzproducts = [amzproducts]

            for amzproduct in amzproducts:
                ct1 += 1
                asin = amzproduct.asin
                browse_nodes = amzproduct.browse_nodes
                try:
                    nodeid = browse_nodes[0].id
                except:
                    needdownparent.append(asin)
                    continue
                # print node.id,222222222222
                # sdf
                data = [asin,nodeid ]
                alldata.append(data)

        _CTime.PrintSpace("执行结束")

        misc.save_data_csv(alldata, "amazon_%s.csv" % lan)
        return ct, ct1

    alldata = []
    allct = 0
    allct1 = 1
    for lan in amazon_dict:
        ct, ct1 = _GetProducts(lan)
        allct += ct
        allct1 += ct1
        alldata.append(("<%s>下载了%s/%s" % (lan, ct1, ct)))

    _CTime.PrintSpace("下载完毕")
    print "共完成:%s/%s" % (allct1, allct)
    print "\n".join(alldata)

nobrandlist =None
lostasinlist =None
def DownBrandInfo():
    global lostasinlist,nobrandlist
    retrylist = []
    nobrandlist = []
    lostasinlist = []
    # def _GetProduct(lan):
    #     dn = {
    #         "us": 2,
    #     }
    #     market_id = dn[lan]
    #     products = SysMarketProductMap.objects.filter(market_id=market_id).values("item_id").all()
    #     for product in products:
    #         yield product["item_id"]

    def _GetProduct(lan):
        for asin in amazonasintrack.objects.values_list("asin",flat=True):
            yield asin

        # for asin in retrylist:
        #     yield asin

    amazon_dict = {}

    amazon_dict["us"] = AmazonAPI("AKIAJEXGSZ6O2Y6GCVGA", "D801IPdV5loOr29fW46/nVELHtsQZaWjh1M1Z1l3", "oucher309-21",
                             region="US", Timeout=5, MaxQPS=1)#43800052@qq.com

    import socket
    socket.setdefaulttimeout(5)

    needdownparent = []
    def _GetProducts(lan):
        global lostasinlist,nobrandlist
        ct = 0
        ct1 = 0
        alldata = []
        alldata.append(["asin", "title", "featurestr", "desc", "publisher", "detail_page_url"])

        amazon = amazon_dict[lan]

        product = _GetProduct(lan)
        flag = True
        while flag:
            items = []
            for i in range(10):
                try:
                    asin = product.next()
                except:
                    flag = False
                    break
                if asin:
                    items.append(asin)
                ct += 1
            #print items,222222222
            if not items:
                break
            # if ct>4000:
            #     break
            lostasinlist += items[:]
            itemstr = ",".join(items)

            _CTime.PrintSpace(",".join(("分析<%s>"%lan, "%s/%s"%(ct, ct1), itemstr,str(len(retrylist)))))
            print len(lostasinlist),len(nobrandlist)
            data = []
            # import time
            # time.sleep(1)
            try:
                amzproducts = amazon.lookup(ItemId=itemstr, ResponseGroup="ItemAttributes", Timeout=5)
            except Exception as e:
                retrylist.extend(items)
                print type(e),dir(e),e.args,e.message,len(retrylist),111111111111111
                continue
            if type(amzproducts) == list:
                pass
            else:
                amzproducts = [amzproducts]

            for amzproduct in amzproducts:

                asin = amzproduct.asin
                try:
                    lostasinlist.remove(asin)
                except:
                    pass

                brandname = amzproduct.brand
                if not brandname:
                    nobrandlist.append(asin)
                    continue
                ct1 += 1
                #print asin,brandname,111111111
                # browse_nodes = amzproduct.browse_nodes
                # try:
                #     nodeid = browse_nodes[0].id
                # except:
                #     needdownparent.append(asin)
                #     continue

                data = [asin,brandname]
                info = amazonbrand.objects.filter(asin=asin).first()
                if not info:
                    info = amazonbrand()
                    info.asin = asin
                info.brand = brandname
                info.save()

                # with open("amazon_brand.csv","a") as f:
                #     f.write("%s,%s\n"%(asin,brandname))
                #alldata.append(data)

        _CTime.PrintSpace("执行结束")

        #misc.save_data_csv(alldata, "amazon_%s.csv" % lan)
        return ct, ct1

    alldata = []
    allct = 0
    allct1 = 1
    for lan in amazon_dict:
        ct, ct1 = _GetProducts(lan)
        allct += ct
        allct1 += ct1
        alldata.append(("<%s>下载了%s/%s" % (lan, ct1, ct)))
    nobrandlist = list(set(nobrandlist))
    lostasinlist = list(set(lostasinlist))
    with open("nobrandlist.csv","w") as f:
        f.write("\n".join(nobrandlist))
    with open("lostasinlist.csv","w") as f:
        f.write("\n".join(lostasinlist))

    _CTime.PrintSpace("下载完毕")
    print "共完成:%s/%s" % (allct1, allct)
    print "\n".join(alldata)


def main():
    #
    lans = ["it","de","jp","es","fr"]
    #lans = ["de", "jp", "es", "fr"]
    #lans = ["es",]
    for lan in lans:
        filename  = "upload/amazon/desc/amazon_%s.xls"%lan
        alldata = ImportXls(filename)
        #REPORTINFO.ASIN_DOWN.data[lan]=len(alldata)
        newdata_dict = {}
        for data in alldata:
            newdata = {}

            asin,title,featurestr,desc = data[:4]
            newdata["asin"] = asin
            newdata["title"] = title
            newdata["feature"] = featurestr
            newdata["description"] = desc
            spu_id = Asin2Spu(asin)
            if spu_id in (0,None):
                continue
            newdata["spu_id"] = spu_id
            olddata = newdata_dict.get(spu_id,None)
            if olddata:
                if len(olddata["description"]) > len(newdata["description"]):
                    continue
            newdata_dict[spu_id] = newdata

        # alldata = []
        # asin_list = CSysAsin.GetAsinList(lan)
        # for newdata in newdata_dict.values():
        #     if newdata["asin"] not in asin_list:
        #         continue
        #     alldata.append(newdata)
        alldata = newdata_dict.values()

        REPORTINFO.ALL_SPU_DOWN.data[lan] = len(alldata)
        REPORTINFO.ALL_SPU_REDUCE_NO_DESC.data[lan] = 0
        REPORTINFO.DESCLEN_LT30.data[lan] = 0

        alldata1 =[]
        for newdata in alldata:

            ct =len(newdata["description"])
            if ct<30:
                REPORTINFO.DESCLEN_LT30.data[lan] +=1
            if ct==0:
                #REPORTINFO.ALL_SPU_REDUCE_NO_DESC.data[lan] += 1
                continue

            alldata1.append(newdata)

        REPORTINFO.ALL_SPU_REDUCE_NO_DESC.data[lan] = len(alldata1)

        CSpuDesc.Bluk_Add(alldata1,lan,SOURCE.AMAZON_INFO)

    print "\n".join(REPORTINFO.DoReport())

def main2():
    lan = "jp"
    # asin_list = CSysAsin.GetAsinList(lan)
    #
    # market_id = GetMarketID(lan)
    # oQuery = SysMarketProductMap.objects.filter(market=market_id)
    # REPORTINFO.AMA_PRODUCTS_PUSHED.data["asin"] = oQuery.count()
    # REPORTINFO.AMA_PRODUCTS_PUSHED.data["sku"] = oQuery.values("sku_id").distinct().count()
    #
    # sku_list = oQuery.values("sku_id")#.values_list("sku_id",flat=True)
    # REPORTINFO.AMA_PRODUCTS_PUSHED.data["spu"] =SkuProduct.objects.filter(id__in=sku_list).values("spu_id").distinct().count()
    #
    # filename = "amazon_%s.xls" % lan
    # #alldata = ImportXls(filename)
    #
    #
    #
    # #newdata_dict = {}
    # alldata =[]
    # skudict = {}
    # spudict = {}
    #
    # for data in ImportXls(filename):
    #     asin = data[0]
    #
    #     spu_id,sku_id = Asin2SpuSku(asin)
    #     if spu_id in (0, None):
    #         continue
    #     skudict[sku_id] = 1
    #     spudict[spu_id] = 1
    #
    #     alldata.append(data)
    #
    # REPORTINFO.AMA_PRODUCTS_DOWNED.data["asin"] = len(alldata)
    # REPORTINFO.AMA_PRODUCTS_DOWNED.data["sku"] = len(skudict)
    # REPORTINFO.AMA_PRODUCTS_DOWNED.data["spu"] = len(spudict)
    #
    #
    # #alldata = newdata_dict.values()
    #
    # skudict = {}
    # spudict = {}
    # alldata1 = []
    # for newdata in alldata:
    #     asin, title, featurestr, desc = newdata[:4]
    #     ct = len(desc)
    #     if ct < 30:
    #     #     REPORTINFO.DESCLEN_LT30.data[lan] += 1
    #     # if ct == 0:
    #         continue
    #     spu_id,sku_id = Asin2SpuSku(asin)
    #
    #     skudict[sku_id] = 1
    #     spudict[spu_id] = 1
    #
    #     alldata1.append(newdata)
    #
    # REPORTINFO.AMA_PRODUCTS_REDUCE.data["asin"] = len(alldata1)
    # REPORTINFO.AMA_PRODUCTS_REDUCE.data["sku"] = len(skudict)
    # REPORTINFO.AMA_PRODUCTS_REDUCE.data["spu"] = len(spudict)
    #
    # newdata_dict = {}
    # for data in alldata1:
    #     asin, title, featurestr, desc = data[:4]
    #     newdata = {}
    #     newdata["asin"] = asin
    #     spu_id, sku_id = Asin2SpuSku(asin)
    #     newdata["title"] = title
    #     newdata["feature"] = featurestr
    #     newdata["description"] = desc
    #     newdata["spu_id"] = spu_id
    #     olddata = newdata_dict.get(spu_id, None)
    #     if olddata:
    #         if len(olddata["description"]) > len(newdata["description"]):
    #             continue
    #
    #     newdata_dict[spu_id]= newdata
    #
    # # CSpuDesc.Bluk_Add(newdata_dict.values(), lan, SOURCE.AMAZON_INFO)
    # REPORTINFO.AMA_PRODUCTS_SAVED.num = len(newdata_dict)
    #------------------------------------------------------------------

    #
    # oQuery = SkuProduct.objects.filter()
    # REPORTINFO.ALL_PRODUCTS.num = oQuery.values("spu_id").distinct().count()
    #
    # SaledProducts = SkuStatistic.objects.filter(platform="Amazon").values("spu").distinct()
    # #SaledProducts = SkuDaysStatistic.objects.values("sku").filter(total_qty__gt=0).values("sku")
    # oQuery = oQuery.filter(id__in=SaledProducts)
    # REPORTINFO.SALED_PRODUCTS.num = oQuery.values("spu_id").distinct().count()
    #
    # done_spu_list = CSpuDesc.GetDoned_Spu_List(lan)
    # oQuery = oQuery.exclude(spu__in=done_spu_list)
    # REPORTINFO.SALED_PRODUCTS_NOTUSED.num = oQuery.values("spu_id").distinct().count()
    #
    # spu_list = oQuery.values_list("spu_id",flat=True).distinct()
    # allct = len(spu_list)
    # alldata = []
    # for spu_id in spu_list:
    #     #print spu_id,222222
    #     product = SpuProduct.objects.filter(id=spu_id).values("title").first()
    #     title = product["title"]
    #
    #     ct += 1
    #     if ct % 1000 == 0:
    #         _CTime.PrintSpace("%s/%s" % (ct, allct))
    #
    #     extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
    #     if not extinfo:
    #         continue
    #     description = extinfo["description"]
    #
    #     if len(description)<30:
    #         continue
    #
    #     feature = extinfo["feature"]
    #     data = [spu_id,title,feature,description]
    #     alldata.append(data)
    #
    # REPORTINFO.SALED_PRODUCTS_DESCGT30.m_Num = len(alldata)
    # REPORTINFO.SALED_PRODUCTS_TRAN_TIME.m_Num = len(alldata)
    # REPORTINFO.SALED_PRODUCTS_TRAN_COUNT.m_Num = 0
    # newalldata = []
    # transcache = {}
    # for data in alldata:
    #     spu_id, title, feature, description = data
    #
    #     if title not in transcache:
    #         transcache[title] = 1
    #         REPORTINFO.SALED_PRODUCTS_TRAN_COUNT.m_Num += len(title)
    #     # else:
    #     #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
    #     #     REPORTINFO.HASTRANSD_TIME.data["字符"] += len(title)
    #
    #     if feature not in transcache:
    #         transcache[feature] = 1
    #         REPORTINFO.SALED_PRODUCTS_TRAN_COUNT.m_Num += len(feature)
    #     # else:
    #     #     REPORTINFO.HASTRANSD_TIME.data["字符"] += len(feature)
    #     #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
    #
    #     if description not in transcache:
    #         transcache[description] = 1
    #         REPORTINFO.SALED_PRODUCTS_TRAN_COUNT.m_Num += len(description)
    #     # else:
    #     #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
    #     #     REPORTINFO.HASTRANSD_TIME.data["字符"] += len(description)
    #
    #
    #         # ------------------------------------------------------------------
    #         # CSpuDesc.Bluk_Add(alldata, lan, SOURCE.AMAZON_INFO)
    #         REPORTINFO.AMA_PRODUCTS_SAVED.num = len(newdata_dict)
    #
    #         oQuery = SkuProduct.objects.filter()
    #         REPORTINFO.ALL_PRODUCTS.num = oQuery.values("spu_id").distinct().count()
    #
    #         # HASSTOCKProducts = SkuDaysStatistic.objects.values("sku").filter(total_qty__gt=0).values("sku")
    #         # oQuery = oQuery.filter(id__in=HASSTOCKProducts)
    #         hasstore_products = SkuWarehouseInventory.objects.values("sku_id").annotate(
    #             allct=Sum('on_hand_qty')).filter(
    #             allct__gt=1).values("sku_id")
    #         query_select = Q(purchase_ok=1) | Q(id__in=hasstore_products)
    #         allproducts = SkuProduct.objects.filter(query_select).values("id")
    #         oQuery = oQuery.filter(id__in=allproducts)
    #
    #         REPORTINFO.HASSTOCK_PRODUCTS.num = oQuery.values("spu_id").distinct().count()
    #
    #         done_spu_list = CSpuDesc.GetDoned_Spu_List(lan)
    #         oQuery = oQuery.exclude(spu__in=done_spu_list)
    #         REPORTINFO.HASSTOCK_PRODUCTS_NOTUSED.num = oQuery.values("spu_id").distinct().count()
    #
    #         spu_list = oQuery.values_list("spu_id", flat=True).distinct()
    #         allct = len(spu_list)
    #         alldata = []
    #         ct = 0
    #         for spu_id in spu_list:
    #             # print spu_id,222222
    #             product = SpuProduct.objects.filter(id=spu_id).values("title").first()
    #             title = product["title"]
    #
    #             ct += 1
    #             if ct % 1000 == 0:
    #                 _CTime.PrintSpace("%s/%s" % (ct, allct))
    #
    #             extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
    #             if not extinfo:
    #                 continue
    #             description = extinfo["description"]
    #
    #             if len(description) < 30:
    #                 continue
    #
    #             feature = extinfo["feature"]
    #             data = [spu_id, title, feature, description]
    #             alldata.append(data)
    #
    #         REPORTINFO.HASSTOCK_PRODUCTS_DESCGT30.m_Num = len(alldata)
    #         REPORTINFO.HASSTOCK_PRODUCTS_TRAN_TIME.m_Num = len(alldata)
    #         REPORTINFO.HASSTOCK_PRODUCTS_TRAN_COUNT.m_Num = 0
    #         newalldata = []
    #         transcache = {}
    #         for data in alldata:
    #             spu_id, title, feature, description = data
    #
    #             if title not in transcache:
    #                 transcache[title] = 1
    #                 REPORTINFO.HASSTOCK_PRODUCTS_TRAN_COUNT.m_Num += len(title)
    #             # else:
    #             #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
    #             #     REPORTINFO.HASTRANSD_TIME.data["字符"] += len(title)
    #
    #             if feature not in transcache:
    #                 transcache[feature] = 1
    #                 REPORTINFO.HASSTOCK_PRODUCTS_TRAN_COUNT.m_Num += len(feature)
    #             # else:
    #             #     REPORTINFO.HASTRANSD_TIME.data["字符"] += len(feature)
    #             #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
    #
    #             if description not in transcache:
    #                 transcache[description] = 1
    #                 REPORTINFO.HASSTOCK_PRODUCTS_TRAN_COUNT.m_Num += len(description)
    #                 # else:
    #                 #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
    #                 #     REPORTINFO.HASTRANSD_TIME.data["字符"]
    #


    # ------------------------------------------------------------------
    oQuery = SkuProduct.objects.filter()
    REPORTINFO.ALL_PRODUCTS.num = oQuery.values("spu_id").distinct().count()


    # PUSHABLEProducts = SkuDaysStatistic.objects.values("sku").filter(total_qty__gt=0).values("sku")
    # oQuery = oQuery.filter(id__in=PUSHABLEProducts)
    hasstore_products = SkuWarehouseInventory.objects.values("sku_id").annotate(allct=Sum('on_hand_qty')).filter(
            allct__gt=1).values("sku_id")

    query_select = Q(purchase_ok=1) | Q(id__in=hasstore_products)
    #query_select = Q(id__in=hasstore_products)
    allproducts = SkuProduct.objects.filter(query_select).values("id")
    oQuery = oQuery.filter(id__in=allproducts)

    REPORTINFO.PUSHABLE_PRODUCTS.num = oQuery.values("spu_id").distinct().count()

    SaledProducts = SkuStatistic.objects.values("sku").distinct()
    oQuery = oQuery.filter(id__in=SaledProducts)
    REPORTINFO.PUSHABLE_PRODUCTS_NOSALE.num = oQuery.values("spu_id").distinct().count()



    # done_spu_list = CSpuDesc.GetDoned_Spu_List(lan)
    # oQuery = oQuery.exclude(spu__in=done_spu_list)
    # REPORTINFO.PUSHABLE_PRODUCTS_NOTUSED.num = oQuery.values("spu_id").distinct().count()

    spu_list = oQuery.values_list("spu_id", flat=True).distinct()
    allct = len(spu_list)
    alldata = []
    ct =0
    for spu_id in spu_list:
        # print spu_id,222222
        product = SpuProduct.objects.filter(id=spu_id).values("title").first()



        ct += 1
        if ct % 1000 == 0:
            _CTime.PrintSpace("%s/%s" % (ct, allct))
        if not product:
            continue
        title = product["title"]
        extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
        if not extinfo:
            continue
        description = extinfo["description"]

        if len(description) < 30:
            continue

        feature = extinfo["feature"]
        data = [spu_id, title, feature, description]
        alldata.append(data)

    REPORTINFO.PUSHABLE_PRODUCTS_DESCGT30.m_Num = len(alldata)
    REPORTINFO.PUSHABLE_PRODUCTS_TRAN_TIME.m_Num = len(alldata)
    REPORTINFO.PUSHABLE_PRODUCTS_TRAN_COUNT.m_Num = 0
    newalldata = []
    transcache = {}
    for data in alldata:
        spu_id, title, feature, description = data

        if title not in transcache:
            transcache[title] = 1
            REPORTINFO.PUSHABLE_PRODUCTS_TRAN_COUNT.m_Num += len(title)
        # else:
        #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
        #     REPORTINFO.HASTRANSD_TIME.data["字符"] += len(title)

        if feature not in transcache:
            transcache[feature] = 1
            REPORTINFO.PUSHABLE_PRODUCTS_TRAN_COUNT.m_Num += len(feature)
        # else:
        #     REPORTINFO.HASTRANSD_TIME.data["字符"] += len(feature)
        #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1

        if description not in transcache:
            transcache[description] = 1
            REPORTINFO.PUSHABLE_PRODUCTS_TRAN_COUNT.m_Num += len(description)
            # else:
            #     REPORTINFO.HASTRANSD_TIME.data["次数"] += 1
            #     REPORTINFO.HASTRANSD_TIME.data["字符"]


    #REPORTINFO.SALED_PRODUCTS_DESCGT30m_Num = oQuery.values("spu_id").distinct().count()
    #REPORTINFO.NewReport()
    print "\n".join(REPORTINFO.NewReport())
   # # alldata = filter(clearlt30desc,alldata)
   #
   #  SALED_PRODUCTS = "系统有库存有销量的产品spu数"
   #  SALED_PRODUCTS_TRAN_TIME = "需要翻译的spu数"
   #  SALED_PRODUCTS_TRAN_COUNT = "需要翻译的字符数"
   #
   #  PUSHABLE_PRODUCTS = "系统可上架的产品spu数"
   #  PUSHABLE_PRODUCTS_TRAN_TIME = "需要翻译的spu数"
   #  PUSHABLE_PRODUCTS_TRAN_TIME = "需要翻译的字符数"

def GetTransReport():
    lan = "jp"
    alldata,result = misc.get_data_xls("upload/amazon/sku_fortrans_jp.xls")
    skulist = []
    for data in alldata:
        skulist.append(str(data[1].strip()))

    #skulist = skulist_str.split(",")


    print "总共需要处理sku-->",len(skulist)
    # ------------------------------------------------------------------
    oQuery = SkuProduct.objects.filter(sku__in=skulist)
    print "有效sku-->",len(oQuery.values_list("sku",flat=True))


    oQuery = SkuProduct.objects.filter(sku__in=skulist)
    print "有效spu-->",oQuery.values_list("spu",flat=True).distinct().count()
    allct = oQuery.values_list("spu",flat=True).distinct().count()


    alldata = []
    ct =0
    for spu_id in oQuery.values_list("spu",flat=True).distinct():
        product = SpuProduct.objects.filter(id=spu_id).values("title").first()

        ct += 1
        if ct % 100 == 0:
            _CTime.PrintSpace("%s/%s" % (ct, allct))
        if not product:
            continue
        title = product["title"]
        extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
        if  extinfo:
            feature = extinfo["feature"]
            description = extinfo["description"]
        else:
            feature = ""
            description = ""
        # if len(description) < 30:
        #     continue

        data = [spu_id, title, feature, description]
        alldata.append(data)

    transcache = {}
    for data in alldata:
        spu_id, title, feature, description = data

        if title not in transcache:
            transcache[title] = len(title)

        if feature not in transcache:
            transcache[feature] = len(feature)

        if description not in transcache:
            transcache[description] = len(description)


    print "需要翻译字符长度--->",sum(transcache.values())

    # oldinfo_list = ReadCache("de")
    # _CTime.PrintSpace("读取以前上架的产品信息")
    # transcache = {}
    # for data in alldata:
    #     spu_id, title, feature, description = data
    #
    #     if title not in transcache and title not in oldinfo_list:
    #         transcache[title] = len(title)
    #
    #     if feature not in transcache and feature not in oldinfo_list:
    #         transcache[feature] = len(feature)
    #
    #     if description not in transcache and description not in oldinfo_list:
    #         transcache[description] = len(description)
    #
    #
    # print "使用原来的上架产品后需要翻译字符长度--->",sum(transcache.values())
def OutTrans(lan):
    alldata,result = misc.get_data_xls("upload/amazon/sku_fortrans_%s.xls"%lan)
    skulist = []
    for data in alldata:
        skulist.append(str(data[1].strip()))

    print "总共需要处理sku-->",len(skulist)
    # ------------------------------------------------------------------
    oQuery = SkuProduct.objects.filter(sku__in=skulist)

    print "有效sku-->",len(oQuery.values_list("sku",flat=True))


    oQuery = SkuProduct.objects.filter(sku__in=skulist)
    print "有效spu-->",oQuery.values_list("spu",flat=True).distinct().count()
    allct = oQuery.values_list("spu",flat=True).distinct().count()


    alldata = [
       [ "spu","旧标题","旧摘要","旧描述","新标题","新摘要","新描述"]
    ]
    ct =0
    for spu_id in oQuery.values_list("spu",flat=True).distinct():
        product = SpuProduct.objects.filter(id=spu_id).values("title","spu").first()
        spucode = product["spu"]
        ct += 1
        if ct % 100 == 0:
            _CTime.PrintSpace("%s/%s" % (ct, allct))
        if not product:
            continue

        # if CSpuDesc.objects.filter(spu_id=spu_id).filter(language=lan).exists():
        #     continue

        title = product["title"]
        extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
        if  extinfo:
            feature = extinfo["feature"]
            description = extinfo["description"]
        else:
            feature = ""
            description = ""
        # if len(description) < 30:
        #     continue
        newinfo = CSpuDesc.objects.filter(spu_id=spu_id).filter(language=lan).first()
        if newinfo:
            data = [spucode, title, feature, description,newinfo.title,newinfo.feature,newinfo.description]
        else:
            data = [spucode, title, feature, description, "","",""]

        alldata.append(data)
    misc.save_data_xls(alldata,"upload/amazon/out%s.xls"%lan)

def DoTrans(lan):
    alldata,result = misc.get_data_xls("upload/amazon/sku_fortrans_%s.xls"%lan)
    skulist = []
    for data in alldata:
        skulist.append(str(data[1].strip()))

    print "总共需要处理sku-->",len(skulist)
    # ------------------------------------------------------------------
    oQuery = SkuProduct.objects.filter(sku__in=skulist)

    print "有效sku-->",len(oQuery.values_list("sku",flat=True))


    oQuery = SkuProduct.objects.filter(sku__in=skulist)
    print "有效spu-->",oQuery.values_list("spu",flat=True).distinct().count()
    allct = oQuery.values_list("spu",flat=True).distinct().count()


    alldata = []
    ct =0
    for spu_id in oQuery.values_list("spu",flat=True).distinct():
        product = SpuProduct.objects.filter(id=spu_id).values("title").first()
        ct += 1
        if ct % 100 == 0:
            _CTime.PrintSpace("%s/%s" % (ct, allct))
        if not product:
            continue

        if CSpuDesc.objects.filter(spu_id=spu_id).filter(language=lan).exists():
            continue

        title = product["title"]
        extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
        if  extinfo:
            feature = extinfo["feature"]
            description = extinfo["description"]
        else:
            feature = ""
            description = ""
        # if len(description) < 30:
        #     continue

        data = [spu_id, title, feature, description]
        alldata.append(data)
        #print data
    transcache = {}
    #savedata = []

    #sdfsadf
    ct =0
    allct = len(alldata)
    #print alldata,23123123
    for data in alldata:
        spu_id, title, feature, description = data
        #print title
        #continue
        try:
            features = eval(feature)
            features_lens = len(features)

        except:
            features = [feature,]
            features_lens = 1
        olddata = {
            "title":title,
            #"feature": feature,
            "description": description,
        }


        for i in range(features_lens):
            olddata["feature%s"%i] = features[i]

        newdata = {}
        #continue


        #print olddata
        for key in olddata:
            value = olddata[key]
            if value not in transcache:
                if value:
                    dn = misc.Trans(lan,texts=[value])
                    try:
                        newvalue = dn.values()[0]
                    except Exception as e:
                        misc.ColorPrint("翻译失败",e,key,spu_id,value)
                        newvalue = ""
                    newvalue = newvalue.replace("</ ","</")
                    newvalue = newvalue.replace(" />", "/>")
                    if ct % 50 == 0:
                        print value ,"-->",newvalue
                else:
                    newvalue = ""
                transcache[value] =newvalue
            newdata[key] = transcache[value]

        newfeatures = []
        for i in range(features_lens):
            newvalue = newdata["feature%s"%i]
            newfeatures.append(newvalue)


        #newdata["feature"] =  "'%s'"%newdata["feature"].decode("utf-8").encode("utf-8").replace("||","','")
        newdata["feature"] = "||".join(newfeatures)
        # if title in transcache:
        #     newdata[title] = transcache[title]
        #     title = ""
        #
        #
        # if feature in transcache:
        #     newdata[feature] = transcache[feature]
        #     feature = ""
        #
        # if description in transcache:
        #     newdata[description] = transcache[description]
        #     description = ""
        #
        # texts = [title,description,feature]

        ct += 1
        if ct % 50 == 0:
            _CTime.PrintSpace("%s/%s" % (ct, allct))

        #print texts,ct,2222
        # if texts:
        #     dn = misc.EN2DE(texts=texts)
        #
        #     # try:
        #     if title:
        #         transcache[title] = newdata["title"] = dn[title]
        #
        #     if description:
        #         transcache[description] = newdata["description"] = dn[description]
        #     if feature:
        #         transcache[feature] = newdata["feature"] = dn[feature]
        #     # except Exception as e:
            #     print e,9111
            #     continue

        newdata["spu_id"] = spu_id
        #savedata.append(newdata)
        CSpuDesc.Bluk_Add([newdata], lan, SOURCE.AMAZON_US_INFO_TRANS)


    #CSpuDesc.Bluk_Add(savedata, lan, SOURCE.AMAZON_US_INFO_TRANS)

# g_OnTrans = False
# def DoTransViews(lan,celery_task=None):
#     import time
#     class _task(object):
#         def __init__(self,task,spuct,skuct):
#             self.m_Task = task
#             self.m_SpuCt = spuct
#             self.m_SkuCt = skuct
#             self.m_Simple = ""
#
#         def update_state(self,curct,failct,allcharct=0):
#             if self.m_Task:
#                 self.m_Task.update_state(state="PROGRESS",meta={
#                     "curct": curct,
#                     "failct": failct,
#                     "spuct": self.m_SpuCt,
#                     "skuct": self.m_SkuCt,
#                     "simple": self.m_Simple,
#                     "allcharct":allcharct
#                 })
#
#     curtask = _task(celery_task, 1000, 4000)
#     for i in range(10000):
#         if i %100==0:
#             curtask.m_Simple = "%s已经准备好了"
#         curtask.update_state(i,i/10,i*10)
#         yield i
#         time.sleep(1)

g_OnTrans = False
def DoTransViews(lan,celery_task=None):
    class _task(object):
        def __init__(self,task,spuct,transct):
            self.m_Task = task
            self.m_SpuCt = spuct
            self.m_transct = transct
            self.m_Simple = ""

        def update_state(self,curct,failct,allcharct=0):
            if self.m_Task:
                self.m_Task.update_state(state="PROGRESS",meta={
                    "curct": curct,
                    "failct": failct,
                    "spuct": self.m_SpuCt,
                    "transct": self.m_transct,
                    "simple": self.m_Simple,
                    "allcharct":allcharct
                })
    #if celery_task==None:

    #celery_task.update_state()
    alldata,result = misc.get_data_xls("upload/amazon/sku_fortrans_%s.xls"%lan)
    skulist = []
    for data in alldata:
        skulist.append(str(data[1].strip()))

    print "总共需要处理sku-->%s"%len(skulist)
    # ------------------------------------------------------------------
    oQuery = SkuProduct.objects.filter(sku__in=skulist)
    skuct = len(oQuery.values_list("sku",flat=True))
    print "有效sku-->%s"%skuct


    oQuery = SkuProduct.objects.filter(sku__in=skulist)
    spuct = oQuery.values_list("spu",flat=True).distinct().count()
    print "有效spu-->%s"% spuct

    allct = oQuery.values_list("spu",flat=True).distinct().count()


    alldata = []
    ct =0
    for spu_id in oQuery.values_list("spu",flat=True).distinct():
        product = SpuProduct.objects.filter(id=spu_id).values("title").first()
        ct += 1
        if ct % 100 == 0:
            print "%s/%s" % (ct, allct)
        if not product:
            continue

        if CSpuDesc.objects.filter(spu_id=spu_id).filter(language=lan).exists():
            continue

        title = product["title"]
        extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
        if  extinfo:
            feature = extinfo["feature"]
            description = extinfo["description"]
        else:
            feature = ""
            description = ""


        data = [spu_id, title, feature, description]
        alldata.append(data)

    transcache = {}
    print "实际需要翻译spu数%s"%len(alldata)
    curtask = _task(celery_task, spuct, len(alldata))
    ct =0
    failct = 0
    allct = len(alldata)
    allcharct = 0
    for data in alldata:
        spu_id, title, feature, description = data
        try:
            features = eval(feature)
            features_lens = len(features)

        except:
            features = [feature,]
            features_lens = 1
        olddata = {
            "title":title,
            #"feature": feature,
            "description": description,
        }


        for i in range(features_lens):
            olddata["feature%s"%i] = features[i]

        newdata = {}
        #continue


        #print olddata
        for key in olddata:
            value = olddata[key]
            if value not in transcache:
                if value:
                    dn = misc.Trans(lan,texts=[value])
                    allcharct += len(value)
                    try:
                        newvalue = dn.values()[0]
                    except Exception as e:
                        failct += 1
                        misc.ColorPrint("翻译失败",e,key,spu_id,value)
                        newvalue = ""
                    newvalue = newvalue.replace("</ ","</")
                    newvalue = newvalue.replace(" />", "/>")
                    if ct % 50 == 0:
                        print "%s-->%s"%(value,newvalue)
                else:
                    newvalue = ""
                transcache[value] =newvalue
            newdata[key] = transcache[value]

        newfeatures = []
        for i in range(features_lens):
            newvalue = newdata["feature%s"%i]
            newfeatures.append(newvalue)


        newdata["feature"] = "||".join(newfeatures)

        ct += 1
        if ct % 50 == 1:
            curtask.m_Simple = newdata["title"]
            print "%s/%s" % (ct, allct)
        curtask.update_state(ct,failct,allcharct)
        newdata["spu_id"] = spu_id
        if newdata["title"]=="":#标题翻译失败算翻译失败
            continue
        CSpuDesc.Bluk_Add([newdata], lan, SOURCE.AMAZON_US_INFO_TRANS)

    print "总共翻译字符%s"%allcharct
    return {
        "curct": ct,
        "failct": failct,
        "spuct": curtask.m_SpuCt,
        "transct": curtask.m_transct,
        "simple": curtask.m_Simple,
        "allcharct":allcharct
    }

def ReadCache(lan):
    dn = {}
    products = CSpuDesc.objects.filter(language=lan).values()
    for product in products:

        spu_id = product["spu_id"]

        description = product["description"]
        feature = product["feature"]
        title = product["title"]

        product = SpuProduct.objects.filter(id=spu_id).values("title").first()


        if not product:
            continue
        trans_title = product["title"]
        dn[title] = trans_title
        extinfo = SpuDescriptionEn.objects.filter(spu=spu_id).values().first()
        if  extinfo:
            trans_feature = extinfo["feature"]
            trans_description = extinfo["description"]
            dn[title] = trans_title
            dn[feature] = trans_feature
            dn[description] = trans_description

    return dn