# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _name = 'sale.order.line.shipment'
    order_shipment_id = fields.Many2one('sale.order')
    product_id = fields.Many2one('product.product')


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    order_line_shipment_ids = fields.One2many('sale.order.line.shipment', 'order_shipment_id')
    release = fields.Boolean('Release')
    sale_state = fields.Selection([('progress', 'In Progress'), ('confirmed', 'Confirmed'), ('not_confirmed', 'Not Confirmed')])
    shipment_method = fields.Selection([('all_in', 'All In'), ('sea_freight', 'Sea freight'), ('land_freight', 'Land Freight'), ('air_freight', 'Air Freight'), ('clearance', 'Clearance')])
    shipment_type = fields.Selection([('cross', 'Cross'), ('import', 'Import'), ('export', 'Export')])
    user_operation_id = fields.Many2one('res.users')
    customer_class_id = fields.Many2one('customer.class')
    container_qty = fields.Integer()
    
    country_loding_id = fields.Many2one('res.country', string="Country Of Loading")
    city_loding_id = fields.Many2one('res.city', string="City Of Loading")
    place_loding_id = fields.Many2one('loading.place', string="Place Of Loading")
    port_loafing_id = fields.Many2one('port', string="POL")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    port_dest_id = fields.Many2one('port', string="POD")

    weight_type_id = fields.Many2one('weight.type')
    agreement_method_id = fields.Many2one('agreement.method')
    customs_dec_id = fields.Many2one('customs.declaration', string="Customs Declaration")
    shiping_line_id = fields.Many2one('res.partner')
    container_size_id = fields.Many2one('container.size')
    free_days = fields.Integer()
    vessel_id = fields.Many2one('vessel')
    voyage_id = fields.Many2one('voyages.detail')
    voyage_date = fields.Date()
    truck_type_id = fields.Many2one('truck.type')
    
    
    
