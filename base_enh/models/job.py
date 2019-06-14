# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError
from odoo.osv.expression import AND , OR

class JobCommodityLine(models.Model):
    _name = 'job.commodity.line'
    
    commodity_id = fields.Many2one('commodity',String='Commodity',required=True)
    package_name = fields.Char()
    quantity = fields.Float()
    operation = fields.Char()
    volume = fields.Float()
    gross_weight = fields.Char()
    job_id = fields.Many2one('job')
    
    

class Job(models.Model):
    _name = 'job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(readonly=True)
    sale_inquiry_id = fields.Many2one('sale.inquiry',store=True)
    from_validity_date = fields.Date(related='sale_inquiry_id.from_validity_date')
    to_validity_date = fields.Date(related='sale_inquiry_id.to_validity_date')
    partner_id = fields.Many2one('res.partner', related="sale_inquiry_id.partner_id")
    
    order_line_shipment_ids = fields.One2many('sale.inquiry.line', 
                                              inverse_name='job_id',
                                              related='sale_inquiry_id.order_line_shipment_ids')
    
    release = fields.Boolean(related='sale_inquiry_id.release',string='Release')
    admin_release = fields.Boolean(related='sale_inquiry_id.admin_release',string='Admin Release')
    sale_state = fields.Selection([('progress', 'In Progress'), 
                                   ('confirmed', 'Confirmed'), 
                                   ('not_confirmed', 'Not Confirmed')],
                                    related='sale_inquiry_id.sale_state')
    
    operation_type = fields.Selection([('house', 'House'), 
                                   ('master', 'Master'), 
                                   ('direct', 'Direct'),
                                   ('other', 'Other')],
                                    string='Operation Type')
    
    service = fields.Selection([('door_to_door', 'Door To Door'), 
                                   ('door_to_port', 'Door To Port'), 
                                   ('port_to_port', 'Port To Port'),
                                   ('port_to_door', 'Port To Door')],
                                    string='Service')
    intercom = fields.Char ('Intercom (CR)')

#   sales inquiry filters
    shipment_method = fields.Selection([('clearance', 'Clearance'), 
                                        ('sea_freight', 'Sea freight'), 
                                        ('land_freight', 'Land Freight'), 
                                        ('air_freight', 'Air Freight'), 
                                        ('other_services', 'Other Services')],
                                        string="Shipment Method",
                                        related='sale_inquiry_id.shipment_method')
    shipment_type = fields.Selection([('import', 'Import'), 
                                        ('export', 'Export'), 
                                        ('cross', 'Cross'), 
                                        ('internal', 'internal')],string="Shipment Type",
                                        related='sale_inquiry_id.shipment_type')  
    shipment_logic = fields.Selection([('fcl', 'FCL'), 
                                        ('lcl', 'LCL'), 
                                        ('roro', 'RORO')],string="Shipment logic",
                                        related='sale_inquiry_id.shipment_logic')
    customer_ref = fields.Char(string='Customer Reference',related='sale_inquiry_id.customer_ref')
    shipper_ref = fields.Char(string='Shipper Reference',related='sale_inquiry_id.shipper_ref')
    consignee_ref = fields.Char(string='Consignee Reference',related='sale_inquiry_id.consignee_ref') 
    notify_party_ref = fields.Char(string='Notify Party Ref',related='sale_inquiry_id.notify_party_ref') 
    add_notify_ref = fields.Char(string='Additional Notify Ref') 
    consignee_id = fields.Many2one('res.partner', string='Consignee',related="sale_inquiry_id.consignee_id")
    first_notify_id = fields.Many2one('res.partner', string='First Notify Party',
                                      related="sale_inquiry_id.first_notify_id")
    add_notify_id = fields.Many2one('res.partner', string='Additional Notify',
                                    related="sale_inquiry_id.add_notify_id")
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
                                        ('c_and_f', 'C & F')],string="Shipment Terms",store=True,
                                        related='sale_inquiry_id.shiping_terms')
