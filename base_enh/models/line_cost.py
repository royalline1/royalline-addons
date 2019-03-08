# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AdditionalCost(models.Model):
    _name = 'additional.cost'
    
    
    product_id = fields.Many2one('product.product', string='Additional Name', required=True ,domain=[('is_discount', '=', True)])
    cost = fields.Float()
    line_cost_id = fields.Many2one('line.cost' ,required=True)
    
    
class LineCostLine(models.Model):
    _name = 'line.cost.line'
    
    container_id = fields.Many2one('container.size', 'Container', required=True)
    min_qty = fields.Integer('Minimum Quantity', required=True)
    agency = fields.Float('Agency', compute="_compute_agency",store=True)
    transport_price = fields.Float('Transport Price', required=True)
    product_id = fields.Many2one('product.product', string='Name Of Discount', domain=[('is_discount', '=', True)])
    value = fields.Float('Discount Value', required=True)
    line_cost_id = fields.Many2one('line.cost', required=True)
    container_ids = fields.Many2many('container.size',compute ='_compute_container_ids')
    total = fields.Float('Total',compute='_compute_total')
    
    @api.depends('agency','transport_price','value')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.agency + rec.transport_price - rec.value
            
            
    @api.depends('line_cost_id','line_cost_id.line_id')
    def _compute_container_ids(self):
        for rec in self:
            rec.container_ids = [(6,0,rec.line_cost_id.line_id.mapped('sea_ids.container_size_id').ids)]
    
    @api.depends('container_id')
    def _compute_agency(self):
        for rec in self:
            if rec.container_id:
                sea_ids =rec.mapped('line_cost_id.line_id.sea_ids').filtered(lambda x:x.container_size_id.id == rec.container_id.id)
                if sea_ids:
                    rec.agency = sea_ids[0].agency
                else :
                    rec.agency = 0.0
            
            else :
                rec.agency = 0.0


class LineCost(models.Model):
    _name = 'line.cost'
    _rec_name = 'line_id'
    
    line_id = fields.Many2one('res.partner', string="Shipping Line", required=True,domain=[('company_type', '=', 'company'),('is_sea_line', '=', True)])
    quot_number = fields.Char(string="Quotation Number", required=True)
    date = fields.Date('Date', required=True)
    country_loding_id = fields.Many2one('res.country', string="Country Of Loading", required=True)
    state_loding_id = fields.Many2one('res.country.state', string="State Of Loading")
    city_loding_id = fields.Many2one('res.city', string="City Of Loading")
    place_loding_id = fields.Many2one('loading.place', string="Place Of Loading")
    transport_loading_id = fields.Many2one('transport.type', string="Transport Type Of Loading")
    port_loafing_id = fields.Many2one('port', string="POL")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    port_dest_id = fields.Many2one('port', string="POD")
    transport_dest_id = fields.Many2one('transport.type', string="Transport Type Of Destination")
    delivery_place_id = fields.Many2one('delivery.place', 'Place Of Delivery')
    bill_fees = fields.Float('Bill fees',compute='_compute_bill_fees',store=True)
    free_demurrage_and_detention = fields.Integer()
    total_rate = fields.Float('Total Rate')
    transt_time = fields.Integer()
    customer_id = fields.Many2one('res.partner',stirng='Named Account')
    ak = fields.Boolean('FAK',default=True)
    product_id = fields.Many2one('product.product')
    start_date = fields.Date('Start Date')
    expiry_date = fields.Date('Expiry Date')
    note = fields.Text('Notes')
    expired_price = fields.Boolean()
    newxt_price = fields.Boolean()
    line_cost_ids = fields.One2many('line.cost.line','line_cost_id',string="Price")
    additional_cost_ids = fields.One2many('additional.cost','line_cost_id',string="Additional Cost")
    total_cost = fields.Float('Total Cost',compute="_compute_total_cost")
    product_discount_id = fields.Many2one('product.product', string='Additional Discount' ,domain=[('is_discount', '=', True)])
    discount = fields.Float(default=0.0)
    
    @api.depends('line_id')
    def _compute_bill_fees(self):
        for rec in self:
            if rec.line_id:
                rec.bill_fees = rec.line_id.bill_fees
            else:
                rec.bill_fees = 0.0
                
                
    @api.depends('discount','bill_fees','total_rate','line_cost_ids','line_cost_ids.total','additional_cost_ids','additional_cost_ids.cost')
    def _compute_total_cost(self):
        for rec in self:
            total_additional_cost = sum(rec.mapped('additional_cost_ids.cost')+[0])
            total_price = sum(rec.mapped('line_cost_ids.total')+[0])
            rec.total_cost = total_additional_cost + total_price + rec.total_rate + rec.bill_fees - rec.discount
            
    @api.onchange('line_id')     
    def onchange_line_id(self):
        self.line_cost_ids = [(6,0,[])]
    
    
    
    
    
    
