# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InsuranceCondition(models.Model):
    _name = 'insurance.condition'
    _description = "InsuranceCondition"
    
    name = fields.Char(required=True)
    type = fields.Selection([('include','Include'),('exclude','Exclude')],required=True)
    cost_id = fields.Many2one('line.cost',ondelete='cascade')
    
    
class AdditionalInsuCost(models.Model):
    _name = 'insurance.cost.line'
    _description = "AdditionalInsuCost"
    
    product_id = fields.Many2one('product.product', string='Additional Name', required=True,
                                 domain=[('is_add_cost', '=', True)] )
    cost = fields.Monetary(string="Cost")
    cost_id = fields.Many2one('insurance.cost', string="Line Cost")
    currency_id = fields.Many2one('res.currency', string="Currency")

class InsuranceCost(models.Model):
    _name = 'insurance.cost'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'qut_number'
    _description = "InsuranceCost"
    
    partner_id = fields.Many2one('res.partner',string="Insurance Company",domain=[('is_insurance_company', '=', True)])
    qut_number =fields.Char('Quotation Number')
    date = fields.Date('Date')
    country_loading_id = fields.Many2one('res.country',string="Country Of Loading")
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading")
    city_loading_id= fields.Many2one('res.city',string='City Of Loading')
    country_dest_id = fields.Many2one('res.country',string="Country Of Destination")
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination")
    city_dest_id = fields.Many2one('res.city',string='City Of  Destination')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    insurance_type_id = fields.Many2one('insurance.type',string="Insurance Type")
    rate = fields.Monetary()
    currency_id = fields.Many2one('res.currency', string="Currency")
    note = fields.Text()
    total = fields.Monetary(compute="_compute_total")
    cost_line_ids = fields.One2many('insurance.cost.line','cost_id',string="Additional Cost")
    condition_ids = fields.One2many('insurance.condition','cost_id',string="Condition")
    
    
    is_expired = fields.Boolean('Is Expired Price',compute='_compute_is_expired',search="_search_is_expired")
    is_next = fields.Boolean(compute='_compute_is_expired',search="_search_is_next")
    active=fields.Boolean(default=True)
    
    
    
    def _search_is_expired(self,op,val):
        sql = """
select id from insurance_cost where to_date <= '%s'
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
select id from insurance_cost where from_date > '%s'
"""%fields.Date.today()
        self._cr.execute(sql)
        ids = self._cr.fetchall()
        ids = [id[0] for id in ids]
        if val and op == '=' or not val and op == '!=':
            domain = [('id','in', ids)]
        else :
            domain = [('id','not in', ids)]
        return domain
    
    
    
    @api.multi
    @api.depends('to_date','from_date')
    def _compute_is_expired(self):
        for rec in self:
            if rec.to_date and rec.to_date < fields.Date.today():
               rec.is_expired = True 
            else:
               rec.is_expired = False
            if rec.from_date and rec.from_date > fields.Date.today():
               rec.is_next = True 
            else:
               rec.is_next = False
    
    @api.depends('rate','cost_line_ids','cost_line_ids.cost')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.rate + sum(rec.mapped('cost_line_ids.cost')+[0])
        
        
        
        
    