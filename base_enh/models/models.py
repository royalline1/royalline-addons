# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression


class ResPlace(models.Model):
    _name = 'res.place'
    _rec_name = 'address'
    
    country_id = fields.Many2one('res.country',required=True)
    city_id = fields.Many2one('res.city',required=True)
    state_id = fields.Many2one('res.country.state')
    address = fields.Text('Address',required=True)
    
    
class Port(models.Model):
    _name = 'port'

    name = fields.Char(string='Name',required=True)
    code = fields.Char(string='Code')
    type = fields.Selection([('air',"Air"),('sea',"Sea"),('dry',"Dry")],required=True)
    country_id = fields.Many2one('res.country',stirng="Country",required=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_shipper = fields.Boolean('Is Shipper')
    is_consignee = fields.Boolean('Is Consignee')
    is_notify = fields.Boolean('Is notify Party')
    is_agent = fields.Boolean('Is Agent')
    is_diver = fields.Boolean('Is Driver')
    is_customs_point = fields.Boolean('Is Customs point')
    is_competitor = fields.Boolean('Is Competitor')
    is_sea_line = fields.Boolean('Is Sea Line')
    is_air_line = fields.Boolean('Is Air Line')
    is_clearance_company= fields.Boolean('Is Clearance Company')
    is_transporter_company= fields.Boolean('Is Transporter Company')
    is_insurance_company= fields.Boolean('Is Insurance Company')

    phone_ids = fields.One2many('res.phone','partner_id', string='Phones Number')
    
    sea_ids = fields.One2many('sea.lines','partner_id')
    bill_fees = fields.Float('Bill Fees')
    release_to_bill = fields.Float('Release To Bill')
    amendment_fees = fields.Float('Amendment Fees')
    late_payment = fields.Float('Late Payment')
    
    custome_id = fields.Many2one('res.partner',string="Customs point",domain=[('is_customs_point','=',True)])
    customer_class_id = fields.Many2one('customer.class')

    plate_code = fields.Char('Plate Code')
    plate_number = fields.Char('Plate Number')
    country_nati_id = fields.Many2one(
        'res.country', 'Nationality (Country)')
    country_truck_id = fields.Many2one(
        'res.country', 'Truck Nationality')
    truck_type_id = fields.Many2one('truck.type')
    
    cheek_name = fields.Char('Cheek Name')
    
    product_ids = fields.Many2many('product.product')
    
    
    @api.onchange('city_id')
    def _onchange_city_id(self):
        pass
    def open_vesels(self):
        action = self.env.ref('base_enh.vesel_action').read()[0]
        action['domain'] = [('sea_line_id','=',self.id)]
        action['context'] = {'default_sea_line_id':self.id}
        return action
    
    
class ResPhone(models.Model):
    _name = 'res.phone'
    
    name = fields.Char('Number',required=True)
    note = fields.Char('Note')  
    partner_id = fields.Many2one('res.partner')
    
    
class SeaLines(models.Model):
    _name="sea.lines"
    
    container_size_id = fields.Many2one('container.size',string="Container Size")
    type = fields.Selection([('import','Import'),('export','Export'),('cross','Cross')])
    free_days = fields.Integer('Free Days')
    first_demurrage_from = fields.Integer('First Way Demurrage From')
    first_demurrage_to = fields.Integer('First Way Demurrage To')
    first_rate =  fields.Float('First Way Demurrage Rate') 
    second_demurrage_from = fields.Integer('Second Way Demurrage From')
    second_demurrage_to = fields.Integer('Second Way Demurrage To')
    second_rate =  fields.Float('Second Way Demurrage Rate')
    third_demurrage_from = fields.Integer('Third Way Demurrage From')
    third_demurrage_to = fields.Integer('Third Way Demurrage To')
    third_rate =  fields.Float('Third Way Demurrage Rate')
    delivery_order = fields.Float('Delivery Order')
    agency = fields.Float('Agency')
    partner_id = fields.Many2one('res.partner')
    
    
    
     
    
class ProductProduct(models.Model):
    _inherit = "product.template"   
    
    is_discount = fields.Boolean('Is Discount')

    
class ProductProduct(models.Model):
    _inherit = "product.product"
    
    temperature = fields.Integer('Temperature')
    warehouse_condition = fields.Integer('Warehouse condition')
    warehouse_condition_att = fields.Binary(attachment=True,string="Attachment")
    transport_condition = fields.Integer('Transport condition')
    transport_condition_att = fields.Binary(attachment=True,string="Attachment")
    port_condition = fields.Integer('Port condition')
    port_condition_att = fields.Binary(attachment=True,string="Attachment")
    other_condition = fields.Integer('Other condition')
    other_condition_att = fields.Binary(attachment=True,string="Attachment")
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('com_customer_id' ):
            partner_id = self.env['res.partner'].browse(self._context.get('com_customer_id' ))
            args = expression.AND([args] + [[('id','in',partner_id.product_ids.ids)]])
            
            
        
        return super(ProductProduct, self)._search(args, offset, limit, order, count, access_rights_uid)
    
    
      