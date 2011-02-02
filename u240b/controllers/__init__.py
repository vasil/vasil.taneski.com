import urllib
import base64
import os.path
import hashlib
import logging

from u240b.utils import config
from u240b.utils import jabber
from u240b.models import Cv
from u240b.models import Visit

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    """Handler for the main page requests (/).
    """
    
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '..', 
                                                       'views', 
                                                       'index.html')
        template_vars = {'short_status': config.get('200', 'short'),
                         'long_status': config.get('200', 'long')}
        self.response.out.write(template.render(path, template_vars))
        visit = Visit(self.request)
        visit.put()
        jabber(self.request, config.get('action', 'visiting'))


class CVHandler(webapp.RequestHandler):
    """Handler for the CV requests (/cv).
    """
    
    def get(self):
        cv = Cv.all().order('-created_at').get()
        
        self.response.headers['ETag'] = cv.e_tag
        self.response.headers['Last-Modified'] = cv.rfc2822_date
        self.response.headers['Content-MD5'] = cv.md5_sum
        self.response.headers['Content-Type'] = config.get('content', 'type')
        self.response.headers['Content-Disposition'] = '%s;filename=%s' % (
                                          config.get('content', 'disposition'),
                                          config.get('content', 'filename'))
        self.response.out.write(cv.pdf)
        visit = Visit(self.request)
        visit.put()
        jabber(self.request, config.get('action', 'download_cv'))


class AdminHandler(webapp.RequestHandler):
    """Handler for the admin pages (/admin).
    """
    
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '..', 
                                                       'views', 
                                                       'admin.html')
        self.response.out.write(template.render(path, {}))
    
    def post(self):
        try:
            cv = Cv(pdf=db.Blob(self.request.get('file')))
            md5 = hashlib.md5(cv.pdf)
            cv.rfc2822_date = cv.created_at.strftime('%a, %d %b %Y %H:%M:%S'\
                                                     '+0100')
            cv.e_tag = md5.hexdigest()
            cv.md5_sum = base64.encodestring(md5.digest()).rstrip()
            cv.put()
            self.redirect('/%s' % config.get('upload', 'ok'))
        except Exception, err:
            logging.error(err)
            self.redirect('/%s' % config.get('upload', 'fail'))


class SitemapHandler(webapp.RequestHandler):
    """Handler for the sitemap.xml
    """
    
    def get(self):
        cv = Cv.all().order('-created_at').get()
        
        path = os.path.join(os.path.dirname(__file__), '..', 
                                                       'views', 
                                                       'sitemap.xml')
        template_vars = {'lastmod': cv.created_at.isoformat()[:-7] + '+01:00'}
        self.response.out.write(template.render(path, template_vars))


class NotFoundHandler(webapp.RequestHandler):
    """Handler for the undefined pages.
    """
    
    def get(self, page=None):
        self.error(404)
        path = os.path.join(os.path.dirname(__file__), '..', 
                                                       'views', 
                                                       'index.html')
        template_vars = {'short_status': config.get('404', 'short'),
                         'long_status': config.get('404', 'long'),
                         'page': str(urllib.unquote_plus(page))}
        self.response.out.write(template.render(path, template_vars))
