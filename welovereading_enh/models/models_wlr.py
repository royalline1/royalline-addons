# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InternalRequisitiond(models.Model):
    _inherit = ['internal.requisition']
    _description = "InternalRequisitiond"
    
    request_emp = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        readonly=True,
        required=False,
        copy=True,
    )
    
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=False,
        readonly=True,
        copy=True,
        related='request_emp.department_id',
    )
