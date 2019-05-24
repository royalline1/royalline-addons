# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError
from odoo.osv.expression import AND , OR

class Job(models.Model):
    _name = 'job'
    
    name = fields.Char(readonly=True)
    from_validity_date = fields.Date()
    to_validity_date = fields.Date()
    partner_id = fields.Many2one('res.partner',required=True)
    order_line_shipment_ids = fields.One2many('sale.inquiry.line', 'inquiry_id')
    release = fields.Boolean('Release')
    admin_release = fields.Boolean('Admin Release')
    sale_state = fields.Selection([('progress', 'In Progress'), ('confirmed', 'Confirmed'), ('not_confirmed', 'Not Confirmed')], default="progress")
#     shipment_method = fields.Selection([('clearance', 'Clearance'), 
#                                         ('sea_freight', 'Sea freight'), 
#                                         ('land_freight', 'Land Freight'), 
#                                         ('air_freight', 'Air Freight'), 
#                                         ('other_services', 'Other Services')])
#     shipment_type = fields.Selection([('import', 'Import'), 
#                                         ('export', 'Export'), 
#                                         ('cross', 'Cross'), 
#                                         ('internal', 'internal')])
#   sales inquiry filters
    shipment_method = fields.Selection([('clearance', 'Clearance'), 
                                        ('sea_freight', 'Sea freight'), 
                                        ('land_freight', 'Land Freight'), 
                                        ('air_freight', 'Air Freight'), 
                                        ('other_services', 'Other Services')],string="Shipment Method",store=True)
    shipment_type = fields.Selection([('import', 'Import'), 
                                        ('export', 'Export'), 
                                        ('cross', 'Cross'), 
                                        ('internal', 'internal')],string="Shipment Type",store=True)  
    shipment_logic = fields.Selection([('fcl', 'FCL'), 
                                        ('lcl', 'LCL'), 
                                        ('roro', 'RORO')],string="Shipment logic",store=True)
    customer_ref = fields.Char('Customer Reference')
    shipper_ref = fields.Char('Shipper Reference')
    consignee_ref = fields.Char('Consignee Reference') 
    notify_party_ref = fields.Char('Notify Party Ref') 
    add_notify_ref = fields.Char('Additional Notify Ref') 
    consignee_id = fields.Many2one('res.partner', string='Consignee')
    first_notify_id = fields.Many2one('res.partner', string='First Notify Party')
    add_notify_id = fields.Many2one('res.partner', string='Additional Notify')
#   the condition of shipment delivery
    shiping_terms = fields.Selection([('exw', 'EXW'), 
                                        ('fca', 'FCA'), 
                                        ('cpt', 'CPT'),
                                        ('cip', 'CIP'), 
                                        ('dat', 'DAT'), 
                                        ('dap', 'DAP'),
                                        ('ddp', 'DDP'), 
                                        ('dore_to_dore', 'Door to Door'), 
                                        ('fas', 'FAS'),
                                        ('fob', 'FOB'), 
                                        ('cfr', 'CFR'), 
                                        ('cif', 'CIF'),
                                        ('c_and_f', 'C & F')],string="Shipment Terms",store=True)
#   shipment details fields added 22-05-2019
    volume_ship = fields.Float('Volume')
    dimensions = fields.Float('Dimensions')
    weight = fields.Float('Weight')
    charge_weight = fields.Float('Chargeable Weight')
    type_package_no = fields.Float('No. & Type of Packages')
    
