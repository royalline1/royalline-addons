# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression
from odoo.exceptions import UserError
from os import linesep
    
class MITCompanies (models.Model):
    _name = 'mit.companies'
    _description = "MITCompanies"
    
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
    _description = "TradeName"
    
    
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
    active=fields.Boolean(default=True)

class ImporterCard (models.Model): 
    _name = 'importer.card'
    _description = "ImporterCard"
    
    
    card_No = fields.Char ('Card No.')
    name = fields.Char ('Name')
    issue_date = fields.Datetime ('Date of Issue')
    expiry_date = fields.Datetime ('Expiry Date')
    active = fields.Boolean('Active',default=True)
    
class IndividualEstablishment (models.Model):
    _name = 'individual.establishment'
    _description = "IndividualEstablishment"
    
    
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
    active=fields.Boolean(default=True)
    
    
    
    
    
    
    
    
    
     