from django.conf import settings
import base64
import hashlib
import hmac
import simplejson
import time
 
DISQUS_SECRET_KEY = 'vRH9JSvhIdzA5JXKAGctjUYu3qc2OEqzbq4BXcSdE81XKe4UTyF3jiOh2kyNPDxS'
DISQUS_PUBLIC_KEY = 'b3WBwKT9FqgFdDPvF9SghI4CstUEmkfJEJxVcaDPrgtBcEM1qtdFOcdJ2FKinjUq'
 
def get_disqus_sso(user=None):
    # create a JSON packet of our data attributes
    if user:
	data = simplejson.dumps({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })
    else:
	data = simplejson.dumps({})
    # encode the data to base64
    message = base64.b64encode(data)
    # generate a timestamp for signing the message
    timestamp = int(time.time())
    # generate our hmac signature
    sig = hmac.HMAC(DISQUS_SECRET_KEY, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
 
# return a script tag to insert the sso message
    return """<script type="text/javascript">
    var disqus_config = function() {
        this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";
    }
    </script>""" % dict(
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=DISQUS_PUBLIC_KEY,
    )
