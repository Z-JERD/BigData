# Hadoop

## Hadoop组成:

    1. HDFS（数据存储）

        HDFS原理：

            https://juejin.cn/post/6844904080272277517

        图解HDFS:

            https://juejin.cn/post/6844903949569359880

    2. Yarn（资源调度）

        https://juejin.cn/post/7011365385098231816

        https://zhuanlan.zhihu.com/p/141220207

    3. MapReduce（计算）

        https://juejin.cn/post/6890403796938129415

    4. Common（辅助工具）




## Hadoop安装：

    https://juejin.cn/post/6844903608568250376#heading-9
    https://www.cnblogs.com/hello-/articles/9600269.html

    Hadoop 50070端口无法访问：

        https://ask.hellobi.com/blog/tianshanbpf/14344

    启动/停止 Hadoop:

        sbin/start-dfs.sh
        sbin/stop-dfs.sh

    是否启动成功：

        http://10.210.10.214:50070/

## centos7 hadoop 集群安装配置：

    https://juejin.cn/post/6844903608631328776#heading-2

## hdfs dfs常用命令的使用：

    https://blog.csdn.net/WQY992/article/details/89002269

# HIVE

## Hive安装：

    https://juejin.cn/post/6844903949766492167
    https://zhuanlan.zhihu.com/p/326901148
    https://www.cnblogs.com/lyt010/p/12865764.html

    启动Hive报错：

        JDK版本不兼容：
            https://blog.csdn.net/lezeqe/article/details/102681203

    启动HIVE:

        cd /usr/local/hive/bin
        hive

        查看当前使用的数据库：

            hive> select current_database();

## Dbeaver连接Hive

    https://blog.csdn.net/weixin_34116110/article/details/91928290

    https://blog.csdn.net/DFZR_ZXHY/article/details/106172288

    root is not allowed to impersonate root：

        https://www.cnblogs.com/lijinze-tsinghua/p/8563054.html

    Hive驱动问题：

        https://www.icode9.com/content-4-614418.html


## HIVE SQL:

    https://juejin.cn/post/6946169491143262238

    https://juejin.cn/post/6934324080917086221

## 操作示例:

### COMMENT 中文乱码

    https://www.cnblogs.com/qingyunzong/p/8724155.html

### 创建表结构:

        CREATE  TABLE IF NOT EXISTS `cubor_chain`(
            `cinema_name`       string  comment '影院名称',
            `cinema_code`       int     comment '影院编码',
            `movie_name`       string   comment '影片名称',
            `movie_edition`    string   comment '影片版本',
            `movie_code`       string   comment '排次号',
            `hall_name`        string   comment '影厅名称',
            `shows`             int     comment '场次',
            `audience`          int     comment '人次',
            `revenue`           int     comment '票房',
            `show_date`         date    comment '放映日期',
            `device`            int     comment '设备归属 1:自购 2 租赁'
        )
        COMMENT '票房统计'
        ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

### 导入表数据：

    通过文件：

        load data local inpath '/root/tianhongyingye.csv' into table cubor_chain;

    通过SQL：


        insert into table  cubor_chain values
            ("菏泽魔影影城电影院",37147141,"夺冠","普通","001100062020",1,1,0,0, "2020-01-24",2),
            ("菏泽魔影影城电影院",37147141,"信念一生","普通","001100152020",1,1,50,2500, "2020-08-21",2);

## 分桶：

    Hive 的分桶采用对分桶字段的值进行哈希，然后除以桶的个数求余的方式决定该条记录存放在哪个桶当中


    创建表结构：
        CREATE  TABLE IF NOT EXISTS `hall_buck`(
            `seats`             int     comment  '座位数',
            `manufactures`      string  comment  '服务器品牌',
            `model`             string  comment  '放映机品牌',
            `cinema_code`       int     comment '影院编码',
            `cinema_name`       string  comment '影院名称',
            `chain`             string  comment '院线',
            `sheng`             string  comment  '省',
            `shi`               string  comment   '市'
        )
        COMMENT '影厅统计'
        clustered by(cinema_code)
        into 4 buckets
        ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

    导入数据：

        load data local inpath '/usr/sft/data_demo/hall_buck.csv' into table hall_buck;

## 分区:
        创建表结构：
                CREATE  TABLE IF NOT EXISTS `hall_part`(
                    `seats`             int     comment  '座位数',
                    `manufactures`      string  comment  '服务器品牌',
                    `model`             string  comment  '放映机品牌',
                    `cinema_code`       int     comment '影院编码',
                    `cinema_name`       string  comment '影院名称',
                    `chain`             string  comment '院线',
                    `sheng`             string  comment  '省',
                    `shi`               string  comment   '市'
                )
                COMMENT '影厅统计'
                partitioned by (province int)
                ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

        导入数据：

            load data local inpath '/usr/sft/data_demo/hall_buck_320000.csv' into table hall_part partition(province=320000);
            load data local inpath '/usr/sft/data_demo/hall_buck_410000.csv' into table hall_part partition(province=410000);

## 查询结果导出本地
   
    hive(default)>insert overwrite local directory
    '/usr/sft/data_demo'
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    select * from hall_part;





