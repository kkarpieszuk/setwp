#!/usr/bin/python

import sys, getopt, os
import config
import libraries.brwsr as browser
import cfg.urls as urls


def main(argv):
    thisdir = os.getcwd()

    try:
        opts, args = getopt.getopt(argv, "n:", ["name="])
    except getopt.GetoptError:
        print "error in getopt"

    name = config.name
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            name = arg

    # create database
    os.system("echo 'create database "+name+"' | mysql -u"+config.dbuser+" -p"+config.dbpass)

    # go to server dir
    os.chdir(config.serverpath)

    # download wordpress
    os.system('svn checkout '+ urls.wordpress['svn'] +' ' + name)

    # go into wordpress dir
    os.chdir(name)

    # download wpconfigsample
    os.system('wget ' + urls.wordpress['wpconfig'])

    # go to plugins dir
    os.chdir('wp-content/plugins')

    # remove hello dolly
    os.system('rm -rf hello.php')

    #download plugins
    for plugin, url in urls.otgs['git'].iteritems():
        os.system('git clone ' + url)

    for plugin, url in urls.external_plugins['svn'].iteritems():
        os.system('svn co ' + url + ' ' + plugin )

    # go back to name dir and change chmod
    os.chdir('../..')
    os.system('chmod 777 .')

    browser.runbrowser(name)

    print "=================="
    print "Here is your site:"
    print config.serverurl + name + '/wp-admin'


if __name__ == "__main__":
    main(sys.argv[1:])
