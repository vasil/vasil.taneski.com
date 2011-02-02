import os
import re
import logging
import ConfigParser

from google.appengine.api import xmpp
from google.appengine.ext.webapp import template


def jabber(request, action):
    """Sends a xmmp message to user address.
    
    @param request: the wsgi request from which the call is made.
    @param action: string representation of the noted action.
    """
    
    if re.search(config.get('ua', 'browsers'), request.user_agent, re.I) and \
       not re.search(config.get('ua','bots'), request.user_agent, re.I):
        path = os.path.join(os.path.dirname(__file__), '..', 
                                                       'views', 
                                                       'visit.txt')
        template_vars = {'action': action,
                         'visitor_ip': request.remote_addr,
                         'referrer': request.referrer}
        msg = template.render(path, template_vars)
        xmpp.send_message(config.get('user', 'address'), msg)


config_path = os.path.join(os.path.dirname(__file__), '..',
                                                      '..', 
                                                      'config', 
                                                      'u240b.conf')
config = ConfigParser.ConfigParser()
config.read(config_path)
