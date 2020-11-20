## 环境配置

1. 下载

    ```
    git clone git@github.com:yuhixyz/Four-Mixed-Operation-Practice-System.git
    cd Four-Mixed-Operation-Practice-System
    ```

2. 安装依赖（python>=3.7.9）

    ```
    pip install -r requirements.txt
    ```

## 本地测试

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

    注意：此时使用的配置为 settings.dev，如果需要线上部署，请将配置文件切换为 settings.prod

5. 登录 django-admin 后台
    
    访问 http://127.0.0.1:8000/admin