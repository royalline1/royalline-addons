# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression
from odoo.exceptions import UserError
from os import linesep

class SalePerson(models.Model):
    _name = "sale.person"
    
    user_id = fields.Many2one('res.users',required=True)
    type = fields.Selection([('sale','Sale'),
                             ('operation','Operation'),
                             ('follow','Follow')],required=True)
    partner_id = fields.Many2one('res.partner')
    

class ResPlace(models.Model):
    _name = 'res.place'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'address'
    
    country_id = fields.Many2one('res.country',required=True)
    city_id = fields.Many2one('res.city',required=True)
    state_id = fields.Many2one('res.country.state')
    is_port = fields.Boolean('Is Terminal')
    port_id = fields.Many2one('port')
    address = fields.Text('Address',required=True)
    is_delivery_place = fields.Boolean('Is Delivery Place') 
    zip_code = fields.Integer('ZIP Code')
    
    @api.onchange('country_id')
    def place_erase(self):
        """Erase data from City, state, address, zipcode and Port"""
        self.city_id=u''
        self.state_id=u''
        self.address=u''
        self.zip_code=u''
        self.port_id=u''
    
    @api.onchange('state_id')
    def erase_state_related(self):
        for rec in self:
            rec.city_id = u''
            rec.port_id = u''
            rec.address = u''
        
class Port(models.Model):
    _name = 'port'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',required=True)
    code = fields.Char(string='Code')
    type = fields.Selection([('air',"Air"),('sea',"Sea"),('dry',"Dry")],required=True,default='air')
    country_id = fields.Many2one('res.country',stirng="Country",required=True)
    state_id = fields.Many2one('res.country.state','State')
    port_type = fields.Many2many('port.type', string='Port Type',required=True)
    city_id = fields.Many2one('res.city',required=True)
    
    @api.onchange('country_id')
    def erase_country_related(self):
        """Erase related fields to 'Country' once empty or changed"""
        for rec in self:
            rec.state_id=u''
            rec.city_id=u''
    
    @api.onchange('state_id')
    def erase_state_related(self):
        """erase related fields to state once empty or changed"""
        for rec in self:
            rec.city_id=u''
        
    
class PortType(models.Model):
    _name = 'port.type'
     
    name = fields.Char('Name')
    
class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    local_name = fields.Char("Local Name")

class ResCity(models.Model):
    _inherit="res.city"
    code = fields.Char("Code")
    local_name = fields.Char("Local Name")
    
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
    is_depot = fields.Boolean('Is Depot')

    phone_ids = fields.One2many('res.phone','partner_id', string='Phones Number')
    
    sea_ids = fields.One2many('sea.lines','partner_id')
    bill_fees = fields.Float('Bill Fees')
    release_to_bill = fields.Float('Release To Bill')
    amendment_fees = fields.Float('Amendment Fees')
    late_payment = fields.Float('Late Payment')
    
    customs_id = fields.Many2one('res.partner',string="Customs point",domain=[('is_customs_point','=',True)])
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
    
    sale_person_ids= fields.One2many('sale.person','partner_id')
    

#   City local name   
    local_name = fields.Char("Local Name")
    
#   gogle map field display at contact form.   
    google_map_partner = fields.Char(string="Map")

#   commodity ids
    commodity_ids = fields.Many2many('commodity')  
    job_id = fields.Many2one ('job')
    job_position_id = fields.Many2one('job.position', string="Staff Job Position")
    @api.multi
    def name_get(self):
        if 'custom_point' in self._context:
            lines = []
            for record in self:
                name = (record.name + ' | ' + record.parent_id.name) if record.parent_id else record.name
                lines.append((record.id,name))
            return linese
        lines = []
        for record in self:
            name = record.name + ' | ' + str(record.plate_code) + ' | '+ str(record.plate_number) if record.is_diver else record.name
            lines.append((record.id,str(name)))
        return lines
        return super(ResPartner, self).name_get()
