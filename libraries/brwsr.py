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
        b.find_by_css('#pass1-text').fill( config.wppass )
        b.check('pw_weak')
        b.find_by_css('#admin_email').fill(  config.wpmail )
        b.find_by_css('input.button-large').click()

def activateplugins(b, name):
    url = config.serverurl + name + '/wp-admin'
    b.visit( url )
    b.find_by_css('#user_login').fill(config.wpuser)
    time.sleep(2)
    b.find_by_css('#user_pass').fill(config.wppass)
    b.check('rememberme')
    b.find_by_css('#wp-submit').click()
    if (b.is_text_present('Dashboard', wait_time=2)):
        b.visit( url + '/plugins.php')
        b.find_by_css('#cb-select-all-1').check()
        b.select('action', 'activate-selected')
        b.find_by_css('#doaction').click()
        '''
        if (b.is_text_present('Welcome to WooCommerce', wait_time=2)):
            b.find_by_css('.woocommerce-message a.button-primary').first.click()
            b.find_by_css('.wc-setup-actions .button-primary').first.click()
            time.sleep(1)
            b.find_by_name('save_step').first.click()
            time.sleep(1)
            b.find_by_name('save_step').first.click()
            time.sleep(1)
            b.find_by_name('save_step').first.click()
            time.sleep(1)
            b.find_by_name('save_step').first.click()
            time.sleep(1)
            b.find_by_css('.submit a.skip').click()
        b.visit( url )
        '''
        if (b.is_text_present('No thanks, I will configure myself', wait_time=2)):
            b.find_by_text('No thanks, I will configure myself').click()
            b.find_by_name('save').click()
            for lang in config.languages:
                b.find_by_value(lang).check()
            b.find_by_value('Next').click()
            time.sleep(3)
            b.find_by_name('icl_lang_sel_footer').check()
            b.find_by_value('Next').click()
            time.sleep(3)
            b.find_by_name('later').click()
            time.sleep(3)
            b.find_by_name('finish').click()
            time.sleep(3)
            b.find_by_css('.installer-dismiss-nag').click()
            time.sleep(3)

def runbrowser(name):
    with Browser() as b:
        firstwizard(b, name)
        activateplugins(b, name)
