# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InsuranceCondition(models.Model):
    _name = 'insurance.condition'
    
    name = fields.Char(required=True)
    type = fields.Selection([('include','Include'),('exclude','Exclude')],required=True)
    cost_id = fields.Many2one('line.cost',ondelete='cascade')
    
    
class AdditionalInsuCost(models.Model):
    _name = 'insurance.cost.line'
    
    product_id = fields.Many2one('product.product', string='Additional Name', required=True )
    cost = fields.Float()
    cost_id = fields.Many2one('line.cost',  required=True)

class InsuranceCost(models.Model):
    _name = 'insurance.cost'
    _rec_name = 'qut_number'
    
    partner_id = fields.Many2one('res.partner',string="Insurance Company",domain=[('is_insurance_company', '=', True)])
    qut_number =fields.Char('Quotation Number')
    date = fields.Date('Date')
    from_country_id = fields.Many2one('res.country',string="From Country")
    from_city_id = fields.Many2one('res.city',string='From City')
    to_country_id = fields.Many2one('res.country',string="To Country")
    to_city_id = fields.Many2one('res.city',string='To City')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    insurance_type_id = fields.Many2one('insurance.type',string="Insurance Type")
    rate = fields.Float()
    note = fields.Text()
    total = fields.Float(compute="_compute_total")
    cost_line_ids = fields.One2many('insurance.cost.line','cost_id',string="Additional Cost")
    condition_ids = fields.One2many('insurance.condition','cost_id',string="Condition")
    
    @api.depends('rate','cost_line_ids','cost_line_ids.cost')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.rate + sum(rec.mapped('cost_line_ids.cost')+[0])
        
        
        
        
    