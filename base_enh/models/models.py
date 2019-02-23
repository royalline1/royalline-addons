# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FinalDest(models.Model):
    _name = 'final.dest'
    _rec_name = 'zip'
    
    zip = fields.Integer('ZIP Code',required=True)
    counrty_id = fields.Many2one('res.country',required=True)
    city_id = fields.Many2one('res.city',required=True)
    state_id = fields.Many2one('res.country.state',required=True)
    address = fields.Text('Address',required=True)
    
class Port(models.Model):
    _name = 'port'

    name = fields.Char(string='Name',required=True)
    code = fields.Char(string='Code')
    type = fields.Selection([('air',"Air"),('sea',"Sea"),('dry',"Dry")],required=True)
    country_id = fields.Many2one('res.country',stirng="Country",required=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_shipper = fields.Boolean('Is Shipper')
    is_consignee = fields.Boolean('Is Consignee')
    is_notify = fields.Boolean('Is notify Party')
    is_agent = fields.Boolean('Is Agent')
    customer_class_id = fields.Many2one('customer.class')
    
    
    @api.onchange('city_id')
    def _onchange_city_id(self):
        pass
        