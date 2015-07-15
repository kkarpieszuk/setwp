from splinter import Browser
import config
import time

def firstwizard(b, name):
    b.visit( config.serverurl + name )
    b.find_by_css('a.button-large').click()
    b.find_by_css('#dbname').fill( name )
    b.find_by_css('#uname').fill( config.dbuser )
    b.find_by_css('#pwd').fill( config.dbpass )
    b.find_by_css('input.button-large').click()
    if (b.is_text_present('Run the install', wait_time=2)):
        b.find_by_css('a.button-large').click()
        b.find_by_css('#weblog_title').fill( name )
        b.find_by_css('#user_login').fill( config.wpuser )
        b.find_by_css('.wp-generate-pw').click()
        b.find_by_css('#pass1').fill( config.wppass )
        b.check('pw_weak')
        b.find_by_css('#admin_email').fill(  config.wpmail )
        b.find_by_css('input.button-large').click()

def runbrowser(name):
    with Browser() as b:
        firstwizard(b, name)
