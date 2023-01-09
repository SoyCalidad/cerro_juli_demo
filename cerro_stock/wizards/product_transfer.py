from odoo import api, fields, models, _
from odoo.exceptions import UserError

class WizardProductProductTransferBetweenStates(models.Model):
    _name = 'wizard.product.product.transfer_between_states'
    _description = 'Wizard Product Product Transfer Between States'
    
    product_id = fields.Many2one('product.product', string='Product')
    from_state = fields.Selection([('good', 'Good'), ('regular', 'Regular'), ('bad', 'Bad'), ('lost', 'Lost')], string='From State')
    to_state = fields.Selection([('good', 'Good'), ('regular', 'Regular'), ('bad', 'Bad'), ('lost', 'Lost')], string='To State')
    quantity = fields.Integer('Quantity')

    def transfer_between_states(self):
        """This method transfers the quantity of product from one state to
        another."""
        self.ensure_one()
        if self.from_state == self.to_state:
            raise UserError(_('From state and to state cannot be the same.'))
        if self.from_state == 'good':
            if self.quantity > self.product_id.product_good_state_qty:
                raise UserError(_('You cannot transfer more product than the quantity in good state.'))
            self.product_id.product_good_state_qty -= self.quantity
        elif self.from_state == 'regular':
            if self.quantity > self.product_id.product_regular_state_qty:
                raise UserError(_('You cannot transfer more product than the quantity in regular state.'))
            self.product_id.product_regular_state_qty -= self.quantity
        elif self.from_state == 'bad':
            if self.quantity > self.product_id.product_bad_state_qty:
                raise UserError(_('You cannot transfer more product than the quantity in bad state.'))
            self.product_id.product_bad_state_qty -= self.quantity
        elif self.from_state == 'lost':
            if self.quantity > self.product_id.product_lost_state_qty:
                raise UserError(_('You cannot transfer more product than the quantity in lost state.'))
            self.product_id.product_lost_state_qty -= self.quantity
        if self.to_state == 'good':
            self.product_id.product_good_state_qty += self.quantity
        elif self.to_state == 'regular':
            self.product_id.product_regular_state_qty += self.quantity
        elif self.to_state == 'bad':
            self.product_id.product_bad_state_qty += self.quantity
        elif self.to_state == 'lost':
            self.product_id.product_lost_state_qty += self.quantity