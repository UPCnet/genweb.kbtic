from five import grok
from plone import api
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from plone.batching import Batch
from genweb.kbtic.interface import IGenwebKbticLayer
from Products.Five.browser import BrowserView
from datetime import datetime
from DateTime import DateTime


class MakeObsolets(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        catalog = getToolByName(portal, 'portal_catalog')
        end = DateTime('2016/12/31 23:59:59')

        date_range_query = { 'query':end, 'range': 'max'}

        items = catalog.queryCatalog(
            {"portal_type":"KbticDocument",
             "modified" : date_range_query,
             "sort_order":"reverse"
        })

        for i in items:
            obj = i.getObject()
            print(obj)
            obj.obsolete = True
            obj.reindexObject()
        return "ok"


class ListingKbticDocs(grok.View):
    """ Filtered content search view for every folder. """
    grok.context(Interface)
    grok.name('listingkbtic')
    grok.template("listingkbtic")
    grok.require('zope2.View')
    grok.layer(IGenwebKbticLayer)

    def update(self):
        self.query = self.request.form.get('q', '')
        self.obsolete = self.request.form.get('o', '')
        if self.request.form.get('t', ''):
            self.tags = [v for v in self.request.form.get('t').split(',')]
        else:
            self.tags = []

    def get_batched_contenttags(self, query=None, batch=True, b_size=10, b_start=0):
        pc = getToolByName(self.context, "portal_catalog")
        path = self.context.getPhysicalPath()
        path = "/".join(path)
        r_results = pc.searchResults(path=path)
        batch = Batch(r_results, b_size, b_start)
        return batch

    def get_contenttags_by_query(self):
        pc = getToolByName(self.context, "portal_catalog")
        path = self.context.getPhysicalPath()
        path = "/".join(path)

        def quotestring(s):
            return '"%s"' % s

        def quote_bad_chars(s):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                s = s.replace(char, quotestring(char))
            return s

        if not self.query and not self.tags:
            return self.getContent()

        if not self.query == '':
            multispace = u'\u3000'.encode('utf-8')
            for char in ('?', '-', '+', '*', multispace):
                self.query = self.query.replace(char, ' ')

            query = self.query.split()
            query = " AND ".join(query)
            query = quote_bad_chars(query) + '*'

            if self.tags:
                if not self.obsolete == '':
                    r_results = pc.searchResults(path={'query': path},
                                                 SearchableText=query,
                                                 Subject={'query': self.tags, 'operator': 'and'},
                                                 )
                else:
                    r_results = pc.searchResults(path={'query': path},
                                                 SearchableText=query,
                                                 Subject={'query': self.tags, 'operator': 'and'},
                                                 obsolete=False
                                                 )
            else:
                if not self.obsolete == '':
                    r_results = pc.searchResults(path={'query': path},
                                                 SearchableText=query
                                                 )
                else:
                    r_results = pc.searchResults(path={'query': path},
                                                 SearchableText=query,
                                                 obsolete=False
                                                 )

            return r_results
        else:
            if not self.obsolete == '':
                r_results = pc.searchResults(path={'query': path},
                                             Subject={'query': self.tags, 'operator': 'and'})
            else:
                r_results = pc.searchResults(path={'query': path},
                                             Subject={'query': self.tags, 'operator': 'and'},
                                             obsolete=False
                                             )

            return r_results

    def get_tags_by_query(self):
        pc = getToolByName(self.context, "portal_catalog")

        def quotestring(s):
            return '"%s"' % s

        def quote_bad_chars(s):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                s = s.replace(char, quotestring(char))
            return s

        if not self.query == '':
            multispace = u'\u3000'.encode('utf-8')
            for char in ('?', '-', '+', '*', multispace):
                self.query = self.query.replace(char, ' ')

            query = self.query.split()
            query = " AND ".join(query)
            query = quote_bad_chars(query)
            path = self.context.absolute_url_path()

            r_results = pc.searchResults(path={'query': path, 'depth': 2},
                                         Subject=query)

            return r_results
        else:
            return self.get_batched_contenttags(query=None, batch=True, b_size=10, b_start=0)

    def get_container_path(self):
        return self.context.absolute_url()

    def getContent(self):
        portal = api.portal.get()
        catalog = getToolByName(portal, 'portal_catalog')
        path = self.context.getPhysicalPath()
        path = "/".join(path)
        if self.obsolete == '1':
            items = catalog.searchResults(path={'query': path, 'depth': 2},
                                          sort_on='modified',
                                          sort_order='reverse',
                                          obsolete=True,)
        else:
            items = catalog.searchResults(path={'query': path, 'depth': 2},
                                          sort_on='modified',
                                          sort_order='reverse',
                                          obsolete=False,)

        return items


class SearchFilteredContentAjax(ListingKbticDocs):
    """ Ajax helper for filtered content search view for every folder. """
    grok.context(Interface)
    grok.name('search_filtered_content_ajax')
    grok.template("searchfilteredcontentajax")
    grok.require('zope2.View')
    grok.layer(IGenwebKbticLayer)
