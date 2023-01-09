from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def send_to_event(self):
        """This method confirms the sale order and creates a stock picking
        as internal transfer from main inventory to the events location."""
        self.ensure_one()
        self.action_confirm()

        picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_internal').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('cerro_stock.stock_location_events').id,
            'move_lines': [(0, 0, {
                'name': self.name,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom.id,
                'product_uom_qty': line.product_uom_qty,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            }) for line in self.order_line],
        })

        return {
            'name': 'Events',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'target': 'current',
            'domain': [('picking_type_id', '=', self.env.ref('stock.picking_type_internal').id)],
        }
        
    