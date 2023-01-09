from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    shelf = fields.Char('Shelf')
    
    product_good_state_qty = fields.Integer('Product Good State')
    product_regular_state_qty = fields.Integer('Product Regular State')
    product_bad_state_qty = fields.Integer('Product Bad State')
    product_lost_state_qty = fields.Integer('Product Lost State')

    @api.onchange('product_good_state_qty', 'product_regular_state_qty', 'product_bad_state_qty', 'product_lost_state_qty')
    def _onchange_product_state(self):
        """This method check if the sum of all states is less or equal to the available quantity."""
        self.ensure_one()
        if self.product_good_state_qty + self.product_regular_state_qty + self.product_bad_state_qty + self.product_lost_state_qty > self.qty_available:
            raise UserError(_('The sum of all states cannot be greater than the available quantity.'))

    def transfer_between_states(self):
        """This method calls the wizard to transfer certain quantity of product
        from one state to another."""
        self.ensure_one()
        return {
            'name': 'Transfer Between States',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard.product.product.transfer_between_states',
            'target': 'new',
            'context': {
                'default_product_id': self.id,
            },
        }


