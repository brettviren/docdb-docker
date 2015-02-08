#!/usr/bin/env python
'''
Install DocDB
'''

import os
from subprocess import check_output, check_call

os.environ.setdefault('DOCDB_ROOT','/var/lib/docdb')

thisdir=os.path.dirname(os.path.realpath(__file__))


def pwgen(): 
    return check_output('pwgen -s 12 1',shell=True).strip()

def env(name, default=''):
    var='DOCDB_'+name.upper()
    ret = os.environ.get(var,default)
    #print ('name="%s" var="%s" default="%s" ret="%s"' % (name,var,default,ret))
    return ret


config = dict(
    root = env('root'),

    db_name = env('db_name','DocDB'),
    db_host = env('db_host','localhost'),

    db_admuser = env('db_admuser','docdbadm'),
    db_admpass = env('db_admpass', pwgen()),
    db_rwuser = env('db_rwuser','docdbrw'),
    db_rwpass = env('db_rwpass', pwgen()),
    db_rouser = env('db_rouser','docdbro'),
    db_ropass = env('db_ropass', pwgen()),

    web_admuser = env('web_admuser', 'docdbadm'),
    web_admpass = env('web_admpass', pwgen()),
    web_rwuser = env('web_rwuser', 'docdbrw'),
    web_rwpass = env('web_rwpass', pwgen()),

    file_root = env('file_root', os.path.join(env('root'), 'htdocs')),
    script_root = env('script_root', os.path.join(env('root'), 'cgi-bin')),
    web_host = env('web_host', 'localhost'),
    web_base = env('web_base', 'DocDB'),
    cgi_base = env('cgi_base', 'DocDB'),
    admin_email = env('admin_email','root@localhost'),
    admin_name = env('admin_name','root'),
    auth_file = env('auth_file', os.path.join(env('root'), 'passwords/htpasswd')),
    smtp_server = env('smtp_server','localhost'),
    first_year = env('first_year', 2000),
    project_name = env('project_name', 'Document Database'),
    project_nick = env('project_nick', 'DocDB'),

    giturl = env('giturl','https://github.com/ericvaandering/DocDB.git'),
    gittag = env('gittag'),
    srcdir = env('srcdir', os.path.join(env('root'), 'src')),

    my_cnf = env('my_cnf', os.path.join(env('root'), 'my.cnf')),
)

def form(string, **kwds):
    dat = dict(config)
    dat.update(**kwds)
    return string.format(**dat)

def info(string, **kwds):
    print (form('Info: ' + string, **kwds))


def shell(cmd, **kwds):
    fcmd = form(cmd,**kwds)
    info('shell: ' + fcmd)
    check_call(fcmd, shell=True)

def filter_template(template, destination):
    info('filtering %s -> %s' % (template, destination))

    text = open(template).read()
    try:
        newtext = text.format(**config)
    except KeyError:
        newtext = text % config

    open(destination, 'w').write(newtext)


def install_docdb_files():
    if os.path.exists(config['srcdir']):
        info ('source already installed at {srcdir}')
    else:
        tag = config.get('gittag')
        if tag:
            tag = '-b ' + tag
        shell('git clone {tag} {giturl} {srcdir}', tag=tag)

    shell('mkdir -p {file_root} && chown www-data.www-data {file_root}')
    shell('ln -sf {srcdir}/DocDB/html {file_root}/Static')
    shell('mkdir -p {script_root}')
    shell('ln -sf {srcdir}/DocDB/cgi {script_root}/private')
    # fixme; what about public/ ?

    for fname in ['ProjectGlobals.pm', 'ProjectMessages.pm',
                  'ProjectRoutines.pm', 'ProjectHelp.xml']:
        filter_template(os.path.join(thisdir, fname+'.template'), 
                        form('{script_root}/private/{fname}', fname=fname))

    filter_template(os.path.join(thisdir, 'apache-site.template'),
                    form('/etc/apache2/sites-available/{web_host}.conf'))
    shell('ln -sf /etc/apache2/sites-available/{web_host}.conf /etc/apache2/sites-enabled/')

    filter_template(os.path.join(thisdir, 'my.cnf.template'), config['my_cnf'])

    shell('rm -f {auth_file}')
    shell('mkdir -p {dir}', dir=os.path.dirname(config['auth_file']))
    shell('touch {auth_file}')  # retarded
    shell('htpasswd -m -b {auth_file} {web_admuser} {web_admpass}')
    shell('htpasswd -m -b {auth_file} {web_rwuser} {web_rwpass}')

    
def configure_mysql():
    filter_template(os.path.join(thisdir, 'mysql-init.sql.template'),
                    '/tmp/mysql-init.sql')
    filter_template(os.path.join(thisdir, 'mysql-secgrp.sql.template'),
                    '/tmp/mysql-secgrp.sql')
    shell('mysql -uroot -hlocalhost < /tmp/mysql-init.sql')

    shell('mysql -u{db_admuser} -p{db_admpass} {db_name} < {sql}',
          sql = os.path.join(thisdir,'CreateDatabase.SQL'))
    shell('mysql -u{db_admuser} -p{db_admpass} {db_name} < /tmp/mysql-secgrp.sql')
    

def main():
    install_docdb_files()
    configure_mysql()

if '__main__' == __name__:
    main()
