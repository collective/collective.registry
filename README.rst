Introduction
============

This add-on extends plone.app.registry by adding a contextual registry
which can be used over any object. It has been created to store view
configuration throw the add-on collective.configviews 2.X

How to use this add-on
======================

As a developer you can get the IRegistry adapter from a content object and next
use it as you want to get/set your configuration stuff.

As a content administrator you can manage the configuration stored in a content
by calling the view $content_url/contextual_registry/view where $content_url must
be replaced by the url of your content item.

How to install
==============

Please follow the official documentation_.

Credits
=======

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to
