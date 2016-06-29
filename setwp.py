#!/usr/bin/python

import sys, getopt, os
import config
import libraries.brwsr as browser
import cfg.urls as urls

def install_wordpress(to_dir, name):
    this_dir = os.path.dirname(os.path.realpath(__file__))

    if os.path.isdir( this_dir + "/downloads/wordpress"  ) == False:
        os.chdir(this_dir + "/downloads/")
        os.system('svn checkout '+ urls.wordpress['svn'] +' wordpress')
        os.chdir("wordpress")
        os.system('wget ' + urls.wordpress['wpconfig'])
        os.chdir("../..")
    os.chdir(this_dir + "/downloads/wordpress")
    os.system("svn up")
    os.chdir("..")
    os.system("cp -R wordpress" + " " + to_dir + "/" + name)





def main(argv):
    try:
        opts, args = getopt.getopt(argv, "dn:", ["name=", "delete"])
    except getopt.GetoptError:
        print "error in getopt"

    name = config.name
    delete = False
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            name = arg
        if opt in ("-d", "--delete"):
            delete = True

    name = name.replace("-", "")

    # go to server dir
    os.chdir(config.serverpath)

    if (delete):
        os.system("echo 'drop database "+name+"' | mysql -u"+config.dbuser+" -p"+config.dbpass)
        os.system("rm -rf " + name)
        print "Site '" + name + "' deleted"
        return


    # create database
    os.system("echo 'create database "+name+"' | mysql -u"+config.dbuser+" -p"+config.dbpass)

    # download wordpress
    install_wordpress(config.serverpath, name)

    

    # go to plugins dir
    os.chdir(config.serverpath + "/" + name + '/wp-content/plugins')

    # remove hello dolly
    os.system('rm -rf hello.php')

    #download plugins
    for plugin, details in urls.plugins['git'].iteritems():
        os.system('git clone ' + details['url'])
        if (details['composer'] == 1):
            os.chdir(plugin)
            os.system('composer.phar install')
            os.chdir(os.pardir)

    for plugin, url in urls.plugins['svn'].iteritems():
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
