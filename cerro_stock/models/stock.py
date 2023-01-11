from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    petitioner_id = fields.Many2one('hr.employee', string='Petitioner')

    def button_validate(self):
        """Overwrite the methods to update the product quantities
        When the picking is from the warehouse to the events the quantity by state is updated reducing the values by state
        When the picking is from the events to the warehouse the quantity by state is updated increasing the values by state
        """
        res = super(StockPicking, self).button_validate()
        for move in self.move_lines:
            if not move.move_state_validation:
                if move.location_dest_id.id == self.env.ref('cerro_stock.stock_location_events').id:
                    print(move.product_id.product_good_state_qty)
                    move.product_id.product_good_state_qty -= move.product_good_state_qty
                    move.product_id.product_regular_state_qty -= move.product_regular_state_qty
                    move.product_id.product_bad_state_qty -= move.product_bad_state_qty
                    move.product_id.product_lost_state_qty -= move.product_lost_state_qty
                elif move.location_id.id == self.env.ref('cerro_stock.stock_location_events').id :
                    move.product_id.product_good_state_qty += move.product_good_state_qty
                    move.product_id.product_regular_state_qty += move.product_regular_state_qty
                    move.product_id.product_bad_state_qty += move.product_bad_state_qty
                    move.product_id.product_lost_state_qty += move.product_lost_state_qty
                move.move_state_validation = True
        return res
    

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_good_state_qty = fields.Integer(string='Good State Quantity')
    product_regular_state_qty = fields.Integer(string='Regular State Quantity')
    product_bad_state_qty = fields.Integer(string='Bad State Quantity')
    product_lost_state_qty = fields.Integer(string='Lost State Quantity')
    move_state_validation = fields.Boolean('Move State Validation', default=False, copy=False)

    def action_show_state_qtys(self):
        """ Returns an action that will open a form view (in a popup) allowing to work on all the
        move lines of a particular move. This form view is used when "show operations" is not
        checked on the picking type.
        """
        self.ensure_one()
        
        view = self.env.ref('cerro_stock.view_stock_move_state_qtys_form')

        return {
            'name': _('Detailed Operations'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.move',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
        }
    
