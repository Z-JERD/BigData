
# Es的数据格式
    
    Index:     相当于一个库

    Types:     相当于表

    Documents: 相当于表的行

    Fields:    相当于列
    
    Elasticsearch 5.x	支持多种type
    Elasticsearch 6.X中, 一个index下已经只能包含一个type
    Elasticsearch 7.X中, Type的概念已经被删除了默认类型为：_doc）

# Es的访问
    
    http://localhost:9200
    
    9200端口: 浏览器访问的http协议RESTful端口
    9300端口: Elasticsearch集群间组件的通信端口

# Es索引
    
## 1.创建索引
    
    向ES服务器发PUT请求: http://127.0.0.1:9200/shopping

    索引分片数:
        7.0.0-: 默认5片
        7.0.0+: 默认1片
    
    重复添加索引，会返回错误信息

## 2.查看所有索引
    
    向ES服务器发GET请求: http://127.0.0.1:9200/_cat/indices?v

## 3.查看单个索引
    
    向ES服务器发GET请求 ：http://127.0.0.1:9200/shopping

## 4.删除索引
    
    向ES服务器发DELETE请求 ：http://127.0.0.1:9200/shopping

# 映射操作

    类似于数据库(database)中的表结构(table)

## 创建映射
    
    向ES服务器发PUT请求 ：http://127.0.0.1:9200/student/_mapping

    type：类型

        String类型，又分两种：
            text：可分词
            keyword：不可分词，数据会作为完整字段进行匹配
    
        Numerical：数值类型，分两类
            基本数据类型：long、integer、short、byte、double、float、half_float
            浮点数的高精度类型：scaled_float
        
        Date：日期类型
        
        Array：数组类型
        
        Object：对象

    index：是否索引
        
        默认为true，也就是说你不进行任何配置，所有字段都会被索引。
        
        true：字段会被索引，则可以用来进行搜索
        false：字段不会被索引，不能用来搜索

    store：是否将数据进行独立存储，默认为false

    analyzer：分词器

    eg：
        请求体内容为：
            {
              "properties": {
                "name":{
                  "type": "text",
                  "index": true
                },
                "sex":{
                  "type": "text",
                  "index": false
                },
                "age":{
                  "type": "long",
                  "index": false
                },
                "nick_name":{
                  "type": "keyword",
                  "index": true
                }
              }
            }

## 查看映射
    
    向ES服务器发GET请求 ：http://127.0.0.1:9200/student/_mapping

# 文档操作

## 创建文档

    向ES服务器发POST请求 ：http://127.0.0.1:9200/shopping/_doc
    请求体内容为：
        {
            "title":"小米手机",
            "category":"小米",
            "images":"http://www.gulixueyuan.com/xm.jpg",
            "price":3999.00
        }

    默认情况下，ES服务器会随机生成一个"_id"

    要自定义唯一性标识，需要在创建时指定：http://127.0.0.1:9200/shopping/_doc/fc11a3fb95ef4

## 查看文档
    
    需要指明文档的唯一性标识

    向ES服务器发GET请求 ：http://127.0.0.1:9200/shopping/_doc/1

    res:
        {
            "_index": "shopping",
            "_type": "_doc",
            "_id": "IqyFDIABy32hvzomFW-v",           # 唯一标识
            "_version": 1,
            "_seq_no": 0,
            "_primary_term": 1,
            "found": true,                          # 查询结果   false表示未查找到不会有_source信息
            "_source": {                            # 文档源信息
                "title": "小米手机",
                "category": "小米",
                "images": "http://www.gulixueyuan.com/xm.jpg",
                "price": 3999
            }
        }

## 修改文档

    覆盖原有的数据内容：

        向ES服务器发POST请求 ：http://127.0.0.1:9200/shopping/_doc/1

        eg：

            {
                "title":"华为手机",
                "category":"华为",
                "images":"http://www.gulixueyuan.com/hw.jpg",
                "price":4999.00
            }

    修改某数据的局部信息：

        向ES服务器发POST请求 ：http://127.0.0.1:9200/shopping/_update/1

        eg:

            { 
              "doc": {
                "price":3000.00
              } 
            }

## 删除文档

    唯一性标识删除:
        
        向ES服务器发DELETE请求 ：http://127.0.0.1:9200/shopping/_doc/1
    
    条件删除：
        
        向ES服务器发POST请求 ：http://127.0.0.1:9200/shopping/_delete_by_query

        eg:
            {
              "query":{
                "match":{
                  "price":4000.00
                }
              }
            }

