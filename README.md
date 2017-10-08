Lianjia_Spider_Redis
===
# 一．项目介绍<br> 
使用lxml+MongoDB+echart进行链家网房产信息数据的爬取、存储及可视化。分布式爬虫采用redis主-从结构，主机负责爬取一级URL并生成二级URL，从机负责二级URL数据爬取、存储及相关信息反馈给主机。主从通信采用redis的set实现。主机采用双线程，分别生成二手房、租房信息的url hash集合并存于redis,从机去redis集合拿url并爬取，爬取失败的url则重新加入集合<br> 
# 二. 反爬<br> 
从免费IP代理池中选择代理IP，不断换取User-Agent， 并且控制随机访站时间<br>