#   shipment details fields added 22-05-2019
    volume_ship = fields.Float(related='sale_inquiry_id.volume_ship',string='Volume')
    dimensions = fields.Float(related='sale_inquiry_id.dimensions',string='Dimensions')
    weight = fields.Float(related='sale_inquiry_id.weight',string='Weight')
    charge_weight = fields.Float(related='sale_inquiry_id.charge_weight',string='Chargeable Weight')
    type_package_no = fields.Float(related='sale_inquiry_id.type_package_no',string='No. & Type of Packages')
    
#     shipment_type = fields.Selection([('cross', 'Cross'), ('import', 'Import'), ('export', 'Export')])
    sales_person = fields.Many2one('res.users', related="sale_inquiry_id.sales_person")
    user_operation_id = fields.Many2one('res.users',related="sale_inquiry_id.user_operation_id")
    customer_class_id = fields.Many2one('customer.class', related="sale_inquiry_id.customer_class_id"
                                        , store=True)
    shipper_id = fields.Many2one('res.partner', string='Shipper',
                                  related="sale_inquiry_id.shipper_id")
    
    country_loading_id = fields.Many2one('res.country', string="Country Of Loading",
                                         related="sale_inquiry_id.country_loading_id")
    city_loading_id = fields.Many2one('res.city', string="City Of Loading",
                                      related="sale_inquiry_id.city_loading_id")
    place_loading_id = fields.Many2one('res.place', string="Place Of Loading",
                                       related="sale_inquiry_id.place_loading_id")
    port_loading_id = fields.Many2one('port', string="POL",
                                      related="sale_inquiry_id.port_loading_id")
    state_loading_id = fields.Many2one('res.country.state', string="State Of Loading",
                                       related="sale_inquiry_id.state_loading_id")
    country_dest_id = fields.Many2one('res.country', string="Country Of Destination",
                                      related="sale_inquiry_id.country_dest_id")
    city_dest_id = fields.Many2one('res.city', string="City Of Destination",
                                   related="sale_inquiry_id.city_dest_id")
    place_dest_id = fields.Many2one('res.place', string="Place Of Destination",
                                    related="sale_inquiry_id.place_dest_id")
    port_dest_id = fields.Many2one('port', string="POD",related="sale_inquiry_id.port_dest_id")
    place_of_port_id = fields.Many2one('res.place',related="sale_inquiry_id.place_of_port_id")
    state_dest_id = fields.Many2one('res.country.state', string="State Of Destination"
                                    ,related="sale_inquiry_id.state_dest_id")
    is_loading = fields.Boolean(related='sale_inquiry_id.is_loading')
    is_discharge = fields.Boolean(related='sale_inquiry_id.is_discharge')
    
    delivery_place_id = fields.Many2one('res.place', string='Place Of Delivery',
                                        related="sale_inquiry_id.delivery_place_id")

    
    agreement_method_id = fields.Many2one('agreement.method', related="sale_inquiry_id.agreement_method_id")
    customs_dec_id = fields.Many2one('customs.declaration', string="Customs Declaration",
                                     related="sale_inquiry_id.customs_dec_id")
    shipping_line_id = fields.Many2one('line.cost',related="sale_inquiry_id.shipping_line_id")
    shipping_line_ids = fields.Many2many('line.cost', related="sale_inquiry_id.shipping_line_ids")
    partner_shipping_line_id = fields.Many2one('res.partner', related="sale_inquiry_id.partner_shipping_line_id")
    
    free_days = fields.Integer()
    vessel_id = fields.Many2one('vessel',related="sale_inquiry_id.vessel_id")
    voyage_id = fields.Many2one('voyages.detail',related="sale_inquiry_id.voyage_id")
    etd_date = fields.Date('ETD Date', related="sale_inquiry_id.voyage_id.etd_date", readonly=True)
    eta_date = fields.Date('ETA Date', related="sale_inquiry_id.voyage_id.eta_date", readonly=True)
    
    c_month = fields.Char('Month', default=datetime.date.today().month, readonly=True)
    c_year = fields.Char('Year', default=datetime.date.today().year, readonly=True)
    condition_ids = fields.One2many('sale.inquiry.condition', inverse_name='job_id', 
                                    related='sale_inquiry_id.condition_ids',string='Conditions')
    container_size_ids = fields.One2many('sale.inquiry.container', inverse_name='job_id',
                                         string= 'Container Price',related='sale_inquiry_id.container_size_ids')
    container_ids = fields.Many2many('container.size', related="sale_inquiry_id.container_ids")
    
    
    admin_sale_state = fields.Selection([('progress', 'In Progress'), 
                                         ('confirmed', 'Confirmed'), 
                                         ('not_confirmed', 'Not Confirmed')], 
                                         related='sale_inquiry_id.state')
    sea_rate = fields.Float(related='sale_inquiry_id.sea_rate',string='Sea Rate #######')
    insurance_cost_id = fields.Many2one('insurance.cost', string='Insurance Cost',
                                        related="sale_inquiry_id.insurance_cost_id")
    insurance_cost_ids = fields.Many2many('insurance.cost', related="sale_inquiry_id.insurance_cost_ids")
    insurance_rate = fields.Float(related="sale_inquiry_id.insurance_rate")
    transport_rate = fields.Float(related="sale_inquiry_id.transport_rate")
    clearance_id = fields.Many2one('clearance.cost',string='Clearance',
                                   related="sale_inquiry_id.clearance_id")
    clearance_cost_ids = fields.One2many('sale.clearance.cost.line', 
                                         inverse_name='job_id', string='Clearance Cost'
                                         ,related='sale_inquiry_id.clearance_cost_ids')
    
    additional_cost_ids = fields.One2many('inquiry.additional.cost', 
                                          inverse_name='job_id',
                                          related='sale_inquiry_id.additional_cost_ids', 
                                          string='Additional Cost')

