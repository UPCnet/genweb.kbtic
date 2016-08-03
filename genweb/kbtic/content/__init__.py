from zope.interface import implements
from plone.dexterity.content import Item

from genweb.kbtic.content.kbticDocument import IKbticDocument

class KbticDocument(Item):
    implements(IKbticDocument)
