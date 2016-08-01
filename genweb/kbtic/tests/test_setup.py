# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from genweb.kbtic.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of genweb.kbtic into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if genweb.kbtic is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('genweb.kbtic'))

    def test_uninstall(self):
        """Test if genweb.kbtic is cleanly uninstalled."""
        self.installer.uninstallProducts(['genweb.kbtic'])
        self.assertFalse(self.installer.isProductInstalled('genweb.kbtic'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IGenwebKbticLayer is registered."""
        from genweb.kbtic.interfaces import IGenwebKbticLayer
        from plone.browserlayer import utils
        self.failUnless(IGenwebKbticLayer in utils.registered_layers())
