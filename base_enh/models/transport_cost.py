# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class TransportlinsuPrice(models.Model):
    _name = 'transport.price.line'
    _rec_name = 'container_size_id'
    _description = "TransportlinsuPrice"
    
    container_size_id = fields.Many2one('container.size', required=True)
    weight_type_id = fields.Many2one('weight.type')
    truck_type_id = fields.Many2one('truck.type')
    price = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    cost_id = fields.Many2one('transport.cost')
    
    @api.multi
    def name_get(self):
        lines = []
        for rec in self:
            name = ' | '.join([i for i in [rec.cost_id.partner_id.name, rec.weight_type_id.name, rec.truck_type_id.name] if i])
            lines.append((rec.id,name))
        return lines
    
class TransportlinsuCost(models.Model):
    _name = 'transport.cost.line'
    _rec_name = 'container_size_id'
    _description = "TransportlinsuCost"
    
    product_id = fields.Many2one('product.product', string='Transport Name', required=True, 
                                 domain=[('is_add_cost', '=', True)])
    container_size_id = fields.Many2one('container.size', required=True)
    cost = fields.Monetary(required=True, string="Cost")
    currency_id = fields.Many2one('res.currency', string="Currency")
    per_quantity = fields.Boolean()
    cost_id = fields.Many2one('transport.cost', string="Cost line")
    


class TransportCost(models.Model):
    _name = 'transport.cost'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'qut_number'
    _description = "TransportCost"
   
    
    qut_number =fields.Char('Quotation Number')
    is_next = fields.Boolean('Is Next Price',compute='_compute_is_next',search="_search_is_next")
    partner_id = fields.Many2one('res.partner',string="Transporter",domain=[('is_transporter_company', '=', True)])
    free_days = fields.Integer('Free Days')    
    country_loading_id = fields.Many2one('res.country', string="Country Of Loading", required=True)
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading")
    city_loading_id = fields.Many2one('res.city', string="City Of Loading")
    place_loading_id = fields.Many2one('res.place', string="Place Of Loading")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    is_port = fields.Boolean(related="place_dest_id.is_port",store=True)
    date = fields.Date('Date')
    price = fields.Monetary(string="Price")
    cost_line_ids = fields.One2many('transport.cost.line','cost_id',string="Additional Cost")
    price_line_ids = fields.One2many('transport.price.line','cost_id',string="Line Price")
    total = fields.Monetary('Total', compute='_compute_total',store=True)
    note = fields.Text()
    is_expired = fields.Boolean('Is Expired Price',compute='_compute_is_expired',search="_search_is_expired")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    active=fields.Boolean(default=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    payment_term_id = fields.Many2one('account.payment.term', string="Payment Terms", 
                                      related='partner_id.property_supplier_payment_term_id',
                                      readonly=True)
    #Smart buttons
    @api.multi  
    def call_job(self):  
        mod_obj = self.env['ir.model.data']
        try:
            tree_res = mod_obj.get_object_reference('job', 'view_job__tree')[1]
            form_res = mod_obj.get_object_reference('job', 'view_job_form')[1]
        except ValueError:
            form_res = tree_res = search_res = False
        return {  
            'name': ('job'),  
            'type': 'ir.actions.act_window',  
            'view_type': 'form',  
            'view_mode': "[tree,form]",  
            'res_model': 'job',  
            'view_id': False,  
            'views': [(tree_res, 'tree'),(form_res, 'form')], 
            'domain': [('transporter_cost_id.id', '=', self.id)], 
            'target': 'current',  
               }      
    @api.multi  
    def call_sale_inquiry(self):  
        mod_obj = self.env['ir.model.data']
        try:
            tree_res = mod_obj.get_object_reference('sale.inquiry', 'view_inquiry_tree')[1]
            form_res = mod_obj.get_object_reference('sale.inquiry', 'view_inquiry_form')[1]
        except ValueError:
            form_res = tree_res = search_res = False
        return {  
            'name': ('sale.inquiry'),  
            'type': 'ir.actions.act_window',  
            'view_type': 'form',  
            'view_mode': "[tree,form]",  
            'res_model': 'sale.inquiry',  
            'view_id': False,  
            'views': [(tree_res, 'tree'),(form_res, 'form')], 
            'domain': [('transporter_cost_id.id', '=', self.id)], 
            'target': 'current',  
               }
    
    def _search_is_expired(self,op,val):
        sql = """
select id from transport_cost where to_date <= '%s'
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
select id from transport_cost where from_date > '%s'
"""%fields.Date.today()
        self._cr.execute(sql)
        ids = self._cr.fetchall()
        ids = [id[0] for id in ids]
        if val and op == '=' or not val and op == '!=':
            domain = [('id','in', ids)]
        else :
            domain = [('id','not in', ids)]
        return domain
            
        
        return []
    @api.onchange('partner_id')
    def erse_price(self):
        """"Erase price once quotation OR Shipper changed"""
        self.price= 0
        self.qut_number = False
        self.date = False
        self.price_line_ids = False
        self.cost_line_ids = False
        self.transport_line_price = 0
    
    @api.onchange('country_loading_id')
    def erse_loading_country_details(self):
        """"Erase state city and place once country changed"""
        self.state_loading_id=False
        self.city_loading_id=False
        self.place_loading_id=False
            
    @api.onchange('country_dest_id')
    def erse_deliveiry_country_details(self):
        """"Erase state city and place once country changed"""
        self.state_dest_id=False
        self.city_dest_id=False
        self.place_dest_id=False
    
    @api.multi
    @api.depends('to_date')
    def _compute_is_expired(self):
        for rec in self:
            if rec.to_date and rec.to_date < fields.Date.today():
               rec.is_expired = True 
            else:
               rec.is_expired = False
               
    
    api.multi
    @api.depends('from_date')
    def _compute_is_next(self):
        for rec in self:
            if rec.from_date and rec.from_date > fields.Date.today():
               rec.is_next = True 
            else:
               rec.is_next = False
               
    @api.constrains('from_date', 'to_date')
    def validity_date_constraint(self):
        for rec in self:
            if rec.from_date and rec.to_date and rec.from_date > rec.to_date:  
                raise UserError("""The 'From Date' must be less than 'To Date'.""")    
    
#     @api.constrains('is_port','place_dest_id')
#     def is_port_check(self):
#         for rec in self:
#             if not rec.is_port and rec.place_dest_id:
#                 raise UserError('You cannot create transport cost with a not place port')
                
                
        
        
    @api.depends('price','cost_line_ids','cost_line_ids.cost')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price + sum(rec.cost_line_ids.mapped('cost')+[0])
            
    
    
    
        
        
    