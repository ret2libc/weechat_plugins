# -*- coding: utf-8 -*-

# replace messages coming from r2tgirc with the real username
#
# A weechat plugin to replace the nickname of the messages coming from r2tgirc
# with the real name.
#

import_ok = True

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    import_ok = False

try:
    import re
except ImportError as message:
    print('Missing package(s) for %s: %s' % (SCRIPT_NAME, message))
    import_ok = False

SCRIPT_NAME = 'r2tgirc_replace_nick'
SCRIPT_AUTHOR = 'Riccardo Schirone <sirmy15@gmail.com>'
SCRIPT_VERSION = '0.1'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = "When a message comes from r2tgirc, it is replaced with one coming from the real nickname"

VALID_NICK = r'([@~&!%+-])?([^\s,\*?\.!@]+)'
VALID_WRAP_NICK = r'<([@~&!%+-])?([^\s,\*?\.!@]+)> (.*)'
valid_wrap_nick_re = re.compile(VALID_WRAP_NICK)

bot_nick = 'r2tg'
channel = '#radare'
bot_line_re = re.compile(r':' + VALID_NICK + '!([^ ]*) PRIVMSG ' + channel + ' :(.*)')

def replacer2tgnick(data, modifier, modifier_data, string):
    m = bot_line_re.match(string)
    if m is None:
        return string

    sender_nick = m.groups()[1]
    sender_user = m.groups()[2]
    msg = m.groups()[3]

    if sender_nick != bot_nick:
        return string

    m = valid_wrap_nick_re.match(msg)
    if m is None:
        return string

    real_sender = m.groups()[1]
    real_msg = m.groups()[2]

    return ':' + real_sender + '!' + sender_user + ' PRIVMSG ' + channel + ' :' + real_msg

if __name__ == '__main__' and import_ok:
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
        weechat.hook_modifier('irc_in_privmsg', 'replacer2tgnick', '')