# 高级查询
    
    1. 查询所有文档: match_all

    2. 匹配查询: match和multi_match

        对text字段分词匹配, 类似mysql的like %xx%
    
        multi_match可以在多个字段中查询

    3. 精确查询: term和terms

        精确的关键词匹配查询，不对查询条件进行分词
        
        terms允许指定多值进行匹配，这个字段包含了指定值中的任何一个值，那么这个文档满足条件

    4. 前缀查询: prefix

        类似: like xx%

    5. 通配符查询: wildcard
        类似: like %xx%

    6. 组合查询：bool
        
        把`must`（必须 ）、`must_not`（必须不）、`should`（应该）的方式进行组合

    7. 范围查询：
        
        gt	大于>
        gte	大于等于>=
        lt	小于<
        lte	小于等于<=

    8. 排序查询: sort

    9. 分页查询: from size

    10. 聚合查询: aggs
        
        max，min，avg, sum, cardinality(对某个字段去重后取总数)

        stats聚合，对某个字段一次性返回count，max，min，avg和sum五个指标

    11. 桶查询：
        
        桶聚和相当于sql中的group by语句

        terms聚合，分组统计

        在terms分组下再聚合

        text类型的字段不能进行分组

    12. 指定字段查询

        默认情况下，Elasticsearch在搜索的结果中，会把文档中保存在_source的所有字段都返回

        添加_source的过滤：

            includes：来指定想要显示的字段
            excludes：来指定不想要显示的字段

# 倒排索引：

## 倒排索引原理：
	
	倒排索引是per field的，一个字段有一个自己的倒排索引

	term：                每个字段去重后的值
	posting list：        int的数组，存储了所有符合某个term的文档id
	term dictionary：     排序后的term（可以用二分查找的方式，用 logN 次磁盘查找得到目标）
	term index：          term index是一棵t树，包含的是term的一些前缀

	eg：

		查询过滤条件age=18 的过程：
			
			1. 先从term index找到18在term dictionary的大概位置

			2. 从term dictionary里精确地找到18这个term，然后得到一个posting list

## ES比MySQL快的原因：
	
	Mysql只有term dictionary这一层。检索一个term需要若干次的random access的磁盘操作。

	ES在term dictionary的基础上添加了term index来加速检索，term index以树的形式缓存在内存中。
    从term index查到对应的term dictionary的block位置之后，再去磁盘上找term，大大减少了磁盘的random access次数

# Es的排序

# Es的集群

## 集群的概念和特点：
    
    概念：由一个或多个服务器节点组织在一起，共同持有整个的数据，并一起提供索引和搜索功能。
    
    特点：集群有一个唯一的名字标识，这个名字默认就是”elasticsearch”。一个节点只能通过指定某个集群的名字，来加入这个集群。

## 节点Node 
    
    一个节点就是其中的一个服务器，默认情况下，每个节点都会被安排加入到一个叫做“elasticsearch”的集群中


# Es的分片

## 分片的概念
    一个具有10亿文档数据的索引占据1TB的磁盘空间，而任一节点都可能没有这样大的磁盘空间。
    
    Elasticsearch提供了将索引划分成多份的能力，每一份就称之为分片。
    
    当创建一个索引的时候，可以指定你想要的分片的数量。每个分片本身也是一个功能完善并且独立的“索引”，这个“索引”可以被放置到集群中的任何节点上。

## 分片的作用
    
    1. 允许你水平分割 / 扩展你的内容容量

    2. 允许你在分片之上进行分布式的、并行的操作，进而提高性能/吞吐量

## 索引与分片的关系
    Elasticsearch索引是分片的集合。 当Elasticsearch在索引中搜索的时候， 他发送查询到每一个属于索引的分片(Lucene 索引)，
    然后合并每个分片的结果到一个全局的结果集

# Es的副本

## Es副本的概念

    某个分片/节点可能随时宕机, 为了实现故障转移, Elasticsearch允许你创建分片的一份或多份拷贝，这些拷贝叫做复制分片(副本)。