#     shipment_type = fields.Selection([('cross', 'Cross'), ('import', 'Import'), ('export', 'Export')])
    sales_person = fields.Many2one('res.users', default=lambda self: self.env.user)
    user_operation_id = fields.Many2one('res.users')
    customer_class_id = fields.Many2one('customer.class', related="partner_id.customer_class_id", store=True)
    shipper_id = fields.Many2one('res.partner', string='Shipper')
    
    country_loading_id = fields.Many2one('res.country', string="Country Of Loading")
    city_loading_id = fields.Many2one('res.city', string="City Of Loading")
    place_loading_id = fields.Many2one('res.place', string="Place Of Loading")
    port_loading_id = fields.Many2one('port', string="POL")
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination")
    port_dest_id = fields.Many2one('port', string="POD")
    place_of_port_id = fields.Many2one('res.place')
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination")
    is_loading = fields.Boolean()
    is_discharge = fields.Boolean()
    
    delivery_place_id = fields.Many2one('res.place', string='Place Of Delivery')

    
    agreement_method_id = fields.Many2one('agreement.method')
    customs_dec_id = fields.Many2one('customs.declaration', string="Customs Declaration")
    shipping_line_id = fields.Many2one('line.cost')
    shipping_line_ids = fields.Many2many('line.cost', compute="_shipping_line_ids")
    partner_shipping_line_id = fields.Many2one('res.partner', related="shipping_line_id.line_id")
    
    free_days = fields.Integer()
    vessel_id = fields.Many2one('vessel')
    voyage_id = fields.Many2one('voyages.detail')
    etd_date = fields.Date('ETD Date', related="voyage_id.etd_date", readonly=True)
    eta_date = fields.Date('ETA Date', related="voyage_id.eta_date", readonly=True)
    
    c_month = fields.Char('Month', default=datetime.date.today().month, readonly=True)
    c_year = fields.Char('Year', default=datetime.date.today().year, readonly=True)
    condition_ids = fields.One2many('sale.inquiry.condition', 'inquiry_id', 'Conditions')
    container_size_ids = fields.One2many('sale.inquiry.container', 'inquiry_id', 'Container Price')
    container_ids = fields.Many2many('container.size', compute="_compute_container_ids")
    
    
    admin_sale_state = fields.Selection([('progress', 'In Progress'), ('confirmed', 'Confirmed'), ('not_confirmed', 'Not Confirmed')], default="progress")
    sea_rate = fields.Float('Sea Rate #######')
    insurance_cost_id = fields.Many2one('insurance.cost', 'Insurance Cost')
    insurance_cost_ids = fields.Many2many('insurance.cost', compute="_insurance_cost_ids")
    insurance_rate = fields.Float(related="insurance_cost_id.total",readonly=True)
    transport_rate = fields.Float(compute='_compute_transport_rate')
    clearance_id = fields.Many2one('clearance.cost','Clearance')
    clearance_cost_ids = fields.One2many('sale.clearance.cost.line', 'inquiry_id', 'Clearance Cost',readonly=True)
    additional_cost_ids = fields.One2many('inquiry.additional.cost', 'inquiry_id', 'Additional Cost')

#   Transport details  
    transporter_cost_id = fields.Many2one('transport.cost', string='Transport')
    transporter_free_days = fields.Integer(related='transporter_cost_id.free_days', string='Transport Free Days')
#     transporter_name = fields.Char(related='transporter_cost_id.partner_id', string='Transporter name')
    transporter_total = fields.Float(related='transporter_cost_id.total', string='Transport Total')
