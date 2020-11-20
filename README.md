## 项目预览

1. 地址：http://calc.yuhi.xyz

2. 用于测试的账号密码
    账号：test
    密码：test

## 环境配置

1. 下载

    ```
    git clone git@github.com:yuhixyz/Four-Mixed-Operation-Practice-System.git
    cd Four-Mixed-Operation-Practice-System
    ```

2. 安装依赖（python>=3.7.9）

    建议先进入虚拟环境（也可以不），如果使用 `virtualenvwrapper-win` 进行 `python` 的虚拟环境管理，可以参考我的一篇博客：[https://yuhi.xyz/post/win10-配置-python-虚拟环境](https://yuhi.xyz/post/win10-%E9%85%8D%E7%BD%AE-python-%E8%99%9A%E6%8B%9F%E7%8E%AF%E5%A2%83/)。
    
    进入虚拟环境后，进入项目根目录，然后安装项目的依赖
    
    ```
    pip install -r requirements.txt
    ```

## 启动本地服务

1. 将 settings 下的 base.example.py 修改为 base.py 并修改其中的 SECRET_KEY

2. 建立数据库（使用sqlite3，无需额外配置）
    
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

2. 拷贝静态文件
    
    ```
    python manage.py collectstatic
    ```

3. 创建超级管理员

    ```
    python manage.py createsuperuser
    ```

4. 启动本地服务

    ```
    python manage.py runserver
    ```

    访问 http://127.0.0.1:8000 。

    注意：此时使用的配置为 settings.dev 。如果需要线上部署，请将配置文件切换为 settings.prod（需要修改 manage.py 和 wsgi.py 中的配置）。

5. 登录 django-admin 后台
    
    访问 http://127.0.0.1:8000/admin 。

6. 登录后台后创建其他用户

    用户名：随便取； 密码：xxx
    
    设置密码时，假设你希望某用户登录时设置的密码为字符串 S，那么你给他预置的密码应该是 S 经过哈希后的结果。

    在命令行，用 `python manage.py shell` 进入交互状态（注意不要直接使用 `python` 命令， django 会找不到 DJANGO_SETTINGS_MODULE 这一配置信息）

    进入交互状态后，利用 `make_password()` 生成密码即可。

    ```python
    from django.contrib.auth.hashers import make_password 
    print(make_password("tqlqwqtql")) # 假设我们需要的密码是 tqlqwqtql
    ```
    
    得到结果 
    ```
    pbkdf2_sha256$216000$lfz8J1V7JI4j$lvnqFihDDzuiEVAVQN4FD3EGMqm5juaczN1B4lLDgVw=
    ```

    上面的结果就是管理员需要在后台预置的密码，用户登陆时，使用密码"tqlqwqtql" 登录即可。