# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression


class ContainerSize(models.Model):
    _name = 'container.size'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "size"
    _description = "ContainerSize"
    
    size = fields.Char('Size',required=True)
    container_no = fields.Char('No')
    container_status = fields.Selection([('None', 'None'), 
                                         ('Truck', 'Truck'), 
                                         ('Yard', 'Yard'),
                                         ('Vessel', 'Vessel'),
                                         ('Other', 'Other')], 
                                         string="Container Status")
    note = fields.Char('Note')
    TEU = fields.Char('TEU')
    image = fields.Binary(attachment=True)
    active=fields.Boolean(default=True)
