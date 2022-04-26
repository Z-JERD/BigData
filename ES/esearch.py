import json
import traceback

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# pip install elasticsearch==7.7.0


class ElasticObj:

    # 查询方式

    """
    body查询：

    分页： from、size，from  从第几条数据开始展示，size 一页展示多少条数据

    1. 查询全部: match_all

        eg:
            {"query": {"match_all": {}}}

        eg:

             body = {
                "from": 1,
                "size": 5,
                "query": {

                     "match_all": {}
                }
            }

    2. 等于查询: term与terms

        精确的关键词匹配查询，不对查询条件进行分词

        term、terms查询，它并不知道分词器的存在，这种查询适合keyword、numeric、date等明确值的

        term: 查询 xx = "xx"
        terms: 查询 xx = "xx" 或 xx = "yy"

        eg: 查询 movie_start_time 等于 2020-12-11的值

             body = {
                "query": {
                    "term": {
                        "movie_start_time": "2020-12-11"
                    }
                }
            }

        eg: 查询movie_end_time的值为2021-02-20或2020-01-23的值

            body = {
                "query": {
                    "terms": {
                        "movie_end_time": ["2021-02-20", "2020-01-23"]
                    }
                }
            }

        eg: 查询pid为M2020013的数据

             body = {
                    "query": {
                        "term": {
                            "pid": "M2020013"
                        }
                    }
                }

            未查到结果：
                 string字段被拆分成两种新的数据类型: text用于全文搜索的,而keyword用于关键词搜索
                 text被分词， 大写字母全部转为了小写字母, pid类型为text类型, 导致查询不到

            使用keyword方式去查：

                body = {

                    "query": {
                        "term": {
                            "pid.keyword": "M2020013"
                        }
                    }
                }

            mapping:

                 {
                    "name": {
                        "type": "text"            # 使用'name'或'name.keyword' 均查不到
                    },
                    "nickname": {
                        "type": "keyword"        # 使用'nickname'能查到 或'nickname.keyword' 查不到
                    },
                    "cardname": {                # 使用'cardname'查不到 或'cardname.keyword' 能查到
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    }
                }

    3. 包含查询，match与multi_match

        查询条件进行分词，然后进行查询，多个词条之间是or的关系。
        对text类型的传，keyword字段未分词查询不到结果

        match:          xx = "yy"
        multi_match:    mm = "yy" 或 nn = "yy"

        eg: 查询名称中含有"爱"的影片

            body = {
                "query": {
                    "match": {
                        "movie_name": "爱"
                    }
                }
            }

        eg: 查询名称或pid中含有 "少年的你"的影片

             body = {
                "query": {
                    "multi_match": {
                        "query": "少年的你",
                        "fields": ["movie_name", "pid"]
                    }
                }
            }

        eg:
            name为text nickname为keyword类型
            "match": {
                "nickname": "zhang"          # 查不到结果 nickname为keyword类型
            }

            "match": {
                "name": "张"                 # 可查到结果
            }

            "match": {
                "name.keyword": "张"          # 查不到结果
            }

    4. ids: 多ids查询

        eg:
             body = {
                "query": {
                    "ids": {
                        "values": [
                            "AqEVEHsBQDBqZDWffMWs", "B6EVEHsBQDBqZDWffMWs"
                        ]
                    }
                }
            }

    5. 复合查询bool

        bool有3类查询关系，must(都满足),should(其中一个满足),must_not(都不满足)

        eg: 查询pid为GF2019150 且 source_type 为1 的影片

            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "pid.keyword": 'GF2019150'
                                }
                            },
                            {
                                "term": {
                                    'source_type': 1
                                }
                            }
                        ]
                    }
                }
            }

        eg: 查询pid为GF2019150 或 source_type 为2 的影片

             body = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "term": {
                                    "pid.keyword": 'GF2019150'
                                }
                            },
                            {
                                "term": {
                                    'source_type': 2
                                }
                            }
                        ]
                    }
                }
            }

        eg:
            {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                "name": "zhangsan"
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "match": {
                                "age": "40"
                                }
                            }
                        ],
                        "should": [
                            {
                                "match": {
                                "sex": "男"
                                }
                            }
                        ]
                    }
                }
            }

    6. 范围查询: range

        gt, gte, lt, lte

        eg: 查询 开始时间在2019-10-25 和 2019-12-25 之间的影片

           body = {
                "query": {
                    "range": {
                        "movie_start_time": {
                            "gte": "2019-10-25",  # >=
                            "lte": "2019-12-25"   # <=
                        }
                    }
                }
           }

    7. 前缀查询: prefix

        eg:
              body = {
                "query": {
                    "prefix": {
                        "pid.keyword": "YP"
                    }
                }
            }

    8. 通配符查询: wildcard

        EX:
             body = {
                "query": {
                    "wildcard": {
                        "pid": "*2019*"
                    }
                }
            }

    9. 排序 sort

        body = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {
                    "source_type": {
                        "order": "desc"
                    }
                },
                {
                    "pid.keyword": {
                        "order": "asc"
                    }
                }

            ]
        }

    10. 获取指定字段

        # 只需要获取_id数据,多个条件用逗号隔开
        es.search(index="index_name",doc_type="type_name",filter_path=["hits.hits._id"])

        # 获取所有数据
        es.search(index="index_name",doc_type="type_name",filter_path=["hits.hits._*"])

        # 获取_source中指定字段

            {
              "_source": {
                "includes": ["nickname", "age"],      想要显示的字段
                "excludes": ["name", "sex"]           不想要显示的字段
              },
              "query": {
                "terms": {
                  "nickname": ["zhangsan"]
                }
              }
            }

    11. 统计 count

        es.count(index="index_name",doc_type="type_name")

    12. 查看索引数据是否存在


        es.exists(index="index_name",doc_type="type_name", id=1)

    13. 聚合查询：

         {
                "aggs":{
                  "聚合后的别名":{
                    "聚合函数":{"field":"字段"}
                  }
                },
                "size":0
         }

         返回值:
            {
                "hits": {
                    "total": 77626,
                    "max_score": 0,
                    "hits": []
                },
                "aggregations": {
                    "聚合后的别名": {
                        "value": 值
                    }
                }
            }

        对某个字段取最大值max：

            "max_age":{
                    "max":{"field":"age"}
                  }

        对某个字段取最小值min：

            "min_age":{
                "min":{"field":"age"}
              }

        对某个字段求和sum:

            "sum_age":{
                "sum":{"field":"age"}
              }

        对某个字段取平均值avg:

            "avg_age":{
                "avg":{"field":"age"}
              }

        对某个字段的值进行去重之后再取总数:

             "distinct_age":{
                "cardinality":{"field":"age"}
              }

    14. state聚合

        stats聚合，对某个字段一次性返回count，max，min，avg和sum五个指标

            {
                "aggs":{
                  "stats_age":{
                    "stats":{"field":"age"}
                  }
                },
                "size":0
            }

    15. 桶聚合查询（group by）

        text类型的字段不能进行分组

        terms聚合，分组统计

            传参：

                {
                    "aggs":{
                      "owne_groupby":{
                        "terms":{"field":"server_owner"}
                      }
                    },
                    "size":0
                }

            返回值：
                {
                    "took": 78,
                    "timed_out": false,
                    "_shards": {},
                    "hits": {
                        "total": 77626,
                        "max_score": 0,
                        "hits": []
                    },
                    "aggregations": {
                        "owne_groupby": {
                            "doc_count_error_upper_bound": 0,
                            "sum_other_doc_count": 0,
                            "buckets": [
                                {
                                    "key": 1,
                                    "doc_count": 69717
                                },
                                {
                                    "key": 3,
                                    "doc_count": 7810
                                },
                                {
                                    "key": 2,
                                    "doc_count": 99
                                }
                            ]
                        }
                    }
                }

        在terms分组下再聚合

            传参：

                {
                    "aggs":{
                      "owne_groupby":{
                        "terms":{"field":"server_owner"},
                        "aggs":{
                          "sum_owner":{
                            "sum":{"field":"server_owner"}
                      }
                    }
                      }
                    },
                    "size":0
                }

            返回值：

                 "buckets": [
                        {
                            "key": 1,
                            "doc_count": 69717,
                            "sum_owner": {
                                "value": 69717
                            }
                        },
                        {
                            "key": 3,
                            "doc_count": 7810,
                            "sum_owner": {
                                "value": 23430
                            }
                        },
                        {
                            "key": 2,
                            "doc_count": 99,
                            "sum_owner": {
                                "value": 198
                            }
                        }
                    ]

        

    """

    def __init__(self, es_config, index_name="_doc", type_name=None):
        """
        :param es_config:
        :param index_name: 索引名称
        :param type_name: 索引类型

        es_config = {
            "hosts": ["127.0.0.1:9200"],
            "timeout": 5,
            "sniff_on_start": True,                 # 连接前测试
            "sniff_on_connection_fail": True,       # 节点无响应时刷新节点
            "sniff_timeout": 5,                     # 设置超时时间
            "max_retries": 3,                       # 重连次数
            "http_auth": ("user", "pwd")            # 账号和密码
        }

        """
        self.index_name = index_name
        self.type_name = type_name
        self.es = None

        try:

            self.es = Elasticsearch(**es_config)
        except Exception:
            traceback.print_exc()
        finally:
            if not (self.es and self.es.ping()):
                raise Exception('connect failed!')

        # print(self.es.info())

    @staticmethod
    def pageinfo(page=1, pagesize=20, total=0):
        page = int(page)
        if page <= 0:
            page = 1

        pagesize = int(pagesize)
        if pagesize <= 0:
            pagesize = 20

        total = int(total)
        totalpage = abs(((-1) * total) // pagesize)
        if page > totalpage > 0:
            page = totalpage

        offset = (page - 1) * pagesize
        d = {
            "page": page,
            "pagesize": pagesize,
            "offset": offset,
            "total": total,
            "first": 1,
            "prev": page - 1 if (page > 1) else 1,
            "next": page + 1 if (page < totalpage) else totalpage,
            "last": totalpage
        }
        pagination = []
        i = -4
        while i < 5:
            if 1 <= page + i <= totalpage:
                pagination.append(page + i)
            i = i + 1
        d["links"] = pagination

        return d

    def get_conn(self, retry=3):

        es = None

        for i in range(retry):

            try:

                es = Elasticsearch(["127.0.0.1:9200"])

                if es.ping():
                    break

            except Exception as e:

                traceback.print_exc()

        if not (es and es.ping()):

            raise Exception('connect failed!')

        return es

    def get_index_type(self, index_name=None, type_name=None):

        index_name = index_name if index_name else self.index_name
        doc_type = type_name if type_name else self.type_name

        return index_name, doc_type

    def create_index_v6(self, index_name=None, index_type=None):
        """

        设置keyword： https://blog.csdn.net/weixin_38617363/article/details/87914474
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param index_name:
        :param index_type:
        :return:

         {
            "mappings": {
                "movie": {
                    "properties": {
                        "invalid": {
                            "type": "long"
                        },
                        "movie_end_time": {
                            "type": "date"
                        },
                        "movie_name": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "movie_start_time": {
                            "type": "date"
                        },
                        "pid": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "source_type": {
                            "type": "long"
                        },
                        "status": {
                            "type": "long"
                        }
                    }
                }
            }
        }
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        # 创建映射
        _index_mappings = {
            "mappings": {
                doc_type: {
                    "properties": {
                        "title": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "date": {
                            "type": "text",
                            "index": True
                        },
                        "keyword": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "source": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "link": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }

            }
        }
        if self.es.indices.exists(index=index) is not True:

            self.es.indices.create(index=index, body=_index_mappings)

        return True

    def create_index_v7(self, index_name=None):
        """
        创建索引 Elasticsearch 7.X中, Type的概念已经被删除了 默认_doc
        :param index_name:
        :param index_type:
        :return:
        """

        index, _ = self.get_index_type(index_name, None)

        # 创建映射

        _index_mappings = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "index": True
                    },
                    "date": {
                        "type": "text",
                        "index": True
                    },
                    "source": {
                        "type": "long",
                        "index": False
                    }
                }

                }
        }

        if self.es.indices.exists(index=index) is not True:
            self.es.indices.create(index=index, body=_index_mappings)

        return True

    def delete_index(self, index_name):
        """
        删除Index
        :param index_name:
        :return:
        """

        res = self.es.indices.delete(index=index_name, ignore=[400, 404])

        return res

    def get_data(self, e_id=None, doc=None, index_name=None, index_type=None):
        """
        获取数据
        :param e_id:
        :param doc:
        :param index_name:
        :param index_type:
        :param

        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        if e_id:

            # 唯一查询
            try:
                response_data = self.es.get(index=index, doc_type=doc_type, id=e_id)
            except Exception:
                traceback.print_exc()
                # id不存在, 会报错
                response_data = {}

            return 1, response_data

        elif doc:

            # 条件查询 filter_path 指定获取字段
            # response_data = self.es.search(index=index, doc_type=doc_type, body=doc,
            #                                filter_path=["hits.hits._id", "hits.hits._source"])

            response_data = self.es.search(index=index, doc_type=doc_type, body=doc)

        else:

            # 全量查询
            response_data = self.es.search(index=index, doc_type=doc_type)

        total_count = response_data['hits']['total']['value']
        list(map(lambda v: v['_source'].update({"id": v["_id"]}), response_data['hits']['hits']))
        response_data = [v['_source'] for v in response_data['hits']['hits']]

        return total_count, response_data

    def bulk_get_data(self, index_name=None, index_type=None, page_size=2):
        """
        批量读取数据
        借助游标，将所有结果数据存储到内存中
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        query_json = {
            "query": {
                "match_all": {}
            }
        }

        query = self.es.search(index=index, doc_type=doc_type, body=query_json, scroll='5m', size=page_size)

        results = query['hits']['hits']        # es查询出的结果第一页
        total = query['hits']['total']         # es查询出的结果总量
        scroll_id = query['_scroll_id']        # 游标用于输出es查询出的所有结果

        page_num = int(total / page_size)

        for i in range(0, page_num + 1):

            query_scroll = self.es.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']

            results += query_scroll

        return results

    def page_get_data(self, doc=None, index_name=None, index_type=None, page=2, pagesize=5):
        """
        分页查询
        :param doc:
        :param index_name:
        :param index_type:
        :param page:
        :param pagesize:
        :return:
        """
        index, doc_type = self.get_index_type(index_name, index_type)

        if not doc:

            doc = {
                "query": {
                    "match_all": {}
                }
            }

        response_data = self.es.search(index=index, doc_type=doc_type, body=doc)
        total_count = response_data['hits']['total']['value']

        page_info = self.pageinfo(page, pagesize, total_count)

        doc.update({
            "from": page_info["offset"],
            "size": page_info["pagesize"]
        })

        response_data = self.es.search(index=index, doc_type=doc_type, body=doc)
        list(map(lambda v: v['_source'].update({"id": v["_id"]}), response_data['hits']['hits']))
        response_data = [v['_source'] for v in response_data['hits']['hits']]

        return page_info, response_data

    def aggregate_get_data(self, doc=None, index_name=None, index_type=None):
        """
        聚合查询
        :param doc:
        :param index_name:
        :param index_type:
        :return:
        """
        agg_data = {}

        if doc.get("aggs"):

            index, doc_type = self.get_index_type(index_name, index_type)

            response_data = self.es.search(index=index, doc_type=doc_type, body=doc)

            agg_data = {k: v['value'] if v.get('value') else v for k, v in response_data['aggregations'].items()}

        return agg_data

    def bucket_get_data(self, doc=None, index_name=None, index_type=None):
        """
        桶查询  类似MySQL的group by
        :param doc:
        :param index_name:
        :param index_type:
        :return:
        """

        bucket_data = []

        if doc.get("aggs"):

            index, doc_type = self.get_index_type(index_name, index_type)

            response_data = self.es.search(index=index, doc_type=doc_type, body=doc)

            bucket_data = response_data['aggregations']['age_groupby']['buckets']

        return bucket_data

    def append_data(self, info, index_name=None, index_type=None):
        """
        添加数据
        :param info:
            {
                "date": "2017-09-13",
                "source": "慧聪网",
                "link": "https://www.baidu.com/",
                "keyword": "电视",
                "title": "付费 电视 行业面临的转型和挑战"
            }
        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        response = self.es.index(index=index, doc_type=doc_type, body=info)

        return response['_id']

    def bulk_insert_data(self, info, index_name=None, index_type=None):
        """
        批量添加
        :param info: []
        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        es_info = [{"_index": index, "_type": doc_type, "_source": v} for v in info]

        success_count, _ = bulk(self.es,  es_info, index=index, raise_on_error=True)

        return success_count

    def update_date(self, info, e_id=None, index_name=None, index_type=None):
        """
        更新
        :param e_id:
        :param info: doc 或者 script 变量来指定修改的内容

            eg:修改某条数据
                {
                    "doc": {
                        'images': 'https://www.xiaomi.com/xmdn.jpg'
                    }
                }

            eg:更新符合条件的数据

                 body = {
                    "query": {                              # 查询的条件
                        "term": {
                            '_id': 'Tqz3DoABy32hvzomcW-w',
                        }
                    },
                    "script": {                            # 更新的内容
                        "inline": "ctx._source.category = params.category; ctx._source.images=params.images",  # 要执行的变更
                        "params": {
                            "category": "XiaoMi",
                            "images": 'https://www.xiaomi.com/xmtest.jpg'

                        },
                        "lang": "painless"                          # 当前脚本的语言
                    }
                }

        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        updated_rows = 0

        if e_id:
            # 根据唯一标识变更, 并不存在的文档会报错
            try:
                if info.get("doc"):
                    self.es.update(index=index, doc_type=doc_type, id=e_id, body=info)
                else:
                    # 覆盖原内容
                    self.es.index(index=index, doc_type=doc_type, id=e_id, body=info)
                updated_rows = 1
            except Exception:
                traceback.print_exc()
                pass

        else:
            # 更新符合条件的数据
            response_data = self.es.update_by_query(index=index, doc_type=doc_type, body=info)

            updated_rows = response_data["total"]

        return updated_rows

    def delete_data(self, e_id=None, query_info=None, index_name=None, index_type=None):
        """
        删除数据
        :param e_id:
        :param query_info: 匹配条件
            eg:
                {
                    "query":{
                        "match":{
                          "source": "慧聪网"
                        }
                    }
                }
        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        # 删除的个数

        updated_rows = 0

        if e_id:
            # 唯一性标识删除, 并不存在的文档会报错
            try:
                self.es.delete(index=index, doc_type=doc_type, id=e_id)
                updated_rows = 1
            except Exception:
                pass

        elif query_info:
            # 条件删除
            response_data = self.es.delete_by_query(index=index, doc_type=doc_type, body=query_info)

            updated_rows = response_data['total']

        return updated_rows


if __name__ == "__main__":

    # _index = "cinema_hall"
    # _type = "_doc"
    # _ip = "10.210.10.214"

    config = {
        "hosts": ["127.0.0.1:9200"],
        "timeout": 5,
        "sniff_on_start": True,                    # 连接前测试
        "sniff_on_connection_fail": True,          # 节点无响应时刷新节点
        "sniff_timeout": 60,                       # 设置超时时间
        "max_retries": 3,                          # 重连次数
        "http_auth": ("user", "pwd")               # 账号和密码
    }

    _index = "shopping"
    _type = "phone"

    application = ElasticObj(config, index_name='shopping')

    # doc = {
    #     "query": {
    #         "wildcard": {
    #                     "nickname": "*s*"
    #                 }
    #     }
    # }

    #

    body = {
                "from": 6,
                "size": 5,
                "query": {

                     "match_all": {}
                }
            }
    count, ret = application.get_data(doc=body)
    print(count, ret)   # UKz4DoABy32hvzom4m-_

    page_ifno, ret = application.page_get_data()
    print(page_ifno, ret)

    # {'title': '小米电脑', 'category': '小米', 'images': 'https://www.xiaomi.com/xm.jpg', 'price': 3000.0, 'id': 'IqyFDIABy32hvzomFW-v'}


    # a = {'title': '小米MiNi', 'category': '小米', 'images': 'http://www.gulixueyuan.com/xm.jpg', 'price': 2888.0,
    #      "describe": None, 'create_date': "2022-02-22"
    #  }
    # application.append_data(a)



    # ret = application.create_index_v7("test", "_doc")
    #
    # print(ret)

    # body = {
    #     "query": {
    #         "terms": {
    #             "movie_end_time": ["2021-02-20", "2020-01-23"]
    #         }
    #     }
    # }

    # body = {
    #     "query": {
    #         "term": {
    #             "pid.keyword": "YP1912200001",
    #         }
    #     },
    #     "script": {
    #         "inline": "ctx._source.movie_start_time = '2019-12-25'; ctx._source.movie_end_time='2020-01-25'"
    #     }
    # }
    #
    # ret = application.bulk_get_data()
    # print(ret)
    # print(len(ret))