#     @api.multi
#     def name_get(self):
#         lines = []
#         for rec in self:
#             name = (rec.name + ' | ' + str(rec.) + ' | ' + str(rec.))
#             lines.append(rec.id,name)
#         return lines
#     @api.multi
#     def name_get(self):
#         lines = []
#         for record in self:
#             name = record.name + ' | ' + str(record.plate_code) + ' | '+ str(record.plate_number) 
#             lines.append((record.id,str(name)))
#         return lines
        
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if 'customs_filter' in self._context and self._context.get('from_customs_filter',True):
            if not self._context.get('customs_filter'):
                args = expression.AND([args] + [[('id','in',[])]])
            else:
                partner_id = self.env['res.partner'].browse(self._context.get('customs_filter' ))
                args = expression.AND([args] + [[('id','in',partner_id.with_context(from_customs_filter=False).child_ids.mapped('customs_id').ids)]])
        return super(ResPartner, self)._search( args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
    @api.onchange('city_id')
    def _onchange_city_id(self):
        pass
    def open_vessels(self):
        action = self.env.ref('base_enh.vessel_action').read()[0]
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
    name = fields.Char(related="container_size_id.size")
   
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
    
    
    @api.multi
    def name_get(self):
        lines = []
        for record in self:
            name = str(record.name) + ' | ' + str(record.type)
            lines.append((record.id,str(name)))
        return lines
    
    
    
     
    

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        operation_filter = self._context.get('operation_filter',0)
        if operation_filter is False:
            raise UserError('Must select a customer first')
        elif operation_filter:
            ids =  self.env['sale.person'].search([('type','=','operation'),('partner_id','=',operation_filter)]).mapped('user_id').ids
            args = expression.AND([args] + [[('id','in',ids)]])
        return super(ResUsers, self)._search(args, offset, limit, order, count, access_rights_uid)
    
class ExtraServices(models.Model):
    _name = 'extra.services'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name')
    code = fields.Char('Code')
    note = fields.Text('Note')
    active = fields.Boolean('Active',default=True)

class WareHouse (models.Model):
    _name = 'ware.house'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name')
    code = fields.Char('Code')
    note = fields.Text('Note')
    type = fields.Selection([('terminal','Terminal'),('bonded','Bonded'),('others','Others')],  default='terminal', string='Type')
    terminal_code = fields.Char('Terminal Code')
    address = fields.Text('Address')
    image = fields.Binary(attachment=True)
    active = fields.Boolean('Active',default=True)
    image_attachment = fields.Binary(attachment=True,string="Image Attachment")
    
class MITCompanies (models.Model):
    _name = 'mit.companies'

    company_No = fields.Char ('Company No.')
    name = fields.Char ('name')
    type = fields.Selection([('1','ذات مسؤولية محدودة'),
                             ('2','أجنبية - فرع عامل'),
                             ('3','أجنبية-فرع غير عامل'),
                             ('4','معفاه'),
                             ('5','مساهمة خاصة محدودة'),
                             ('6','تضامن'),
                             ('7','توصية بسيطة'),
                             ('8','عربية مشتركة'),
                             ('9','لا تهدف إلى ربح'),
                             ('10','مدنيه'),
                             ('11','مساهمة عامة محدودة'),
                             ('12','اخرى'),
                             ('13','مؤسسة فردية'),
                             ('14','مناطق حرة'),
                             ('15','جمعيات'),
                             ('16','0'),
                             ],string='Type',default='1',required=True, store=True)
    capital = fields.Integer('Capital')
    registration_date = fields.Datetime('Registration Date')
    city_id = fields.Many2one('res.city',required=True)
    phone = fields.Char ('Phone No')
    mobile = fields.Char ('Mobile No')
    HQ = fields.Char('Head Quarter')
    po_box = fields.Integer ('P.O. Box')
    postal_code = fields.Integer ('Postal Code')
    Email = fields.Char ('Email')
    org_national_no = fields.Char ('Org National No')
    active = fields.Boolean('Active',default=True)
    
    @api.multi  
    def get_trade_name(self):  
        mod_obj = self.env['ir.model.data']
        try:
            tree_res = mod_obj.get_object_reference('trade_name', 'trade_name_list_view')[1]
            form_res = mod_obj.get_object_reference('trade_name', 'trade_name_form_view')[1]
#             search_res = mod_obj.get_object_reference('trade_name', 'view_trade_tran_search1')[1]
        except ValueError:
            form_res = tree_res = search_res = False
        return {  
            'name': ('Trade Name list'),  
            'type': 'ir.actions.act_window',  
            'domain': [],  
            'view_type': 'form',  
            'view_mode': "[tree,form]",  
            'res_model': 'trade.name',  
            'view_id': False,  
            'views': [(tree_res, 'tree'), (form_res, 'form')], 
            'domain': [('registration_No','=',self.company_No),('type', '=', self.type)], 
            'target': 'current',  
               } 

            
class TradeName (models.Model):
    _name = 'trade.name'
    
    trade_No = fields.Char ('Trade No.')
    city_id = fields.Many2one('res.city',required=True)
    type = fields.Selection([('1','ذات مسؤولية محدودة'),
                             ('2','أجنبية - فرع عامل'),
                             ('3','أجنبية-فرع غير عامل'),
                             ('4','معفاه'),
                             ('5','مساهمة خاصة محدودة'),
                             ('6','تضامن'),
                             ('7','توصية بسيطة'),
                             ('8','عربية مشتركة'),
                             ('9','لا تهدف إلى ربح'),
                             ('10','مدنيه'),
                             ('11','مساهمة عامة محدودة'),
                             ('12','اخرى'),
                             ('13','مؤسسة فردية'),
                             ('14','مناطق حرة'),
                             ('15','جمعيات'),
                             ('16','0'),
                             ],string='Type',default='1',required=True, store=True)
    registration_No = fields.Char ('Registration No.')
    trade_name = fields.Char ('Trade Name')
    registration_date = fields.Datetime('Registration Date')
    state = fields.Text(string='Status')
    owner = fields.Char('Owner')

class ImporterCard (models.Model): 
    _name = 'importer.card'
    
    card_No = fields.Char ('Card No.')
    name = fields.Char ('Name')
    issue_date = fields.Datetime ('Date of Issue')
    expiry_date = fields.Datetime ('Expiry Date')
    active = fields.Boolean('Active',default=True)
    
class IndividualEstablishment (models.Model):
    _name = 'individual.establishment'
    
    ind_No = fields.Char ('Indiv Estab No.')
    city_id = fields.Many2one('res.city',required=True)
    registeration_date = fields.Datetime ('Registration Date')
    capital = fields.Integer('Capital')
    owner_nationality = fields.Char ('Owner Nationality')
    state = fields.Char(string='Status')
    status_date = fields.Datetime ('Status Date')
    National_ID = fields.Char ('National ID')
    establishment_name = fields.Char ('Establishment Name')
    trade_name = fields.Char ('Trade Name')
    place_id = fields.Many2one('res.place',required=True)
    street = fields.Char ('Street')
    
    
    
    
    
    
    
    
    
     