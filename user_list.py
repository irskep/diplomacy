#!/usr/bin/python

import config
import os, re, cgi, sys
from twik import *


def print_user_list(user_dict):
    con = db.connections.get_con()
    cur = db.DictCursor(con)
    cur.callproc('users_table')
    users = cur.fetchall()
    cur.close()
    db.connections.release_con(con)
    
    table_info = ((0, "name"), (1, "screen name"), (2, "email"), (3, ""), (4, ""))
    table = list()
    for row in users:
        send_msg = "<a class='inline' href='send_msg.py?sn="+row['screen_name']+"'>message</a>"
        add_to_game = "<a class='inline' href='new_game.py?sn="+row['screen_name']+"'>add to game</a>"
        table.append((row['name'], row['screen_name'], row['email'], send_msg, add_to_game))
    templater.print_template("templates/user_list.html", locals())

if __name__ == '__main__':
    
    form = cgi.FieldStorage()
    ses_dict, user_dict = user_manager.init_user_session(form)
    
    if user_dict == {}:
        target_page = 'user_list.py'
        templater.print_template("templates/login_template.html", locals())
    else:
        print_user_list(user_dict)
