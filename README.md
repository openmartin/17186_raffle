## 关于

17186.cn 是山东联通沃玩家的网站，有很多优惠活动，但是每天都要手动去签到和摇一摇很麻烦，
这个脚本就是为了解决这个问题，实现了自动签到和自动摇一摇，代码非常简单。

## 安装

新建虚拟环境

    virtualenv raffle
    cd raffle
    source bin/activate


下载代码

    git clone https://github.com/openmartin/17186_raffle.git
    
修改配置
    
    重命名raffle.template.yaml 为 raffle.yaml，把里面的user和pasword修改为自己的用户名密码
    
    main:
      login:
        user: 186********
        password: ******
    
    配置在你本地电脑或者是你的服务器上，所以是安全的，但是密码是明文的，注意不要让别人看到。
    
添加定时任务

    方法一
    sudo echo "0 20 * * * /home/ec2-user/raffle/17186_raffle/daily_run.sh" >> /var/spool/cron/ec2-user
    注意:修改为你的路径，用户名
    
    方法二
    crontab raffle.cron
    注意:会直接替换掉你的cron配置，如果你的cron里面有配置的话，别使用这种方式。

