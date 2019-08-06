# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression
from odoo.exceptions import UserError
from os import linesep


class AirLineCost(models.Model):
    _name='air.line.cost'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='air_line_comp_id'
    _description='Airline cost table'
    
    air_line_comp_id=fields.Many2one('res.partner', domain=[('is_air_line','=',True)], required=True)
    quot_no=fields.Char('Quotation Number', required=True)
    date=fields.Date('Date', required=True)
    active=fields.Boolean('Active', default=True)
    is_expired=fields.Boolean('Is Expired')
    is_next=fields.Boolean('Is Next')
#   General Info fields 
    country_loading_id=fields.Many2one('res.country',required=True)
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading")
    city_loading_id = fields.Many2one('res.city', string="City Of Loading")
    place_loading_id = fields.Many2one('res.place', string="Place Of Loading", required=False)
    port_loading_id = fields.Many2one('port', string="POL", required=True)
    terminal_loading_id = fields.Many2one('res.place', string="Terminal of Loading", required=True)
    
    transt_time = fields.Integer(required=True)
    start_date = fields.Date('Start Date')
    expiry_date = fields.Date('Expiry Date')
    
    country_dest_id = fields.Many2one('res.country', string="Country Of Discharge", required=True)
    state_dest_id = fields.Many2one('res.country.state', string="State Of Discharge")
    city_dest_id = fields.Many2one('res.city', string="City Of Discharge")
    place_dest_id = fields.Many2one('res.place', string="Place Of Discharge")
    port_dest_id = fields.Many2one('port', string="POD", required=True)
    terminal_des_same_id = fields.Many2one('res.place', string="Terminal of Discharge")
    
    customer_id = fields.Many2one('res.partner',stirng='Named Account')
    fak = fields.Boolean('FAK',default=True)
    commodity_id = fields.Many2many('commodity')
    commodity_domain_ids = fields.Many2many('commodity', related='customer_id.commodity_ids')
    
#   on2many fields
    air_line_cost_line_ds =fields.One2many('air.line.cost.line','air_line_cost_id') 
    air_line_add_cost_ds =fields.One2many('air.line.addit.cost','air_line_costt_id')
    air_line_note_cost_ds =fields.One2many('air.line.note','air_line_costt_id')
    
class AirLineCostLine(models.Model):
    _name = 'air.line.cost.line'
    _description = "AirLineCostLine"
    
    commodity_id = fields.Many2one('commodity',String='Commodity',required=True)
    package_name = fields.Char()
    quantity = fields.Float()
    operation = fields.Char()
    volume = fields.Float()
    chargeable_weight = fields.Char('Chargeable Weight')
    currency_id = fields.Many2one('res.currency', string="Currency")
    cost = fields.Monetary(required=True)
    total = fields.Monetary('Total')
    air_line_cost_id = fields.Many2one('air.line.cost')
    
class AirlineAdditCost(models.Model):
    _name='air.line.addit.cost'
    _description='AirlineAdditCost'
     
    product_id = fields.Many2one('product.product', string='Product', required=True ,domain=[('is_add_cost', '=', True)])
    currency_id = fields.Many2one('res.currency', string="Currency",required=True)
    cost = fields.Monetary(required=True)
    air_line_costt_id = fields.Many2one('air.line.cost')
     
class AirLineNote(models.Model):
    _name='air.line.note'
    _description='AirLineNote'
    
    note=fields.Text('note')
    air_line_costt_id = fields.Many2one('air.line.cost')
    
    
    
    
    
    
    
    
    
    
    
    
    