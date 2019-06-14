# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AdditionalCost(models.Model):
    _name = 'additional.cost'
    
    
    product_id = fields.Many2one('product.product', string='Additional Name', required=True ,domain=[('is_add_cost', '=', True)])
    cost = fields.Float(required=True)
    line_cost_id = fields.Many2one('line.cost' ,required=True)
    
    _sql_constraints = [('check_additional_cost_cost', 'CHECK(cost > 0)', 'The additional cost must be greater than zero.')]
    
    
class LineCostLine(models.Model):
    _name = 'line.cost.line'
    _rec_name = "sea_lines_id"
    
    sea_lines_id = fields.Many2one('sea.lines', 'Container', required=True)
    partner_id = fields.Many2one('res.partner',related="line_cost_id.line_id")
    min_qty = fields.Integer('Minimum Quantity', required=True)
    agency = fields.Float('Agency', related="sea_lines_id.agency",store=True)
    transport_loading_price = fields.Float()
    transport_discharge_price = fields.Float()
    insurance_price = fields.Float()
    clearance_price = fields.Float()
    is_loading = fields.Boolean()
    is_discharge = fields.Boolean()
    is_clearance_cost = fields.Boolean()
    is_insurance_cost = fields.Boolean()
    type = fields.Selection([('loading','Loading'),('discharg','Discharg')])
    product_id = fields.Many2one('product.product', string='Name Of Discount', domain=[('is_discount', '=', True)])
    value = fields.Float('Discount Value')
    rate = fields.Float('Rate')
    line_cost_id = fields.Many2one('line.cost', required=True)
    total = fields.Float('Total',compute='_compute_total')
    
    @api.depends('agency','transport_loading_price','value','rate','transport_discharge_price','clearance_price','insurance_price')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.clearance_price + rec.insurance_price + rec.agency + rec.rate+ rec.transport_discharge_price + rec.transport_loading_price - rec.value
            
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        print(self._context)
        print(args)
        return super(LineCostLine, self)._search( args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)

    @api.onchange('product_id') 
    def erase_value_discount(self):
        """Erase discount value if product name changed"""
        for rec in self:
            rec.value=u''
        

class LineCost(models.Model):
    _name = 'line.cost'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'line_id'
    
    line_id = fields.Many2one('res.partner', string="Shipping Line", required=True,domain=[('company_type', '=', 'company'),('is_sea_line', '=', True)])
    quot_number = fields.Char(string="Quotation Number", required=True)
    date = fields.Date('Date', required=True)
    country_loading_id = fields.Many2one('res.country', string="Country Of Loading", required=True)
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading")
    city_loading_id = fields.Many2one('res.city', string="City Of Loading")
    place_loading_id = fields.Many2one('res.place', string="Place Of Loading")
    transport_loading_id = fields.Many2one('transport.type', string="Transport Type Of Loading")
    port_loading_id = fields.Many2one('port', string="POL")
    terminal_loading_id = fields.Many2one('res.place', string="Terminal of Loading")
    
    is_same_country = fields.Boolean('Is Same Country', default=True)
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    terminal_des_same_id = fields.Many2one('res.place', string="Terminal of Discharge")
    
    country_diff_dest_id = fields.Many2one('res.country', string="Country Of Last Destination")
    state_diff_dest_id = fields.Many2one('res.country.state', string="State Of Last Destination")
    city_diff_dest_id = fields.Many2one('res.city', string="City Of Last Destination")
    place_diff_dest_id = fields.Many2one('res.place', string="Place Of Last Destination")
    port_diff_id = fields.Many2one('port', string="POD Last Country")
    delivery_diff_place_id = fields.Many2one('res.place', 'Place Of Last Delivery')
    terminal_des_diff_id = fields.Many2one('res.place', string="Terminal of delivery")
    
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    port_dest_id = fields.Many2one('port', string="POD")
    transport_dest_id = fields.Many2one('transport.type', string="Transport Type Of Destination")
    delivery_place_id = fields.Many2one('res.place', 'Place Of Delivery')
    bill_fees = fields.Float('Bill fees',compute='_compute_bill_fees',store=True)
    free_demurrage_and_detention = fields.Integer()
    transt_time = fields.Integer()
    customer_id = fields.Many2one('res.partner',stirng='Named Account')
    fak = fields.Boolean('FAK',default=True)
    product_id = fields.Many2one('product.product')
    commodity_id = fields.Many2one('commodity')
    start_date = fields.Date('Start Date')
    expiry_date = fields.Date('Expiry Date')
    note = fields.Text('Notes')
    expired_price = fields.Boolean(compute='_compute_is_expired')
    next_price = fields.Boolean(compute='_compute_is_expired')
    line_cost_ids = fields.One2many('line.cost.line','line_cost_id',string="Price")
    additional_cost_ids = fields.One2many('additional.cost','line_cost_id',string="Additional Cost")
    product_discount_id = fields.Many2one('product.product', string='Additional Discount' ,domain=[('is_discount', '=', True)])
    discount = fields.Float(default=0.0)
    
    @api.onchange('fak')
    def _onchange_fak(self):
        self.commodity_id = False
        
        
    #   loaded country related
    @api.onchange('country_loading_id')
    def erase_related_addr(self):
        self.state_loading_id = u''
        self.city_loading_id= u''
        self.place_loading_id = u''
        self.port_loading_id = u''
        self.terminal_loading_id = u''
    
    @api.onchange('state_loading_id')
    def erase_related_addr_three(self):
        self.city_loading_id= u''
        self.place_loading_id = u''
    
    @api.onchange('city_loading_id')
    def erase_related_addr_four(self): 
        self.place_loading_id = u''
        
    @api.onchange('port_loading_id')
    def erase_related_addr_six(self): 
        self.terminal_loading_id = u''
    
