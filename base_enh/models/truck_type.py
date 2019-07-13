# -*- coding: utf-8 -*-

from odoo import models, fields, api


class truckType(models.Model):
    _name = 'truck.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "truckType"
    
    name = fields.Char('Size',required=True)
    note = fields.Char('Note')
    image = fields.Binary(attachment=True)
    active=fields.Boolean(default=True)
    type = fields.Many2many('truck.type.selections')
class TruckTypeSelections(models.Model):
    _name='truck.type.selections'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='selections of truck type'
    
    name=fields.Char('Name')
    active=fields.Boolean(default=True)