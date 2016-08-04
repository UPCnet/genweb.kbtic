# -*- coding: utf-8 -*-
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from zope.formlib import form


class IEtiquetesHOMEPortlet(IPortletDataProvider):
    """ Defines a new portlet
    """


class Assignment(base.Assignment):
    """ Assigner for portlet. """
    implements(IEtiquetesHOMEPortlet)
    title = _(u"Etiquetes HOME", default=u'Etiquetes HOME')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('templates/etiquetesHOME.pt')

    def mostrarEtiquetes(self):
        """ Etiquetes del sistema
        """
        indexName='Subject'
        catalog = getToolByName(self, 'portal_catalog')
        keywords = list(catalog.uniqueValuesFor(indexName))
        keywords.sort(key=lambda x:x.lower())
        return keywords


    def getKeywordIndexes(self):
        """Gets a list of indexes from the catalog. Uses config.py to choose the
        meta type and filters out a subset of known indexes that should not be
        managed.
        """
        IGNORE_INDEXES = [
            'object_provides',
            'allowedRolesAndUsers',
            'getRawRelatedItems',
            'getEventType',
        ]
        catalog = getToolByName(self, 'portal_catalog')
        idxs = catalog.index_objects()
        idxs = [i.id for i in idxs if i.meta_type == 'KeywordIndex' and
                i.id not in IGNORE_INDEXES]
        idxs.sort()
        return idxs


class AddForm(base.AddForm):
    form_fields = form.Fields(IEtiquetesHOMEPortlet)
    label = _(u"Afegeix portlet de etiquetes kbtic a la home")
    description = _(u"Aquest portlet mostra les etiquetes del site")

    def create(self, data):
        # s'invoca despres de __init__ en clicar Desa
        assignment = Assignment(**data)
        return assignment


class EditForm(base.EditForm):
    form_fields = form.Fields(IEtiquetesHOMEPortlet)
    label = _(u"Edita portlet de etiquetes kbtic a la home")
    description = _(u"Aquest portlet edita les etiquetes del site")
