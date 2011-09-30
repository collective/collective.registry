from zope import interface
from plone.registry import interfaces
from plone.app.registry import Registry
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from plone.registry.recordsproxy import RecordsProxy

ATTRIBUTE_NAME = 'contextual_registry'

class ContextualRegistry(object):
    """The configuration registry
    """
    interface.implements(interfaces.IRegistry)
    def __init__(self, context):
        self.context = context
        self.registry = getattr(self.context, ATTRIBUTE_NAME, None)
    
    def initialize_registry(self):
        if self.registry is None:
            registry = Registry(ATTRIBUTE_NAME)
            setattr(self.context, ATTRIBUTE_NAME, registry)
            self.registry = getattr(self.context, ATTRIBUTE_NAME)

    @property
    def records(self):
        """
        records = schema.Dict(
            title=u"The records of the registry",
            key_type=schema.DottedName(
                    title=u"Name of the record",
                    description=u"By convention, this should include the "
                                 "package name and optionally an interface "
                                 "named, if the record can be described by a "
                                 "field in an interface (see also "
                                 "registerInterface() below), e.g. "
                                 "my.package.interfaces.IMySettings.somefield.",
                ),
            value_type=schema.Object(
                    title=u"The record for this name",
                    schema=IRecord,
                ),
        )
        """
        if self.registry is None:
            return {}
        return self.registry.records

    def __getitem__(self, key):
        """Get the value under the given key. A record must have been
        installed for this key for this to be valid. Otherwise, a KeyError is
        raised.
        """
        if self.registry is None:
            raise KeyError('%s do not exist, no registry on current context %s'%(key, self.context))
        return self.registry.__getitem__(key)

    def get(self, key, default=None):
        """Attempt to get the value under the given key. If it does not
        exist, return the given default.
        """
        if self.registry is None:
            return default
        return self.registry.get(key, default=default)

        
    def __setitem__(self, key, value):
        """Set the value under the given key. A record must have been
        installed for this key for this to be valid. Otherwise, a KeyError is
        raised. If value is not of a type that's allowed by the record, a
        ValidationError is raised.
        """
        if self.registry is None:
            self.initialize_registry()
        return self.registry.__setitem__(key, value)

    def __contains__(self, key):
        """Determine if the registry contains a record for the given key.
        """
        if self.registry is None:
            return False

        return self.registry.__contains__(key)

    def forInterface(self, interface, check=True, omit=(), prefix=None):
        """Get an IRecordsProxy for the given interface. If `check` is True,
        an error will be raised if one or more fields in the interface does
        not have an equivalent setting.
        """
        if self.registry is None and not check:
            #return empty recordsproxy
            return RecordsProxy(self, interface, omitted=omit, prefix=prefix)
        elif self.registry is None and check:
            raise KeyError()
        return self.registry.forInterface(interface, check=check, omit=omit,
                                          prefix=prefix)
        

    def registerInterface(self, interface, omit=(), prefix=None):
        """Create a set of records based on the given interface. For each
        schema field in the interface, a record will be inserted with a
        name like `${interface.__identifier__}.${field.__name__}`, and a
        value equal to default value of that field. Any field with a name
        listed in `omit`, or with the `readonly` property set to True, will
        be ignored. Supply an alternative identifier with `prefix`.
        """
        if self.registry is None:
            self.initialize_registry()
        return self.registry.registerInterface(interface, omit=omit, 
                                               prefix=prefix)


class ContextualRegistryInitializer(BrowserView):
    """A view to initialize the registry over the context"""
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def initialize(self):
        registry = interfaces.IRegistry(self.context)
        if hasattr(registry, 'initialize_registry'):
            registry.initialize_registry()
            url = self.context.absolute_url()+'/'+ATTRIBUTE_NAME+'/view'
        else:
            msg = u"no initialize_registry method on this context"
            IStatusMessage(self.request).add(msg, type="error")
            url = self.context.absolute_url()
        self.request.response.redirect(url)
    
    def __call__(self):
        self.initialize()
