# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from five import grok
from genweb.kbtic import _
from plone.directives import form
from plone.app.textfield import RichText
from plone.directives import dexterity
from zope import schema


class IKbticDocument(form.Schema):
    """Description of the Example Type"""

    dexteritytextindexer.searchable('body')
    body = RichText(
        title=_(u"Body text"),
        description=_(u""),
        required=False,
    )

    obsolete = schema.Bool(
        title=_(u"Document obsolet?"),
        description=_(u"Si el document està marcat com a obsolet, no sortirà a les cerques."),
        required=False,
        default=False,
    )


class View(grok.View):
    grok.context(IKbticDocument)
    grok.template('kbtic_view')


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(IKbticDocument)
