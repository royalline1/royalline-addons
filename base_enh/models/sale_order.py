# -*- coding: utf-8 -*-
from odoo import models, fields, api



class SaleOrderLine(models.Model):
    _name = 'sale.order.line.shipment'
    order_shipment_id = fields.Many2one('sale.order')
    product_id = fields.Many2one('product.product')

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    order_line_shipment_ids = fields.One2many('sale.order.line.shipment','order_shipment_id')
    
    