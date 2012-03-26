from zope.component import adapts
from zope.interface import implements
from persistent import Persistent
from BTrees.LOBTree import LOBTree
from betahaus.pyracont.decorators import content_factory
from betahaus.pyracont.factories import createContent

from voteit.core.models.date_time_util import utcnow
from voteit.core.models.interfaces import ISiteRoot

from voteit.site.models.interfaces import ISupportStorage
from voteit.site.models.interfaces import ISupportRequest
from voteit.site import SiteMF as _


class SupportStorage(object):
    """ An adapter for ISiteRoot that handle feed entries.
    """
    implements(ISupportStorage)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def support_storage(self):
        if not hasattr(self.context, '__support_storage__'):
            self.context.__support_storage__ = LOBTree()
        return self.context.__support_storage__
    
    def _next_free_key(self):
        if len(self.support_storage) == 0:
            return 0
        return self.support_storage.maxKey()+1
    
    def add(self, message, subject='', name='', email='', meeting=None):
        """ Add a support request.
        """
        obj = createContent('SupportRequest', message, subject=subject, name=name, email=email, meeting=meeting)
        
        for i in range(10):
            k = self._next_free_key()
            if self.support_storage.insert(k, obj):
                return
        
        raise KeyError("Couln't find a free key for support request after 10 retries.") # pragma : no cover


@content_factory('SupportRequest', title=_(u"Support request"))
class SupportRequest(Persistent):
    implements(ISupportRequest)

    def __init__(self, message, subject='', name='', email='', meeting=None):
        self.created = utcnow()
        self.message = message
        self.subject = subject
        self.name = name
        self.email = email
        self.meeting = meeting


def includeme(config):
    """ Include to activate support storage components.
        like: config.include('voteit.site.models.support_storage')
    """
    #Register SupportRequest adapter
    config.registry.registerAdapter(SupportStorage, (ISiteRoot,), ISupportStorage)