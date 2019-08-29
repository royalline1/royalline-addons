# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"   
    _description = "Product Template"
    
    medicine_shape_ids=fields.Many2many('medicine.shape', string='Medicine Shape')
    scientific_name_id=fields.Many2one('scientific.name', string='Scientific Name')
    medicine_class_ids=fields.Many2many('medicine.class', string='Medicine Class')
    active_ingredient_ids=fields.Many2many('active.ingredient', string='Active Ingredient')
    
class MedicineShape(models.Model):
    _name="medicine.shape"
    _description = "Medicine Shape"
    
    name = fields.Char()

class ScientificName(models.Model):
    _name="scientific.name"
    _description = "Scientific Name"
    
    name = fields.Char()

class MedicineClass(models.Model):
    _name="medicine.class"
    _description = "Medicine Class"
    
    name = fields.Char()

class ActiveIngredient(models.Model):
    _name="active.ingredient"
    _description = "Active Ingredient"
    
    name = fields.Text()
    
    
    
    
    