# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TransportlinsuCost(models.Model):
    _name = 'transport.cost.line'
    
    product_id = fields.Many2one('product.product', string='Transport Name', required=True )
    cost = fields.Float(required=True)
    cost_id = fields.Many2one('transport.cost', required=True)


class TransportCost(models.Model):
    _name = 'transport.cost'
    _rec_name = 'qut_number'
   
    qut_number =fields.Char('Quotation Number')
    is_next = fields.Boolean('Is Next Price')
    is_expired = fields.Boolean('Is Expired Price')
    partner_id = fields.Many2one('res.partner',string="Transporter",domain=[('is_transporter_company', '=', True)])
    free_days = fields.Integer('Free Days')    
    weight_type_id = fields.Many2one('weight.type')
    truck_type_id = fields.Many2one('truck.type')
    country_loading_id = fields.Many2one('res.country', string="Country Of Loading", required=True)
    city_loading_id = fields.Many2one('res.city', string="City Of Loading")
    place_loading_id = fields.Many2one('loading.place', string="Place Of Loading")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    container_size_id = fields.Many2one('container.size')
    date = fields.Date('Date')
    price = fields.Float()
    cost_line_ids = fields.One2many('transport.cost.line','cost_id',string="Additional Cost")
    total = fields.Float('Total', compute='_compute_total',store=True)
    note = fields.Text()
    
    @api.depends('price','cost_line_ids','cost_line_ids.cost')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.price + sum(rec.cost_line_ids.mapped('cost')+[0])
            
    
    
    
        
        
    