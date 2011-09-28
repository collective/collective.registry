from zope import component
from Products.Five.browser import BrowserView
from plone.registry import interfaces
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#
#class RegistryView(BrowserView):
#    """Registry view"""
#
#    __call__ = ViewPageTemplateFile('records.pt')
#
#    def __init__(self, context, request):
#        self.context = context
#        self.request = request
#        self.registry = component.queryAdapter(self.context,
#                                               interfaces.IRegistry)
#    
#    def records(self):
#        return self.registry.records
#    
#    def values(self):
#        return self.registry.records
#    
#    def testit(self):
#        import pdb;pdb.set_trace()
#        self.registry.registerInterface(ExampleSchema)
#        

from zope import interface
from zope import schema

class ExampleSchema(interface.Interface):
    
    foo = schema.Bool(title=u"foo", default=True)

    bar = schema.ASCIILine(title=u"bar", default="aa")
