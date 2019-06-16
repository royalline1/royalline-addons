# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TransportType(models.Model):
    _name = 'transport.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name',required=True)
    note = fields.Char('Note')
    
