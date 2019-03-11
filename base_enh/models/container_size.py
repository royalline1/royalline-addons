# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression


class ContainerSize(models.Model):
    _name = 'container.size'
    _rec_name = "size"
    
    size = fields.Char('Size',required=True)
    note = fields.Char('Note')
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if 'shipping_filter' in  self._context:
            if self._context.get('shipping_filter'):
                ids = self.env['line.cost.line'].search([('line_cost_id','=',self._context.get('shipping_filter'))]).mapped('container_id').ids
                args = expression.AND([args] + [[('id','in',ids)]])
            else:
                args = expression.AND([args] + [[('id','in',[])]])
        return super(ContainerSize, self)._search( args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
    
