# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    price_list = fields.Many2One('product.price_list', 'Price List',
        domain=[('company', '=', Eval('company'))],
        help='Use the first pricelist found in following precedence:\n\n'
        '- Pricelist of the task\n'
        '- Pricelist of the parent project\n'
        '- Pricelist of the party\n'
        '- Pricelist of sale configuration')
    price_list_used = fields.Function(fields.Many2One('product.price_list',
            'Price List Used'), 'on_change_with_price_list_used')

    @fields.depends(
        'company', 'price_list', 'parent', '_parent_parent.parent', 'party')
    def on_change_with_price_list_used(self, name=None):
        pool = Pool()
        Configuration = pool.get('sale.configuration')
        if self.price_list:
            return self.price_list.id
        parent_project = self.__class__.search([
                ('parent', 'parent_of', [self.id]),
                ('parent', '=', None),
                ])
        if parent_project:
            project = parent_project[0]
            if project.price_list:
                return project.price_list.id
            elif project.party and project.party.sale_price_list:
                return project.party.sale_price_list.id
        elif self.party and self.party.sale_price_list:
            return self.party.sale_price_list.id
        else:
            config = Configuration(1)
            price_list = config.get_multivalue(
                'sale_price_list',
                company=self.company.id if self.company else None)
            return price_list and price_list.id

    @fields.depends('party')
    def on_change_party(self):
        self.price_list = None
        if self.party and self.party.sale_price_list:
            self.price_list = self.party.sale_price_list

    def _group_lines_to_invoice_key(self, line):
        key = super()._group_lines_to_invoice_key(line)
        key += (('price_list', self.price_list_used),)
        return key

    def _get_lines_to_invoice(self):
        lines = super()._get_lines_to_invoice()
        for line in lines:
            line['price_list'] = self.price_list_used
        return lines

    @property
    def invoice_unit_price(self):
        pool = Pool()
        Product = pool.get('product.product')

        if self.price_list_used:
            with Transaction().set_context({
                    'price_list': self.price_list_used.id,
                    }):
                prices = Product.get_sale_price([self.product], 0)
                if prices:
                    return list(prices.values())[0]
        return super().invoice_unit_price

    def _get_invoice_line(self, key, invoice, lines):
        pool = Pool()
        Product = pool.get('product.product')

        # Subject to refactoration, depends on #4709
        invoice_line = super()._get_invoice_line(
            key, invoice, lines)

        pricelist = key['price_list']
        if pricelist:
            with Transaction().set_context({
                    'price_list': pricelist.id,
                    'customer': self.party.id,
                    }):
                prices = Product.get_sale_price([self.product], 0)
                invoice_line.unit_price = prices[self.product.id]
        return invoice_line
