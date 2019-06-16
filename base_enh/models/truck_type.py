# -*- coding: utf-8 -*-

from odoo import models, fields, api


class truckType(models.Model):
    _name = 'truck.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Size',required=True)
    note = fields.Char('Note')
    image = fields.Binary(attachment=True)
    active=fields.Boolean(default=True)