#   Transport details  
    transporter_cost_id = fields.Many2one('transport.cost', string='Transport',
                                          related="sale_inquiry_id.transporter_cost_id")
    transporter_free_days = fields.Integer(related='sale_inquiry_id.transporter_free_days', string='Transport Free Days')
#     transporter_name = fields.Char(related='transporter_cost_id.partner_id', string='Transporter name')
    transporter_total = fields.Float(related='sale_inquiry_id.transporter_total', string='Transport Total')
#   Commodity key
    commodity_ids = fields.Many2many('commodity', related='sale_inquiry_id.commodity_ids')  

#   JOB FIELDS 
    booking_no = fields.Char(string='Booking No')
    booking_date = fields.Date(string='Booking Date')
    booking_confirmation = fields.Date(string='Book Confirm Date')
    contract_no = fields.Char(string='Contract No')
    price_owner = fields.Many2one('res.partner', string='Price Owner', default=1)
    empt_container_depot = fields.Many2one('res.partner', string='Empty Container Depot')
    analytic_account = fields.Many2one('account.analytic.account', string='Analytical Account')
    Bill_Lading_No = fields.Char (string='Bill Of Lading No.') 
    issue_bill_lading_to = fields.Many2one ('res.partner', related='sale_inquiry_id.issue_bill_lading_to', string='Issue Bill of lading To')
#   Tracking fields 
    act = fields.Char('ACT')
    container_loaded_truck = fields.Char('Container Loaded on Truck') 

#   Driver Details      
    driver_ids = fields.One2many('driver.info', 
                                          inverse_name='job_driver_id', 
                                          string='Driver')

    added_con = fields.Boolean()
    
    commodity_line_ids = fields.One2many('job.commodity.line','job_id')
    
    @api.model_create_multi
    @api.returns('self', lambda value:value.id)
    def create(self, vals_list):
        d_id = super(Job, self).create(vals_list)
        for val in d_id:
            val['name'] = self.env['ir.sequence'].next_by_code('job.seq')
        for val in d_id:
            if val.driver_ids:
                for i in range(4):
                    val.write({'driver_ids':[(0,0, {'container_no':0})]}) 
        return d_id 
    
    @api.multi
    def add_con_lines(self):
        if self.driver_ids:
            if self.container_size_ids.container_qty > 0:
                con_no_count = self.container_size_ids.container_qty
                i = 0
                for i in range(int(con_no_count)):
                    self.write({'driver_ids':[(0,0, {'container_no':0})],'added_con':True})
                    i = i + 1
            else:
                raise UserError("Container QTY should be more than 0")    
        else:
            raise UserError("Please select driver first")
   
    
  
        
