#!/usr/bin/env python2.6

import u240b.controllers as controllers

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


def main():
    application = webapp.WSGIApplication([
                              ('/', controllers.MainHandler),
                              ('/[c|C][v|V]', controllers.CVHandler),
                              ('/admin', controllers.AdminHandler),
                              ('/sitemap.xml', controllers.SitemapHandler),
                              ('/(?!_ah/)(.*)', controllers.NotFoundHandler)])
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
