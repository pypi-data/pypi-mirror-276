# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class ProjectInvoicePricelistTestCase(ModuleTestCase):
    "Test Project Invoice Pricelist module"
    module = 'project_invoice_pricelist'


del ModuleTestCase
