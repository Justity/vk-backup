#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''VK-Backup Dialogs

Author:      Rabit <home@rabits.org>
License:     GPL v3
Description: Dialogs management
Required:    python3.5
'''

from . import Common as c

from .Database import Database

from . import Api
from . import Messages
from .Users import S as Users
from .Chats import S as Chats

class Dialogs(Database):
    def requestDialogs(self):
        c.log('debug', 'Requesting dialogs')

        req_data = {'count': 200, 'preview_length': 1, 'offset': 0}

        while True:
            data = Api.request('messages.getDialogs', req_data)
            if data == None:
                return
            count = data['count']
            data = data['items']
            for d in data:
                if 'chat_id' in d['message']:
                    Chats.requestChatMessages(d['message']['chat_id'])
                else:
                    self.requestMessages(d['message']['user_id'])

            req_data['offset'] += 200
            if req_data['offset'] >= count:
                break

    def requestMessages(self, user_id):
        user = Users.getUser(user_id)
        c.log('info', 'Requesting messages for user %s %s %s' % (user_id, user['data']['first_name'], user['data']['last_name']))

        if user_id not in self.data:
            self.data[str(user_id)] = {
                'id' :  user_id,
                'log' : []
            }

        Messages.requestMessages({'user_id': user_id}, self.data[str(user_id)])

    def getMessages(self, user_id):
        if str(user_id) not in self.data:
            self.requestMessages(user_id)
        return self.data[str(user_id)]

S = Dialogs()
