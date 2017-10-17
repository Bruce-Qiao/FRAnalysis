from fabric.api import *
from fabric.contrib.console import confirm

def commit():
    comment = input("Git comment: ")
    local("git add . && git commit -m \"%s\"" % comment)

def push():
    local("git push origin master")

def push_production():
    local("git push production master")

def develop():
    commit()
    push()

def prepare_deploy_production():
    commit()
    push_production()

def deploy():
    code_dir = '/home/www/weixin_project'
    with cd(code_dir):
        run("sudo supervisorctl restart weixin_project")

def production():
    env.hosts = ['104.237.136.103']
    env.user = 'apps'
    prepare_deploy_production()
    deploy()
