#!/usr/bin/python

import config
import os, re, cgi, templater, db
import cookie_session, user_manager

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session(form)

if user_dict == {}:
    target_page = 'main.py'
    templater.print_template("templates/login_template.html", locals())
else:
    templater.print_template("templates/main.html", locals())