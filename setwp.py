#!/usr/bin/python

import sys, getopt, os
import config
import libraries.brwsr as browser
import importlib
import cfg.urls as urls

wpml_cache_dir = "~/.wpml_cache"


def install_wordpress(to_dir, name):
    if os.path.isdir(wpml_cache_dir + "/downloads/wordpress"):
        os.chdir(wpml_cache_dir + "/downloads/")
        os.system('svn checkout ' + urls.wordpress['svn'] + ' wordpress')
        os.chdir("wordpress")
        os.system('wget ' + urls.wordpress['wpconfig'])
        os.chdir("../..")
    os.chdir(wpml_cache_dir + "/downloads/wordpress")
    os.system("svn up")
    os.chdir("..")
    os.system("cp -R wordpress" + " " + to_dir + "/" + name)


def install_git_plugins(plugin, details, name):
    print "##### installing plugin " + plugin + " #######"
    if not os.path.isdir(wpml_cache_dir + "/downloads/plugins/git/" + plugin):
        os.chdir(wpml_cache_dir + "/downloads/plugins/git/")
        os.system('git clone ' + details['url'])
        if details['composer'] == 1:
            os.chdir(wpml_cache_dir + "/downloads/plugins/git/" + plugin)
            os.system('composer.phar install --no-dev')
            os.chdir(os.pardir)
    os.chdir(wpml_cache_dir + "/downloads/plugins/git")
    os.system("cp -R " + plugin + " " + config.serverpath + "/" + name + "/wp-content/plugins/" + plugin)


def main(argv, urls):
    try:
        opts, args = getopt.getopt(argv, "dn:s:", ["name=", "delete", "set="])
    except getopt.GetoptError:
        print("error in getopt")

    name = config.name
    delete = False
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            name = arg
        if opt in ("-d", "--delete"):
            delete = True
        if opt in ("-s", "--set"):
            cfg_module_path = "cfg." + arg
            urls = importlib.import_module(cfg_module_path)

    name = name.replace("-", "")

    # go to server dir
    os.chdir(config.serverpath)

    if (delete):
        os.system("echo 'drop database " + name + "' | mysql -u" + config.dbuser + " -p" + config.dbpass)
        os.system("rm -rf " + name)
        print "Site '" + name + "' deleted"
        return

    # create database
    os.system("echo 'create database " + name + "' | mysql -u" + config.dbuser + " -p" + config.dbpass)

    # download wordpress
    install_wordpress(config.serverpath, name)

    # go to plugins dir
    os.chdir(config.serverpath + "/" + name + '/wp-content/plugins')

    # remove hello dolly
    os.system('rm -rf hello.php')

    # download plugins
    for plugin, details in urls.plugins['git'].iteritems():
        install_git_plugins(plugin, details, name)

    for plugin, url in urls.plugins['svn'].iteritems():
        os.system('svn co ' + url + ' ' + plugin)

    # go back to name dir and change chmod
    os.chdir(config.serverpath + "/" + name)
    os.system('chmod 777 .')

    browser.runbrowser(name)

    print "=================="
    print "Here is your site:"
    print config.serverurl + name + '/wp-admin'


if __name__ == "__main__":
    main(sys.argv[1:], urls)
