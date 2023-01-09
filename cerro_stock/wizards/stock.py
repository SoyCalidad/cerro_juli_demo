from odoo import fields, models

class WizardCerroStock(models.TransientModel):
    _name = 'wizard.cerro_stock'

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    product_ids = fields.Many2many('product.product', string='Products')
    type = fields.Selection([
        ('report_1', 'report 1'),
        ('report_2', 'report 2'),
        ('report_3', 'report 3'),
        ('report_4', 'report 4'),
        ('report_5', 'report 5'),
        ('report_6', 'report 6'),
        ('report_7', 'report 7'),
        ('report_8', 'report 8'),
    ], string='Type')

    def print_report(self):
        data = {
            'product_ids': self.product_ids.ids,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'type': self.type,
        }
        return self.env.ref('cerro_stock.action_report_cerro_stock_{}'.format(self.type)).report_action(self, data=data)