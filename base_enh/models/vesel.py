# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Vesel(models.Model):
    _name = 'vesel'
    
    sea_line_id = fields.Many2one('res.partner',string="Shipping",domain=[('is_sea_line','=',True)],required=True)
    name = fields.Char('Name',required=True)
    country_id = fields.Many2one('res.country')
    image = fields.Binary(attachment=True,related="country_id.image",readonly=True)
    Home_port_id = fields.Many2one('port',string="Home Port")
    build = fields.Selection([(year,year) for year in range(2000,2051)])
    code = fields.Char('Code')
    note = fields.Char('Notes')
    imo_number  = fields.Char('Imo Number')
    voyages_ids = fields.One2many("voyages.detail",'vesel_id')
    
class VoyagesDetail(models.Model):
    _name = "voyages.detail"
    
    vesel_id = fields.Many2one('vesel')
    sea_line_id = fields.Many2one('res.partner',string="Shipping",domain=[('is_sea_line','=',True)])
    voyage_number  = fields.Char('Voyage Number')
    etd_date = fields.Date('ETD Ddate')
    eta_date = fields.Date('ETA Ddate')
    