## 副本的作用
    
    1. 在分片/节点失败的情况下，提供了高可用性
        复制分片从不与原/主要（original/primary）分片置于同一节点上是非常重要的。
        同一个节点上既保存原始数据又保存副本是没有意义的，因为一旦失去了那个节点，我们也将丢失该节点上的所有副本数据。
   
    2. 扩展你的搜索量/吞吐量，因为搜索可以在所有的副本上并行运行

## 默认分片和副本
    
    默认情况下，Elasticsearch中的每个索引被分片1个主分片和1个复制，这意味着，如果你的集群中至少有两个节点

    每个索引总共就有2个分片。索引创建之后，可以在任何时候动态地改变复制的数量，但是你事后不能改变分片的数量

# 路由计算

## 当创建文档时，如何决定这个文档应当被存储在分片1还是分片2中呢？

    routing 是一个可变值，默认是文档的 _id ，也可以设置成一个自定义的值。 
    routing 通过 hash 函数生成一个数字，然后这个数字再除以 number_of_primary_shards （主分片的数量）后得到余数 。
    这个分布在 0 到 number_of_primary_shards-1 之间的余数，就是我们所寻求的文档所在分片的位置。

## 为什么我们要在创建索引的时候就确定好主分片的数量 并且永远不会改变这个数量：
    因为如果数量变化了，那么所有之前路由的值都会无效，文档也再也找不到了

# Es读写流程

## 写流程
    
    写操作， 必须在主分片上面完成之后才能被复制到相关的副本分片

    1. 客户端向 Node 1 发送新建、索引或者删除请求
    
    2. 节点使用文档的 _id 确定文档属于分片 0 。请求会被转发到 Node 3，因为分片 0 的主分片目前被分配在 Node 3 上

    3. Node3在主分片上面执行请求。如果成功了，它将请求并行转发到 Node 1 和 Node 2 的副本分片上。
       一旦所有的副本分片都报告成功, Node 3 将向协调节点报告成功，协调节点向客户端报告成功

## 读流程
    
    从主分片或者从其它任意副本分片检索文档

    1. 客户端向 Node 1 发送获取请求

    2. 节点使用文档的 _id 来确定文档属于分片 0 。分片 0 的副本分片存在于所有的三个节点上。 在这种情况下，它将请求转发到 Node 2 

    3. Node 2 将文档返回给 Node 1 ，然后将文档返回给客户端

    在处理读取请求时，协调结点在每次请求的时候都会通过轮询所有的副本分片来达到负载均衡。

    在文档被检索时，已经被索引的文档可能已经存在于主分片上但是还没有复制到副本分片。 
    在这种情况下，副本分片可能会报告文档不存在，但是主分片可能成功返回文档

## 更新流程

    1.客户端向 Node 1 发送更新请求。

    2.它将请求转发到主分片所在的 Node 3 

    3.Node 3 从主分片检索文档，修改 _source 字段中的 JSON ，并且尝试重新索引主分片的文档。 
      如果文档已经被另一个进程修改，它会重试步骤 3 ，超过 retry_on_conflict 次后放弃。

    4.如果 Node 3 成功地更新文档，它将新版本的文档并行转发到 Node 1 和 Node 2 上的副本分片，重新建立索引。
      一旦所有副本分片都返回成功， Node 3 向协调节点也返回成功，协调节点向客户端返回成功。

    当主分片把更改转发到副本分片时， 它不会转发更新请求。 相反，它转发完整文档的新版本
    
# 文档分析

    分析器实际上是将三个功能封装到了一个包里

## 分析器的功能

### 字符过滤器
    
    字符串按顺序通过每个字符过滤器 。他们的任务是在分词前整理字符串。一个字符过滤器可以用来去掉HTML，或者将 & 转化成 and

### 分词器

    字符串被分词器分为单个的词条。一个简单的分词器遇到空格和标点的时候，可能会将文本拆分成词

### Token过滤器
    
    这个过程可能会改变词条（例如，小写化 Quick ），删除词条（例如， 像 a， and， the 等无用词），或者增加词条（例如，像 jump 和 leap 这种同义词）。

## 分析器的种类
### 标准分析器
    Elasticsearch默认使用的分析器,它根据 Unicode联盟定义的单词边界划分文本, 删除绝大部分标点。最后，将词条小写
### 简单分析器
    在任何不是字母的地方分隔文本，将词条小写
### 空格分析器
    空格分析器在空格的地方划分文本

### IK中文分词器
    ES的默认分词器无法识别中文测试