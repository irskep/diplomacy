#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *
    

form = cgi.FieldStorage()
ses_dict, user_dict = user_manager.init_user_session()


if user_dict == {}:
    
    if form.has_key("name") and form.has_key("screen_name") and form.has_key("reg_email") and\
       form.has_key("passwd1") and form.has_key("passwd2"):
        try:
            email = templater.validators.Email(resolve_domain=True,
                                               not_empty=True).to_python(form["reg_email"].value)
        except templater.formencode.Invalid, e:
            templater.print_error("email: "+str(e))
            sys.exit()
        
        try:
            name = templater.validators.PlainText(r"^[a-zA-Z_\-0-9 ]*$",
                                                  not_empty=True).to_python(form["name"].value)
        except templater.formencode.Invalid, e:
            templater.print_error("name: "+str(e))
            sys.exit()
        
        try:
            screen_name = templater.validators.PlainText(not_empty=True).to_python(form["screen_name"].value)
        except templater.formencode.Invalid, e:
            templater.print_error("screen_name: "+str(e))
            sys.exit()
        
        try:
            ps_validators = templater.validators.FieldsMatch('p1', 'p2')
            ps = ps_validators.to_python({'p1':form["passwd1"].value, 'p2':form["passwd2"].value})['p1']
        except templater.formencode.Invalid, e:
            templater.print_error("Passwords: "+str(e))
            sys.exit()
        
        if user_manager.get_user_byemail(email):
            templater.print_error("that email address already has a user registered to it")
            sys.exit()
        
        #print 'heyhey<br><br>'
        user_manager.add_user(user_manager.gen_userID(), name, email,
                              screen_name, ps)
        templater.print_template("templates/login_template.html", {'target_page':'main.py'})
    elif form.has_key("name") or form.has_key("screen_name") or form.has_key("reg_email") or\
         form.has_key("passwd1") or form.has_key("passwd2"):
        templater.print_error("All fields must be filled out.")
    else:
        templater.print_template("templates/register.html", {'target_page':'register.py'})
else:
    templater.print_template("templates/login_template.html", {'target_page':'login.py'})