#   Commodity key
    commodity_ids = fields.Many2many('commodity')  



    @api.depends('container_size_ids','container_size_ids.cost')
    def _compute_transport_rate(self):
        for rec in self:
            rec.transport_rate = sum([0]+rec.container_size_ids.mapped('cost'))
    @api.depends('container_size_ids','container_size_ids.line_cost_line_id')
    def _compute_container_ids(self):
        for rec in self:
            rec.container_ids = [(6,0,rec.container_size_ids.mapped('line_cost_line_id.sea_lines_id.container_size_id.id'))]
            
    @api.onchange('clearance_id','container_size_ids','container_size_ids.line_cost_line_id','container_size_ids.container_qty')
    def _compute_clearance_cost_ids(self):
        for rec in self:
            cci_obj = self.env['sale.clearance.cost.line']
            print(11)
            rec.clearance_cost_ids.unlink()
            print(22)
            if rec.clearance_id:
                for i in rec.container_size_ids:
                    total = 0.0
                    qty = i.container_qty
                    for l in rec.clearance_id.cost_line_ids:
                        if qty <= 0:
                            break
                        c_qty = l.to_truck - l.from_truck  +1
                        c_qty = c_qty if c_qty < qty else qty
                        qty -= c_qty
                        total += l.cost * c_qty
                    rec.clearance_cost_ids = [(0,0,{'container_id':i.line_cost_line_id.sea_lines_id.container_size_id.id,'cost':total,'inquiry_id':rec.id})]
                        
    @api.depends('country_loading_id','country_dest_id',
                 'city_loading_id','state_loading_id',
                 'city_dest_id','state_dest_id',)
    def _insurance_cost_ids(self):
       insurance_obj = self.env['insurance.cost']
       for rec in self:
            domain = [  ('country_loading_id', '=', rec.country_loading_id.id),
                        ('country_dest_id', '=', rec.country_dest_id.id),
                        ]
            domain = AND([domain, OR([[('city_loading_id', '=', rec.city_loading_id.id),
                                      ('city_dest_id', '=', rec.city_dest_id.id)],
                                    [('state_loading_id', '=', rec.state_loading_id.id),
                                      ('state_dest_id', '=', rec.state_dest_id.id)]])])
           
            insurance_cost_ids = insurance_obj.search(domain)
            rec.insurance_cost_ids = [(6,0,insurance_cost_ids.ids)]
            
            
    
    @api.depends('order_line_shipment_ids',
                 'order_line_shipment_ids.product_id',
                 'country_loading_id','port_dest_id',
                 'port_loading_id','country_dest_id',
                 'shipment_type','partner_id',
                 'is_loading','city_loading_id',
                 'place_loading_id','state_loading_id',
                 'city_dest_id','place_dest_id',
                 'state_dest_id','is_discharge')
    def _shipping_line_ids(self):
       line_cost_obj = self.env['line.cost']
       for rec in self:
            prod_ids = rec.order_line_shipment_ids.mapped('product_id')
            domain = [  ('country_loading_id', '=', rec.country_loading_id.id),
                        ('port_loading_id', '=', rec.port_loading_id.id),
                        ('port_dest_id', '=', rec.port_dest_id.id),
                        ('country_dest_id', '=', rec.country_dest_id.id),
                        ('line_cost_ids.sea_lines_id.type', '=', rec.shipment_type),
                        ('expired_price', '=', False)]
            domain = AND([domain, OR([[('customer_id', '=', rec.partner_id.id)],[('customer_id', '=', False)]])])
           
            domain = AND([domain, OR([[('product_id', 'in', prod_ids.ids)],[('fak', '=', False)]])])         
                        
            if rec.is_loading:
                domain = AND([domain,
                                AND([
                                    [('line_cost_ids.is_loading', '=', True),('place_loading_id', '=', rec.place_loading_id.id)],
                                    OR([[('city_loading_id', '=', rec.city_loading_id.id)],[('state_loading_id', '=', rec.state_loading_id.id)]])
                                    ])
                            ])
            if rec.is_discharge:
                domain = AND([domain,
                                AND([
                                    [('line_cost_ids.is_discharge', '=', True),('place_dest_id', '=', rec.place_dest_id.id)],
                                    OR([[('city_dest_id', '=', rec.city_dest_id.id)],[('state_dest_id', '=', rec.state_dest_id.id)]])
                                    ])
                            ])
            line_cost_ids = line_cost_obj.search(domain)
            rec.shipping_line_ids = [(6,0,line_cost_ids.ids)]
           
          
    @api.constrains('from_validity_date', 'to_validity_date')
    def validity_date_constraint(self):
        for rec in self:
            if rec.from_validity_date and rec.to_validity_date and rec.from_validity_date > rec.to_validity_date:  
                raise UserError("""The 'From Validity Date' must be less than 'To Validity Date'.""")
    
    @api.model_create_multi
    @api.returns('self', lambda value:value.id)
    def create(self, vals_list):
        for val in vals_list:
            val['name'] = self.env['ir.sequence'].next_by_code('inquiry.seq')
        return super(SaleInquiry, self).create(vals_list)
    
    
    
   
    
  
        
