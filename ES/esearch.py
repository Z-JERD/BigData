import traceback

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticObj:

    # 查询方式

    """
    body查询：

    分页： from、size，from  从第几条数据开始展示，size 一页展示多少条数据

    1. 查询全部: match_all

        EX:
            {"query": {"match_all": {}}}

        EX:

             body = {
                "from": 1,
                "size": 5,
                "query": {

                     "match_all": {}
                }
            }

    2. 等于查询: term与terms

        term、terms查询，它并不知道分词器的存在，这种查询适合keyword、numeric、date等明确值的

        term: 查询 xx = "xx"
        terms: 查询 xx = "xx" 或 xx = "yy"

        EX: 查询 movie_start_time 等于 2020-12-11的值

             body = {
                "query": {
                    "term": {
                        "movie_start_time": "2020-12-11"
                    }
                }
            }

        EX: 查询movie_end_time的值为2021-02-20或2020-01-23的值

            body = {
                "query": {
                    "terms": {
                        "movie_end_time": ["2021-02-20", "2020-01-23"]
                    }
                }
            }

        EX: 查询pid为M2020013的数据

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

    3. 包含查询，match与multi_match

        match:          xx = "yy"
        multi_match:    mm = "yy" 或 nn = "yy"

        EX: 查询名称中含有"爱"的影片

            body = {
                "query": {
                    "match": {
                        "movie_name": "爱"
                    }
                }
            }

        EX: 查询名称或pid中含有 "少年的你"的影片

             body = {
                "query": {
                    "multi_match": {
                        "query": "少年的你",
                        "fields": ["movie_name", "pid"]
                    }
                }
            }

    4. ids: 多ids查询

        EX:
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

        EX: 查询pid为GF2019150 且 source_type 为1 的影片

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

        EX: 询pid为GF2019150 或 source_type 为2 的影片

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

    6. 范围查询: range

        EX: 查询 开始时间在2019-10-25 和 2019-12-25 之间的影片

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

        EX:
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

    def __init__(self, index_name, index_type="_doc", ip="127.0.0.1", port=9200, user=None, pwd=None):
        """
        :param index_name: 索引名称
        :param index_type: 索引类型
        :param ip::
        :param port
        :param user:
        :param pwd:
        """
        self.index_name = index_name
        self.index_type = index_type
        self.addr = ip
        self.port = port
        self.user = user
        self.pwd = pwd

        self.es = self.get_conn()

    def get_conn(self, retry=3, timeout=60):

        es = None

        for i in range(retry):

            try:

                if self.user and self.pwd:
                    es = Elasticsearch([self.addr], http_auth=(self.user, self.pwd), port=self.port, sniff_timeout=timeout)
                else:
                    es = Elasticsearch([self.addr],  port=self.port, sniff_timeout=timeout)

                if es.ping():
                    break

            except Exception as e:

                traceback.print_exc()

        if not es.ping():

            raise Exception('connect failed!')

        return es

    def get_index_type(self, index_name=None, index_type=None):

        index = index_name if index_name else self.index_name
        doc_type = index_type if index_type else self.index_type

        return index, doc_type

    def create_index(self, index_name=None, index_type=None):
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

    def create_index_v7(self, index_name=None, index_type=None):
        """
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

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
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        if e_id:

            res = self.es.get(index=index, doc_type=doc_type, id=e_id)

            return res

        elif doc:

            res = self.es.search(index=index, doc_type=doc_type, body=doc,
                                 filter_path=["hits.hits._id", "hits.hits._source"])

        else:

            res = self.es.search(index=index, doc_type=doc_type)

        return res['hits']['hits']

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

    def append_data(self, info, index_name=None, index_type=None):
        """
        添加数据
        :param info:
            {"date": "2017-09-13",
             "source": "慧聪网",
             "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
             "keyword": "电视",
             "title": "付费 电视 行业面临的转型和挑战"
             }
        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        res = self.es.index(index=index, doc_type=doc_type, body=info)

        return res

    def bulk_data(self, info, index_name=None, index_type=None):
        """
        批量添加
        :param info: []
        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        es_info = [{"_index": index, "_type": doc_type, "_source": v} for v in info]

        success, _ = bulk(self.es,  es_info, index=index, raise_on_error=True)

        return success

    def update_date(self, info, e_id=None, index_name=None, index_type=None):
        """
        更新
        :param e_id:
        :param info: {
                        "doc":{
                            "movie_end_time":"2020-11-11"
                        }
                    }

            EX:

                 body = {
                    "query": {
                        "term": {
                            "pid.keyword": "YP1912200001",
                        }
                    },
                    "script": {
                        "inline": "ctx._source.movie_start_time = '2019-12-25'; ctx._source.movie_end_time='2020-01-25'"
                    }
                }

        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        if e_id:
            res = self.es.update(index=index, doc_type=doc_type, id=e_id, body=info)
        else:
            res = self.es.update_by_query(index=index, doc_type=doc_type, body=info)

        return res

    def delete_data(self, e_id=None, info=None, index_name=None, index_type=None):
        """
        删除数据
        :param e_id:
        :param info:
        :param index_name:
        :param index_type:
        :return:
        """

        index, doc_type = self.get_index_type(index_name, index_type)

        if e_id:

            res = self.es.delete(index=index, doc_type=doc_type, id=e_id)

        elif info:

            res = self.es.delete_by_query(index=index, doc_type=doc_type, body=info)

        else:

            res = True

        return res


if __name__ == "__main__":

    # _index = "cinema_hall"
    # _type = "_doc"
    # _ip = "10.210.10.214"

    _index = "shopping"
    _type = "phone"
    _ip = "10.210.10.214"

    application = ElasticObj(_index,  _type, _ip)

    ret = application.create_index_v7("test", "_doc")

    print(ret)

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









