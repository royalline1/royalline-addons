# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Followup(models.Model):
    _name = 'followup'
    
    is_load_from_depot = fields.Boolean('Is Loaded From Depot')
    arrived_to_shipper = fields.Boolean('Arrived to Shipper')
    depart_from_shipper =  fields.Boolean('Depart From Shipper')
    terminal_active =  fields.Boolean('Terminal Active')
    misfer_registered =  fields.Boolean('Misfer Registered')
    xray_registered =  fields.Boolean('X-Ray Registered')
    terminal_gate_in =  fields.Boolean('Terminal Gate In')
    terminal_registered =  fields.Boolean('Terminal Registered')
    loaded_to_vessel =  fields.Boolean('Loaded to Vessel')
    
#     @api.model_create_multi
#     @api.returns('self', lambda value:value.id)
#     def create(self, vals_list):
#         for val in vals_list:
#             val['name'] = self.env['ir.sequence'].next_by_code('job.seq')
#         return super(Job, self).create(vals_list)
    
    
    
   
    
  
        
