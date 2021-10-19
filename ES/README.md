# 参考文档:


## JAVA配置:

    查找安装路径: 
        
        https://www.cnblogs.com/imyalost/p/8745137.html

    设置环境变量: 
        
        https://blog.csdn.net/zhpengfei0915/article/details/50963199

## ES安装:

    ES配置参考文档:
    
        https://blog.csdn.net/wsdc0521/article/details/106551273
    
    访问 ES：
    
        http://10.210.10.214:9200/
        
    历史版本下载:

        https://www.elastic.co/cn/downloads/past-releases
        
    Python操作ES参考文档:
    
        http://www.manongjc.com/detail/7-zfmlfwpwprrsvjn.html
        
## ES报错:
    
        https://blog.csdn.net/feng12345zi/article/details/80367907
        
        https://blog.51cto.com/u_10950710/2124131
        
        es6.8网页拒绝访问：
        
            config/elasticsearch.yml
        
                添加：network.bind_host: 0.0.0.0
        
        
        es7.8网页拒绝访问：
        
            config/elasticsearch.yml
        
                    添加：
        
                        network.host: 0.0.0.0
                        discovery.seed_hosts: ["127.0.0.1"]
                        cluster.initial_master_nodes: ["node-1"]
        
    
## ES集群

    https://zhuanlan.zhihu.com/p/258641792
    
    原理:

        https://www.cnblogs.com/shenlei-blog/p/13367269.html

        https://blog.csdn.net/sinat_16658263/article/details/90444038 
        
        
## Kibana的配置:
    
    参考文档：
        
         https://blog.csdn.net/k0307x1990y/article/details/103278538
         
    访问Kibana：
        
        http://10.210.10.214:5601

       

## Logstash配置:

        https://blog.csdn.net/bbwangj/article/details/80600698

        https://www.cnblogs.com/sunsing123/p/10912826.html


## elasticsearch-head插件:

        https://www.jianshu.com/p/528450d46e3c

        https://www.freesion.com/article/775958324/

        https://blog.51cto.com/u_2262805/2441992
  
/usr/lib/  
