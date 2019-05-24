# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Commodity(models.Model):
    _name = 'commodity'
    
    name = fields.Char ('Name')
    temperature = fields.Float('Temperature')
    warehouse_condition = fields.Char('Warehouse condition')
    warehouse_condition_att = fields.Binary(attachment=True,string="Attachment")
    transport_condition = fields.Char('Transport condition')
    transport_condition_att = fields.Binary(attachment=True,string="Attachment")
    port_condition = fields.Char('Port condition')
    port_condition_att = fields.Binary(attachment=True,string="Attachment")
    other_condition = fields.Char('Other condition')
    other_condition_att = fields.Binary(attachment=True,string="Attachment")
    commodity_category = fields.Many2one('commodity', string='Commodity Category')
    UN_No = fields.Char("UN No")
    IMCO_Class = fields.Char("IMCO Class")
    HS_Code = fields.Char("HS Code")

