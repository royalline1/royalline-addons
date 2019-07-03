# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AdditionalCost(models.Model):
    _name = 'additional.cost'
    _description = "AdditionalCost"
    
    product_id = fields.Many2one('product.product', string='Additional Name', required=True ,domain=[('is_add_cost', '=', True)])
    cost = fields.Monetary(required=True)
    line_cost_id = fields.Many2one('line.cost' ,required=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    
    @api.constrains('cost')
    def check_cost_value(self):
        """cost value greater than 0"""
        for rec in self:
            if rec.cost == 0 or rec.cost < 0:
                raise UserError("'Cost' value should be greater than 0")
    
#     _sql_constraints = [('check_additional_cost_cost', 'CHECK(cost > 0)', 'The additional cost must be greater than zero.')]
    
    
class LineCostLine(models.Model):
    _name = 'line.cost.line'
    _rec_name = "sea_lines_id"
    _description = "LineCostLine"
    
    sea_lines_id = fields.Many2one('sea.lines', 'Container', required=True)
    partner_id = fields.Many2one('res.partner',related="line_cost_id.line_id")
    min_qty = fields.Integer('Minimum Quantity', required=True)
    agency = fields.Monetary('Agency', related="sea_lines_id.agency",store=True)
    transport_loading_price = fields.Monetary()
    transport_discharge_price = fields.Monetary()
    insurance_price = fields.Float()
    clearance_price = fields.Float()
    is_loading = fields.Boolean()
    is_discharge = fields.Boolean()
    is_clearance_cost = fields.Boolean()
    is_insurance_cost = fields.Boolean()
    type = fields.Selection([('loading','Loading'),('discharg','Discharg')])
    product_id = fields.Many2one('product.product', string='Name Of Discount', domain=[('is_discount', '=', True)])
    value = fields.Monetary('Discount Value')
    rate = fields.Monetary('Rate')
    line_cost_id = fields.Many2one('line.cost', required=True)
    total = fields.Monetary('Total',compute='_compute_total')
    currency_id = fields.Many2one('res.currency', string="Currency")
    
    @api.depends('agency','transport_loading_price','value','rate','transport_discharge_price','clearance_price','insurance_price')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.clearance_price + rec.insurance_price + rec.agency + rec.rate+ rec.transport_discharge_price + rec.transport_loading_price - rec.value
            
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        return super(LineCostLine, self)._search( args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)

    @api.onchange('product_id') 
    def erase_value_discount(self):
        """Erase discount value if product name changed"""
        for rec in self:
            rec.value=False
        

class LineCost(models.Model):
    _name = 'line.cost'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'line_id'
    _description = "LineCost"
    
    line_id = fields.Many2one('res.partner', string="Shipping Line", required=True,domain=[('company_type', '=', 'company'),('is_sea_line', '=', True)])
    quot_number = fields.Char(string="Quotation Number", required=True)
    date = fields.Date('Date', required=True)
    country_loading_id = fields.Many2one('res.country', string="Country Of Loading", required=True)
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading")
    city_loading_id = fields.Many2one('res.city', string="City Of Loading")
    place_loading_id = fields.Many2one('res.place', string="Place Of Loading", required=True)
    transport_loading_id = fields.Many2one('transport.type', string="Transport Type Of Loading")
    port_loading_id = fields.Many2one('port', string="POL", required=True)
    terminal_loading_id = fields.Many2one('res.place', string="Terminal of Loading", required=True)
    
    is_same_country = fields.Boolean('Is Same Country', default=True)
    country_dest_id = fields.Many2one('res.country', string="Country Of Discharge", required=True)
    state_dest_id = fields.Many2one('res.country.state', string="State Of Discharge")
    city_dest_id = fields.Many2one('res.city', string="City Of Discharge")
    terminal_des_same_id = fields.Many2one('res.place', string="Terminal of Discharge")
    
    country_diff_dest_id = fields.Many2one('res.country', string="Country Of Last Destination")
    state_diff_dest_id = fields.Many2one('res.country.state', string="State Of Last Destination")
    city_diff_dest_id = fields.Many2one('res.city', string="City Of Last Destination")
    place_diff_dest_id = fields.Many2one('res.place', string="Place Of Last Destination")
    delivery_diff_place_id = fields.Many2one('res.place', 'Place Of Last Delivery')
    
    port_dest_id = fields.Many2one('port', string="POD", required=True)
    transport_dest_id = fields.Many2one('transport.type', string="Transport Type Of Discharge")
    delivery_place_id = fields.Many2one('res.place', 'Place Of Delivery')
    bill_fees = fields.Monetary('Bill fees',compute='_compute_bill_fees',store=True)
    free_demurrage_and_detention = fields.Integer()
    transt_time = fields.Integer(required=True)
    customer_id = fields.Many2one('res.partner',stirng='Named Account')
    fak = fields.Boolean('FAK',default=True)
    product_id = fields.Many2one('product.product')
    commodity_id = fields.Many2one('commodity')
    start_date = fields.Date('Start Date')
    expiry_date = fields.Date('Expiry Date')
    note = fields.Text('Notes')
    is_expired = fields.Boolean(compute='_compute_is_expired',search="_search_is_expired")
    is_next = fields.Boolean(compute='_compute_is_next',search="_search_is_next")
    line_cost_ids = fields.One2many('line.cost.line','line_cost_id',string="Price")
    additional_cost_ids = fields.One2many('additional.cost','line_cost_id',string="Additional Cost")
    product_discount_id = fields.Many2one('product.product', string='Additional Discount' ,domain=[('is_discount', '=', True)])
    discount = fields.Monetary(default=0.0)
    active=fields.Boolean(default=True)
    currency_id = fields.Many2one('res.currency', string="Currency", required=True)
    
    
    is_loading = fields.Boolean(compute="_compute_is_loading")
    is_discharge = fields.Boolean(compute="_compute_is_discharge")
    
    @api.multi    
    @api.depends('line_cost_ids','line_cost_ids.is_discharge')
    def _compute_is_discharge(self):
        for rec in self:
            rec.is_discharge = any(rec.line_cost_ids.mapped('is_discharge'))
            
            
    @api.multi    
    @api.depends('line_cost_ids','line_cost_ids.is_loading')
    def _compute_is_loading(self):
        for rec in self:
            rec.is_loading = any(rec.line_cost_ids.mapped('is_loading'))
        
    
    
    @api.multi
    @api.depends('expiry_date')
    def _compute_is_expired(self):
        for rec in self:
            if rec.expiry_date and rec.expiry_date < fields.Date.today():
               rec.is_expired = True 
            else:
               rec.is_expired = False
               
    @api.multi
    @api.depends('start_date')
    def _compute_is_next(self):
        for rec in self:
            if rec.start_date and rec.start_date > fields.Date.today():
               rec.is_next = True 
            else:
               rec.is_next = False
               
               
    def _search_is_expired(self,op,val):
        sql = """
select id from line_cost where expiry_date <= '%s'
"""%fields.Date.today()
        self._cr.execute(sql)
        ids = self._cr.fetchall()
        ids = [id[0] for id in ids]
        if val and op == '=' or not val and op == '!=':
            domain = [('id','in', ids)]
        else :
            domain = [('id','not in', ids)]
        return domain
    
    def _search_is_next(self,op,val):
        sql = """
select id from line_cost where start_date > '%s'
"""%fields.Date.today()
        self._cr.execute(sql)
        ids = self._cr.fetchall()
        ids = [id[0] for id in ids]
        if val and op == '=' or not val and op == '!=':
            domain = [('id','in', ids)]
        else :
            domain = [('id','not in', ids)]
        return domain
    
    @api.onchange('fak')
    def _onchange_fak(self):
        self.commodity_id = False
        
        
    #   loaded country related
    @api.onchange('country_loading_id')
    def erase_related_addr(self):
        self.state_loading_id = False
        self.city_loading_id= False
        self.place_loading_id = False
        self.port_loading_id = False
        self.terminal_loading_id = False
    
    @api.onchange('state_loading_id')
    def erase_related_addr_three(self):
        self.city_loading_id= False
        self.place_loading_id = False
    
    @api.onchange('city_loading_id')
    def erase_related_addr_four(self): 
        self.place_loading_id = False
        
    @api.onchange('port_loading_id')
    def erase_related_addr_six(self): 
        self.terminal_loading_id = False
    
#   Destination country related
    @api.onchange('country_dest_id')
    def erase_related_addr_des(self):
        self.state_dest_id = False
        self.city_dest_id= False
        self.place_dest_id = False
        self.port_dest_id = False
        self.terminal_des_same_id = False
        self.delivery_place_id = False
    
    @api.onchange('state_dest_id')
    def erase_related_addr_three_des(self):
        self.city_dest_id= False
        self.place_dest_id = False
    
    @api.onchange('city_dest_id')
    def erase_related_addr_four_des(self): 
        self.place_dest_id = False
        
    @api.onchange('port_dest_id')
    def erase_related_addr_six_des(self): 
        self.terminal_des_same_id = False  
    
    #   Last country related
    @api.onchange('country_diff_dest_id')
    def erase_related_addr_last(self):
        self.state_diff_dest_id = False
        self.city_diff_dest_id= False
        self.place_diff_dest_id = False
        self.port_diff_id = False
        self.terminal_des_diff_id = False
        self.delivery_diff_place_id = False
    
    @api.onchange('state_diff_dest_id')
    def erase_related_addr_three_last(self):
        self.city_diff_dest_id= False
        self.place_diff_dest_id = False
    
    @api.onchange('city_diff_dest_id')
    def erase_related_addr_four_last(self): 
        self.place_diff_dest_id = False
        
    @api.onchange('port_diff_id')
    def erase_related_addr_six_last(self): 
        self.terminal_des_diff_id = False  
    
   
               
   
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
            rec.discount=False
                
    
    
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
        self.quot_number = False
        self.date = False
        self.cost_line_ids = False
        self.condition_ids = False
    
    
    
    
    
    
