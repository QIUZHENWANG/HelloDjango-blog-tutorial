from fabric import task
from invoke import Responder
from fabric import Connection


def _get_github_auth_responders(c):
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(c.github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(c.github_username),
        response='{}\n'.format(c.github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'hellodjango-blog-tutorial'
    project_root_path = '~/apps/HelloDjango-blog-tutorial/'
    
    host_ip = c.host # 服务器地址 
    user_name = c.user # 服务器用户名 
    password = c.pwd # 服务器密码 
    #cmd = 'date' # shell 命令，查询服务器上的时间 
    con = Connection(host_ip, user_name, connect_kwargs={'password': password})
    # 先停止应用
    with con.cd(supervisor_conf_path):
        cmd = 'supervisorctl stop {}'.format(supervisor_program_name)
        con.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with con.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders(c)
        con.run(cmd, watchers=responders)

    # 安装依赖，迁移数据库，收集静态文件
    with con.cd(project_root_path):
        con.run('pipenv install --deploy --ignore-pipfile')
        con.run('pipenv run python manage.py migrate')
        con.run('pipenv run python manage.py collectstatic --noinput')

    # 重新启动应用
    with con.cd(supervisor_conf_path):
        cmd = 'supervisorctl start {}'.format(supervisor_program_name)
        con.run(cmd)
        
@task()
def test(c):
    host_ip = c.host # 服务器地址 
    user_name = c.user # 服务器用户名 
    password = c.pwd # 服务器密码 
    cmd = 'date' # shell 命令，查询服务器上的时间 
    con = Connection(host_ip, user_name, connect_kwargs={'password': password})
    result = con.run(cmd, hide=True)
    print(result)
