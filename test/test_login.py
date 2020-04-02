#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import re
from helper_ui import ui_class
from testconfig import TEST_DB
from helper_func import startup, check_response_language_header, curl_available, digest_login
from parameterized import parameterized_class


'''@parameterized_class([
   { "py_version": u'/usr/bin/python'},
   { "py_version": u'/usr/bin/python3'},
],names=('Python27','Python36'))'''
class test_login(unittest.TestCase, ui_class):
    p=None
    driver = None

    @classmethod
    def setUpClass(cls):
        try:
            startup(cls, cls.py_version, {'config_calibre_dir':TEST_DB}, login=False)
        except:
            cls.driver.quit()
            cls.p.kill()


    @classmethod
    def tearDownClass(cls):
        # close the browser window and stop calibre-web
        cls.driver.quit()
        cls.p.kill()

    def tearDown(self):
        if self.check_user_logged_in('', True):
            self.logout()

    def fail_access_page(self, page):
        try:
            self.driver.get(page)
        except WebDriverException as e:
            return re.findall('Reached error page: about:neterror?e=connectionFailure', e.msg)
        if self.driver.title == u'500 Internal server error':
            return 2
        elif self.driver.title == u'Calibre-Web | HTTP Error (Error 403)':
            return 2
        elif self.driver.title == u'Calibre-Web | HTTP Error (Error 404)':
            return 2
        elif self.driver.title == u'Calibre-Web | HTTP Error (Error 405)':
            return 2
        elif self.driver.title == u'Calibre-Web | Login' or self.driver.title == u'Calibre-Web | login':
            return 1
        else:
            return 0

    # try to access all pages without login
    def test_login_protected(self):
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/config"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/user"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/user/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/user/resetpassword/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/book"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/book/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/upload"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/convert"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/convert/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/view"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/config"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/viewconfig"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/user/new"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin/mailsettings"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/ajax/emailstat"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/ajax/editdomain"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/ajax/deletedomain"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/ajax/domainlist"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/ajax/toggleread"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/ajax/bookmark/1/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/get_authors_json"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/get_tags_json"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/get_languages_json"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/get_series_json"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/get_matching_tags"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/get_update_status"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/get_updater_status"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/tasks"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/stats"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/page"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/book"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/book/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/newest"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/newest/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/newest/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/newest/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/oldest"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/oldest/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/oldest/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/a-z"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/a-z/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/a-z/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/hot"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/hot/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/hot/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/rated"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/rated/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/rated/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/discover"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/discover/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/discover/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/author"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/author/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/author/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/series"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/series/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/series/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/language"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/language/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/language/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/category"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/category/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/books/category/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/unreadbooks"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/unreadbooks/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/unreadbooks/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/readbooks"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/readbooks/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/readbooks/page/2"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/delete"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/delete/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/delete/1/EPUB"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/gdrive"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/gdrive/authenticate"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/gdrive/callback"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/gdrive/watch"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/gdrive/watch/subscribe"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/gdrive/watch/revoke"),1)
        # self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/gdrive/watch/callback"),0)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shutdown"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/update"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/search"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/advanced_search"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/cover"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/cover/213"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/show/1/epub"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/read/1/epub"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/download/1/epub"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/download/1/epub/name"),1) # important this endpoint has to exist, otherwise Kobo download will fail
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/register"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/logout"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/remote_login"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/verify/34898295"),2)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/ajax/verify_token"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/send/66"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/add"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/add/1/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/massadd"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/remove"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/remove/1/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/create"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/delete"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/delete/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/shelf/order/1"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/me"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/admin"),1)
        self.assertEqual(self.fail_access_page("http://127.0.0.1:8083/"),1)

    # login with admin
    # create new user, leave passwort empty
    # logout
    # try to login
    # logout
    def test_login_empty_password(self):
        self.driver.get("http://127.0.0.1:8083/login")
        self.login('admin','admin123')
        self.create_user('epass',{'email':'a5@b.com'})
        self.assertTrue(self.check_element_on_page((By.ID,'flash_alert')))
        self.create_user('epass', {'email': 'a5@b.com', 'password':'1', 'passwd_role':1})
        self.assertTrue(self.check_element_on_page((By.ID,'flash_success')))
        self.logout()
        self.assertTrue(self.login('epass','1'))
        self.change_visibility_me({'password':''})
        self.assertTrue(self.check_element_on_page((By.ID,'flash_success')))
        self.logout()
        self.assertFalse(self.login('epass',''))
        self.assertTrue(self.login('epass', '1'))
        self.logout()

    # login with admin
    # create new user (Capital letters), passwort with ß and unicode and spaces within
    # logout
    # try login with username lowercase letters and correct password
    # logout
    # try login with username lowercase letters and password with capital letters
    # logout
    def test_login_capital_letters_user_unicode_password_passwort(self):
        self.driver.get("http://127.0.0.1:8083/login")
        self.login('admin','admin123')
        self.create_user('KaPiTaL',{'password':u'Kß ü执','email':'a@b.com'})
        self.logout()
        self.assertTrue(self.login('KAPITAL',u'Kß ü执'))
        self.logout()
        self.assertTrue(self.login('kapital',u'Kß ü执'))
        self.logout()
        self.assertFalse(self.login('KaPiTaL', u'kß ü执'))

    # login with admin
    # create new user (unicode characters), passwort with spaces at begining
    # logout
    # try login with username and correct password
    # logout
    # try login with username and password without space at beginning
    def test_login_unicode_user_space_end_passwort(self):
        self.driver.get("http://127.0.0.1:8083/login")
        self.login('admin','admin123')
        self.create_user(u'Kß ü执',{'password':' space', 'email':'a1@b.com'})
        self.logout()
        self.assertTrue(self.login(u'Kß ü执',' space'))
        self.logout()
        self.assertFalse(self.login(u'Kß ü执','space'))


    # login with admin
    # create new user (spaces within), passwort with space at end
    # logout
    # try login with username and correct password
    # logout
    # try login with username without space and correct password without space at end
    # try login with username with space and password without space at end
    def test_login_user_with_space_passwort_end_space(self):
        self.driver.get("http://127.0.0.1:8083/login")
        self.login('admin','admin123')
        self.create_user('Klaus peter',{'password':'space ','email':'a2@b.com'})
        self.logout()
        self.assertTrue(self.login('Klaus peter','space '))
        self.logout()
        self.assertFalse(self.login('Klauspeter','space'))
        self.logout()
        self.assertFalse(self.login('Klaus peter','space'))

    # login with admin
    # create new user as admin user
    # logout
    # try login with username and correct password
    # logout
    # delete original admin user
    # logout
    # try login with orig admin
    # rename user to admin
    # logout
    # ToDo: for real check restart has to be performed
    def test_login_delete_admin(self):
        self.driver.get("http://127.0.0.1:8083/login")
        self.login('admin','admin123')
        self.create_user('admin2',{'password':'admin2', 'admin_role':1 ,'email':'a3@b.com'})
        self.logout()
        self.assertTrue(self.login('admin2','admin2'))
        self.edit_user('admin',{'delete':1})
        self.logout()
        self.assertFalse(self.login('admin','admin123'))
        self.login('admin2','admin2')
        self.create_user('admin',{'password':'admin123', 'admin_role':1,'email':'a4@b.com'})
        self.logout()

    @unittest.skipIf(not curl_available, "Skipping language detection, pycurl not available")
    def test_login_locale_select(self):
        # this one should work and throw not an error 500
        url = 'http://127.0.0.1:8083/login'
        self.assertTrue(check_response_language_header(url,
                                                       ['Accept-Language: de-de;q=0.9,en;q=0.7,*;q=0.8'],
                                                       200,
                                                       '<label for="username">Benutzername</label>'),
                        'Locale detect with "-" failed')
        self.assertTrue(check_response_language_header(url,
                                                       ['Accept-Language: *;q=0.9,de;q=0.7,en;q=0.8'],
                                                       200,
                                                       '<label for="username">Username</label>'),
                        'Locale detect with different q failed')
        self.assertTrue(check_response_language_header(url,
                                                       ['Accept-Language: zh_cn;q=0.9,de;q=0.8,en;q=0.7'],
                                                       200,
                                                       '<label for="username">昵称</label>'))
        self.assertTrue(check_response_language_header(url,
                                                       ['Accept-Language: xx'],
                                                       200,
                                                       '<label for="username">Username</label>'),
                        'Locale detect with unknown locale failed')
        self.assertTrue(check_response_language_header(url,
                                                       ['Accept-Language: *'],
                                                       200,
                                                       '<label for="username">Username</label>'),
                        'Locale detect with only "*" failed')

    # CHek that digest Authentication header doesn't crash the aplication
    @unittest.skipIf(not curl_available, "Skipping auth_login, pycurl not available")
    def test_digest_login(self):
        url = 'http://127.0.0.1:8083/login'
        self.assertTrue(digest_login(url,200))

