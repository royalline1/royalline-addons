# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError


class InquiryAdditionalCost(models.Model):
    _name = 'inquiry.additional.cost'
    
    product_id = fields.Many2one('product.product', string='Name',required=True )
    cost = fields.Float(required=True)
    sale_id = fields.Many2one('sale.order')

class SaleInquiryCondition(models.Model):
    _name = 'sale.inquiry.condition'
    
    name = fields.Char(required=True)
    sale_id = fields.Many2one('sale.order',ondelete='cascade')
    
class SaleInquiryContainer(models.Model):
    _name = 'sale.inquiry.container'
    
    container_id = fields.Many2one('container.size','Container',required=True)
    target_rate = fields.Float()
    sold = fields.Float()
    first_rate = fields.Float()
    second_rate = fields.Float()
    third_rate = fields.Float()
    sale_id = fields.Many2one('sale.order')
    sale_mang_id = fields.Many2one('sale.order')
    line_id = fields.Many2one('line.cost',related="sale_id.shipping_line_id")
    line_mang_id = fields.Many2one('line.cost',related="sale_mang_id.shipping_line_id")
    
class ClearanceCostLine(models.Model):
    _name = 'inquiry.clearance.cost'
    
    customs_point_id = fields.Many2one('res.partner','Customs Point')
    customs_dec_id = fields.Many2one('customs.declaration', string="Customs Declaration")
    clearance_id = fields.Many2one('res.partner','Clearance Company')
    rate = fields.Float()
    sale_id = fields.Many2one('sale.order',ondelete='cascade')
    
    
class SaleOrderLineShipment(models.Model):
    _name = 'sale.order.line.shipment'
    
    product_id = fields.Many2one('product.product')
    temperature = fields.Float('Temperature',related="product_id.temperature")
    warehouse_condition = fields.Char('Warehouse condition',related="product_id.warehouse_condition")
    warehouse_condition_att = fields.Binary(attachment=True,string="Attachment",related="product_id.warehouse_condition_att")
    transport_condition = fields.Char('Transport condition',related="product_id.transport_condition")
    transport_condition_att = fields.Binary(attachment=True,string="Attachment",related="product_id.transport_condition_att")
    port_condition = fields.Char('Port condition',related="product_id.port_condition")
    port_condition_att = fields.Binary(attachment=True,string="Attachment",related="product_id.port_condition_att")
    other_condition = fields.Char('Other condition',related="product_id.other_condition")
    other_condition_att = fields.Binary(attachment=True,string="Attachment",related="product_id.other_condition_att")
    order_shipment_id = fields.Many2one('sale.order')


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    from_validity_date = fields.Date()
    
    order_line_shipment_ids = fields.One2many('sale.order.line.shipment', 'order_shipment_id')
    release = fields.Boolean('Release')
    inquiry_name = fields.Char('Inquiry Number',readonly=True)
    admin_release = fields.Boolean('Admin Release')
    sale_state = fields.Selection([('progress', 'In Progress'), ('confirmed', 'Confirmed'), ('not_confirmed', 'Not Confirmed')])
    shipment_method = fields.Selection([('all_in', 'All In'), ('sea_freight', 'Sea freight'), ('land_freight', 'Land Freight'), ('air_freight', 'Air Freight'), ('clearance', 'Clearance')])
    shipment_type = fields.Selection([('cross', 'Cross'), ('import', 'Import'), ('export', 'Export')])
    user_operation_id = fields.Many2one('res.users')
    customer_class_id = fields.Many2one('customer.class',related="partner_id.customer_class_id",store=True)
    container_qty = fields.Integer()
    shipper_id = fields.Many2one('res.partner',string='Shipper')
    
    
    country_loading_id = fields.Many2one('res.country', string="Country Of Loading")
    city_loading_id = fields.Many2one('res.city', string="City Of Loading")
    place_loading_id = fields.Many2one('loading.place', string="Place Of Loading")
    port_loading_id = fields.Many2one('port', string="POL")
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    port_dest_id = fields.Many2one('port', string="POD")
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination")
    
    delivery_place_id = fields.Many2one('delivery.place',string='Place Of Delivery')
    

    weight_type_id = fields.Many2one('weight.type')
    agreement_method_id = fields.Many2one('agreement.method')
    customs_dec_id = fields.Many2one('customs.declaration', string="Customs Declaration")
    shipping_line_id = fields.Many2one('line.cost')
    partner_shipping_line_id = fields.Many2one('res.partner',related="shipping_line_id.line_id")
    
    free_days = fields.Integer()
    vessel_id = fields.Many2one('vessel')
    voyage_id = fields.Many2one('voyages.detail')
    voyage_date = fields.Date()
    truck_type_id = fields.Many2one('truck.type')
    c_month = fields.Char('Month',default=datetime.date.today().month,readonly=True)
    c_year = fields.Char('Year',default=datetime.date.today().year,readonly=True)
    condition_ids = fields.One2many('sale.inquiry.condition','sale_id','Conditions')
    container_size_ids = fields.One2many('sale.inquiry.container','sale_id','Container Price')
    container_size_mang_ids = fields.One2many('sale.inquiry.container','sale_mang_id','Suggest Container Price')
    
    
    
    country_dest_t_id = fields.Many2one('res.country', string="Country Of Destination")
    city_dest_t_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_t_id = fields.Many2one('res.place', string="Place Of Destination")
    
    admin_sale_state = fields.Selection([('progress', 'In Progress'), ('confirmed', 'Confirmed'), ('not_confirmed', 'Not Confirmed')])
    line_cost_id = fields.Many2one('line.cost','Line Cost')
    sea_rate = fields.Float()
    insurance_cost_id = fields.Many2one('insurance.cost','Insurance Cost')
    insurance_rate = fields.Float()
    transport_cost_id = fields.Many2one('transport.cost','Transport Cost')
    transport_rate = fields.Float()
    clearance_cost_ids = fields.One2many('inquiry.clearance.cost','sale_id','Clearance Cost')
    additional_cost_ids = fields.One2many('inquiry.additional.cost','sale_id','Additional Cost')
   
    @api.constrains('from_validity_date','validity_date')
    def validity_date_constraint(self):
        for rec in self:
            if rec.from_validity_date and rec.from_validity_date:
                raise UserError("""The 'From Validity Date' must be less than 'To Validity Date'.""")
            

    
    @api.model_create_multi
    @api.returns('self', lambda value:value.id)
    def create(self, vals_list):
        for val in vals_list:
            val['inquiry_name'] = self.env['ir.sequence'].next_by_code('inquiry.seq')
        return super(SaleOrder, self).create(vals_list)
    
