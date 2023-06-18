# Docker安装MySQL5.7
	参考文档：https://blog.csdn.net/qq_42971035/article/details/127831101	
	
## 1. 拉取镜像
	docker pull mysql:5.7

## 2. 配置启动文件
	docker-compose.yml
	
## 3. 配置my.cnf
	docker-compose中配置的地址是：/usr/local/mysql/conf
	将my.conf放到此目录下

## 4. 设置MySQL授权远程登录
    1.mysql> use mysql
    2.mysql> grant all privileges on *.* to 'root'@'%' identified by '12345';
             使用root:12345来外部访问
    3.刷新权限:
        mysql> flush privileges;
		
# 主从配置
	参考文档：https://zhuanlan.zhihu.com/p/199217698
	
## 1.主机配置：
	
### 1. 主机创建从机用户
	使用命令行进入mysql：

	mysql> mysql -u root -p

	//192.168.0.106是slave从机的IP
	mysql> GRANT REPLICATION SLAVE ON *.* to 'root'@'192.168.0.101' identified by 'centos@123';
	//192.168.0.107是slave从机的IP
	mysql> GRANT REPLICATION SLAVE ON *.* to 'root'@'192.168.0.102' identified by 'centos@123';
	//刷新系统权限表的配置
	mysql> FLUSH PRIVILEGES;

### 2. 主机配置my.cnf
	[mysqld]
	server-id=104
	# 开启binlog
	log-bin=mysql-bin
	# 需要同步的数据库，如果不配置则同步全部数据库
	# binlog-do-db=test_db
	# binlog日志保留的天数，清除超过7天的日志
	expire-logs-days=7
	#设置二进制日志使用内存大小（事务）
	binlog_cache_size=1M  
	#设置使用的二进制日志格式（mixed,statement,row）
	binlog_format=mixed 
	
### 3. 重启mysql

### 4.查看当前binlog日志的信息
	mysql> show slave status \G;
	
## 2.从机配置：	

### 1. 配置my.cnf
	[mysqld]
	server-id=105
	# 开启binlog
	log-bin=mysql-slave1-bin
	# 需要同步的数据库，如果不配置则同步全部数据库
	# binlog-do-db=test_db
	# binlog日志保留的天数，清除超过7天的日志
	expire-logs-days=7
	#设置二进制日志使用内存大小（事务）
	binlog_cache_size=1M  
	#设置使用的二进制日志格式（mixed,statement,row）
	binlog_format=mixed 
	#relay_log配置中继日志
	relay_log=mysql-relay-bin  
	#log_slave_updates表示slave将复制事件写进自己的二进制日志
	log_slave_updates=1  
	# slave设置为只读（具有super权限的用户除外）
	read_only=1
	
### 2. 重启mysql
	
### 3. 在从数据库中配置主从复制

	mysql> mysql -u root -p
	
	mysql>  CHANGE MASTER TO 
			MASTER_HOST='192.168.0.100',
			master_port=3306,
			MASTER_USER='root',
			MASTER_PASSWORD='centos@123',
			MASTER_LOG_FILE='mysql-bin.000001',
			MASTER_LOG_POS=154,
			master_connect_retry=30;
			
			
	master_host：主数据库的IP地址；
	master_port：主数据库的运行端口；
	master_user：在主数据库创建的用于同步数据的用户账号；
	master_password：在主数据库创建的用于同步数据的用户密码；
	master_log_file：指定从数据库要复制数据的日志文件，通过查看主数据的状态，获取File参数；
	master_log_pos：指定从数据库从哪个位置开始复制数据，通过查看主数据的状态，获取Position参数；
	master_connect_retry：连接失败重试的时间间隔，单位为秒。
	
	mysql> show slave status \G;

	mysql> start slave;

	