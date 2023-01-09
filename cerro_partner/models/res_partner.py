from odoo import api, fields, models

class ResPartnerArea(models.Model):
    _name = 'res.partner.area'
    _description = 'Partner Area'

    name = fields.Char(string='Name', required=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    area_id = fields.Many2one('res.partner.area', string='Area')

    