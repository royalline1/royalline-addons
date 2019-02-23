# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrackType(models.Model):
    _name = 'track.type'
    
    name = fields.Char('Size',required=True)
    note = fields.Char('Note')
    
