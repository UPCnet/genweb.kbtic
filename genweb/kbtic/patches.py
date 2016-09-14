from plone.memoize.instance import memoize
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.navtree import buildFolderTree
from zope.component import getMultiAdapter
from Acquisition import aq_inner


@memoize
def getNavTree(self, _marker=None):
    if _marker is None:
        _marker = []
    context = aq_inner(self.context)
    queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
    queryBuilder.query['portal_type'] = ['Folder']
    strategy = getMultiAdapter((context, self.data), INavtreeStrategy)

    return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)
