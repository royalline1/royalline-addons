# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AdditionalCost(models.Model):
    _name = 'additional.cost'
    
    
    product_id = fields.Many2one('product.product', string='Discount', required=True ,domain=[('is_discount', '=', True)])
    cost = fields.Float()
    line_cost_id = fields.Many2one('line.cost')
    
    
class LineCostLine(models.Model):
    _name = 'line.cost.line'
    
    container_id = fields.Many2one('container.size', 'Container')
    min_qty = fields.Integer('Minimum Quantity')
    agency = fields.Float('Agency')
    transport_price = fields.Float('Transport Price')
    product_id = fields.Many2one('product.product', string='Discount', domain=[('is_discount', '=', True)])
    value = fields.Float('Value')
    line_cost_id = fields.Many2one('line.cost')


class LineCost(models.Model):
    _name = 'line.cost'
    
    line_id = fields.Many2one('res.partner', string="name", required=True)
    quot_number = fields.Char(string="Quotation Number", required=True)
    date = fields.Date('Date', required=True)
    country_loding_id = fields.Many2one('res.country', string="Country Of Loading", required=True)
    state_loding_id = fields.Many2one('res.country.state', string="State Of Loading")
    city_loding_id = fields.Many2one('res.city', string="City Of Loading")
    place_loding_id = fields.Many2one('res.place', string="Place Of Loading")
    transport_loading_id = fields.Many2one('transport.type', string="Transport Type Of Loading")
    port_loafing_id = fields.Many2one('port', string="POL")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    port_dest_id = fields.Many2one('port', string="POD")
    transport_dest_id = fields.Many2one('transport.type', string="Transport Type Of Destination")
    delivery_place_id = fields.Many2one('delivery.place', 'Delivery Of Place')
    bill_fees = fields.Float('Bill fees',related='line_id.bill_fees',readonly=True,store=True)
    free_demurrage_and_detention = fields.Integer()
    total_rate = fields.Float('Total Rate')
    transt_time = fields.Integer()
    costumer_id = fields.Many2one('res.partner',stirng='Named Account',domain=[('customer','=',True)])
    ak = fields.Boolean('AK',default=True)
    product_id = fields.Many2one('product.product')
    start_date = fields.Date('Start Date')
    expiry_date = fields.Date('Expiry Date')
    note = fields.Text('Notes')
    expired_price = fields.Boolean()
    newxt_price = fields.Boolean()
    line_cost_ids = fields.One2many('line.cost.line','line_cost_id',string="Price")
    additional_cost_ids = fields.One2many('additional.cost','line_cost_id',string="Additional Cost")
    
    
    
    
    
    
    