#   Destination country related
    @api.onchange('country_dest_id')
    def erase_related_addr_des(self):
        self.state_dest_id = u''
        self.city_dest_id= u''
        self.place_dest_id = u''
        self.port_dest_id = u''
        self.terminal_des_same_id = u''
        self.delivery_place_id = u''
    
    @api.onchange('state_dest_id')
    def erase_related_addr_three_des(self):
        self.city_dest_id= u''
        self.place_dest_id = u''
    
    @api.onchange('city_dest_id')
    def erase_related_addr_four_des(self): 
        self.place_dest_id = u''
        
    @api.onchange('port_dest_id')
    def erase_related_addr_six_des(self): 
        self.terminal_des_same_id = u''  
    
    #   Last country related
    @api.onchange('country_diff_dest_id')
    def erase_related_addr_last(self):
        self.state_diff_dest_id = u''
        self.city_diff_dest_id= u''
        self.place_diff_dest_id = u''
        self.port_diff_id = u''
        self.terminal_des_diff_id = u''
        self.delivery_diff_place_id = u''
    
    @api.onchange('state_diff_dest_id')
    def erase_related_addr_three_last(self):
        self.city_diff_dest_id= u''
        self.place_diff_dest_id = u''
    
    @api.onchange('city_diff_dest_id')
    def erase_related_addr_four_last(self): 
        self.place_diff_dest_id = u''
        
    @api.onchange('port_diff_id')
    def erase_related_addr_six_last(self): 
        self.terminal_des_diff_id = u''  
    
    @api.multi
    @api.depends('expiry_date','start_date')
    def _compute_is_expired(self):
        for rec in self:
            if rec.expiry_date and rec.expiry_date < fields.Date.today():
               rec.expired_price = True 
            else:
               rec.expired_price = False
            if rec.start_date and rec.start_date > fields.Date.today():
               rec.next_price = True 
            else:
               rec.next_price = False
               
   
    @api.constrains('expiry_date','start_date')
    def _expired_date(self):
        for rec in self:
            if rec.expiry_date < rec.start_date:
               raise UserError("'Expiry date' should be greater than 'Start date'")
           
    @api.constrains('transt_time')
    def _transit_time(self):
        for rec in self:
            if rec.transt_time <= 0:
               raise UserError("Transit time should be more than Zero!")

    @api.constrains('discount')
    def discount_value(self):
        for rec in self:
            if rec.discount < 0:
                raise UserError(" 'Discount' value should be greater than or equal zero.")
    
    @api.onchange('product_discount_id')
    def erase_discount_value(self):
        for rec in self:
            rec.discount=u''
                
    
    
    @api.model_create_multi
    @api.returns('self', lambda value:value.id)
    def create(self, vals_list):
        res = super(LineCost, self).create( vals_list)
        for rec in res:
            if not rec.place_dest_id:
                rec.line_cost_ids.write({'is_discharge':False,'transport_discharge_price':0.0})
            if not rec.place_loading_id:
                rec.line_cost_ids.write({'is_loading':False,'transport_loading_price':0.0})
        return res
    
    @api.multi
    def write(self, vals):
        res = super(LineCost, self).write(vals)
        for rec in self:
            if not rec.place_dest_id:
                rec.line_cost_ids.write({'is_discharge':False,'transport_discharge_price':0.0})
            if not rec.place_loading_id:
                rec.line_cost_ids.write({'is_loading':False,'transport_loading_price':0.0})
        return res
    @api.depends('line_id')
    def _compute_bill_fees(self):
        for rec in self:
            if rec.line_id:
                rec.bill_fees = rec.line_id.bill_fees
            else:
                rec.bill_fees = 0.0
                
                
            
    @api.onchange('line_id')     
    def onchange_line_id(self):
        self.line_cost_ids = [(6,0,[])]
    
    
    
    
    
    
