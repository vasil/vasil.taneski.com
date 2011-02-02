from google.appengine.ext import db


class Cv(db.Model):
    """Model for the CV Entries.
    """
    
    pdf = db.BlobProperty(required=True)
    rfc2822_date = db.StringProperty()
    e_tag = db.StringProperty()
    md5_sum = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)


class Visit(db.Model):
    """Model for the Visit Entries.
    """
    
    ip = db.StringProperty()
    referrer = db.URLProperty()
    user_agent = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    def __init__(self, request):
        super(Visit, self).__init__()
        self.ip = request.remote_addr
        self.user_agent = request.user_agent

        if request.referrer:
            self.referrer = request.referrer
