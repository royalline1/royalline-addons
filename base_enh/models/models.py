# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FinalDest(models.Model):
    _name = 'final.dest'
    _rec_name = 'zip'
    
    zip = fields.Integer('ZIP Code',required=True)
    counrty_id = fields.Many2one('res.country',required=True)
    city_id = fields.Many2one('res.city',required=True)
    state_id = fields.Many2one('res.country.state',required=True)
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
    phone_ids = fields.One2many('res.phone','partner_id', string='Phones Number')
    
    air_sea_ids = fields.One2many('air.sea.lines','partner_id')
    bill_fees = fields.Float('Bill Fees')
    release_to_bill = fields.Float('Release To Bill')
    amendment_fees = fields.Float('Amendment Fees')
    late_payment = fields.Float('Pate Payment')
    
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
    
    
    @api.onchange('city_id')
    def _onchange_city_id(self):
        pass
    def open_vesels(self):
        action = self.env.ref('base_enh.vesel_action').read()[0]
        action['domain'] = [('sea_line_id','=',self.id)]
        return action
    
class ResPhone(models.Model):
    _name = 'res.phone'
    
    name = fields.Char('Number',required=True)
    note = fields.Char('Note')  
    partner_id = fields.Many2one('res.partner')
    
    
class AirSeaLines(models.Model):
    _name="air.sea.lines"
    
    container_size_id = fields.Many2one('container.size',string="Container Size")
    free_days = fields.Integer('Free Days')
    first_storage_from = fields.Integer('First Way Storage From')
    first_storage_to = fields.Integer('First Way Storage To')
    first_demurrage_from = fields.Integer('First Way Demurrage From')
    first_demurrage_to = fields.Integer('First Way Demurrage To')
    second_storage_from = fields.Integer('Second Way Storage From')
    second_storage_to = fields.Integer('Second Way Storage To')
    second_demurrage_from = fields.Integer('Second Way Demurrage From')
    second_demurrage_to = fields.Integer('Second Way Demurrage To')
    third_storage_from = fields.Integer('Third Way Storage From')
    third_storage_to = fields.Integer('Third Way Storage To')
    third_demurrage_from = fields.Integer('Third Way Demurrage From')
    third_demurrage_to = fields.Integer('Third Way Demurrage To')
    agency = fields.Float('Agency')
    partner_id = fields.Many2one('res.partner')
    
    
    
    
    
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
      