import unittest
from datetime import datetime

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.component.interfaces import IFactory
from zope.component import createObject


class SupportStorageTests(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        self.config.testing_securitypolicy(userid='some_user',
                                           permissive=True)

    def tearDown(self):
        testing.tearDown()

    def _make_adapted_obj(self):
        from voteit.core.models.site import SiteRoot
        from voteit.site.models.support_storage import SupportStorage
        context = SiteRoot()
        return SupportStorage(context)

    def _register_support_request_factory(self):
        #FIXME: Detach more?
        self.config.scan('voteit.site.models.support_storage')

    def test_interface(self):
        from voteit.site.models.interfaces import ISupportStorage
        obj = self._make_adapted_obj()
        self.assertTrue(verifyObject(ISupportStorage, obj))

    def test_add(self):
        self._register_support_request_factory()
        obj = self._make_adapted_obj()
        meeting = object()
        obj.add('message', subject='subject', name='name', email='email', meeting=meeting)
        
        self.assertEqual(len(obj.support_storage), 1)
        self.assertEqual(obj.support_storage[0].message, 'message')
        self.assertEqual(obj.support_storage[0].subject, 'subject')
        self.assertEqual(obj.support_storage[0].name, 'name')
        self.assertEqual(obj.support_storage[0].email, 'email')
        self.assertEqual(obj.support_storage[0].meeting, meeting)
        
        obj.add('message', subject='subject', name='name', email='email', meeting=meeting)
        self.assertEqual(len(obj.support_storage), 2)

    def test_registration_on_include(self):
        self.config.include('voteit.site.models.support_storage')
        from voteit.core.models.site import SiteRoot
        root = SiteRoot()
        from voteit.site.models.interfaces import ISupportStorage
        adapter = self.config.registry.queryAdapter(root, ISupportStorage)
        self.failUnless(ISupportStorage.providedBy(adapter))


class FeedEntryTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.site.models.support_storage import SupportRequest
        return SupportRequest

    def test_interface(self):
        from voteit.site.models.interfaces import ISupportRequest
        obj = self._cut('message')
        self.assertTrue(verifyObject(ISupportRequest, obj))

    def test_construction(self):
        meeting = object()
        obj = self._cut('message', subject='subject', name='name', email='email', meeting=meeting)
        self.assertTrue(isinstance(obj.created, datetime))
        self.assertEqual(obj.message, 'message')
        self.assertEqual(obj.subject, 'subject')
        self.assertEqual(obj.name, 'name')
        self.assertEqual(obj.email, 'email')
        self.assertEqual(obj.meeting, meeting)

    def test_factory_registered_on_scan(self):
        self.config.scan('voteit.site.models.support_storage')
        
        factory = self.config.registry.queryUtility(IFactory, 'SupportRequest')
        self.failUnless(IFactory.providedBy(factory))
        obj = factory('message')
        self.failUnless(obj)
        obj = createObject('SupportRequest', 'message')
        self.failUnless(obj)