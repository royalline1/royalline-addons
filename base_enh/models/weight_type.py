# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeightType(models.Model):
    _name = 'weight.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Size',required=True)
    note = fields.Char('Note')
    active=fields.Boolean(default=True)
    
