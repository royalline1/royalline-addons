# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AgreementMethod(models.Model):
    _name = 'bill.of.lading'
    
    shipping_line = fields.Char()
    bill_lading_no = fields.Char (string='Bill Of Lading No.')
    shipper = fields.Char(string='Shipper')
    consignee = fields.Char(string='Consignee')
    first_notify = fields.Char(string='First Notify Party')
    add_notify = fields.Char(string='Additional Notify')
    booking_no = fields.Char(string='Booking No')
    contract_no = fields.Char(string='Contract No')
    port_loading = fields.Char(string="POL")
    port_dest = fields.Char(string="POD")
    vessel = fields.Char('vessel')
    voyage = fields.Char('voyages.detail')
    place_of_loading = fields.Char(string='Place of Loading')
    place_of_receipt = fields.Char(string='Place of Receipt')
    commodity_ids = fields.Many2many('commodity',related="job_id.commodity_ids")
    job_id = fields.Many2one('job')
    
    
class ExternalBillOfLoading(models.Model):
    _name = 'external.bill.of.lading'
    
    shipping_line = fields.Char('Shipping Lline')
    bill_lading_no = fields.Char (string='Bill Of Lading No')
    shipper = fields.Char(string='Shipper')
    consignee = fields.Char(string='Consignee')
    first_notify = fields.Char(string='First Notify Party')
    add_notify = fields.Char(string='Additional Notify')
    booking_no = fields.Char(string='Booking No')
    contract_no = fields.Char(string='Contract No')
    port_loading = fields.Char(string="POL")
    port_dest = fields.Char(string="POD")
    vessel = fields.Char('vessel')
    voyage = fields.Char('voyages.detail')
    place_of_loading = fields.Char(string='Place of Loading')
    place_of_receipt = fields.Char(string='Place of Receipt')
    commodity_ids = fields.Many2many('commodity',related="job_id.commodity_ids")
    job_id = fields.Many2one('job')
    show_get = fields.Boolean()
    
    

    def get_place_of_receipt(self):
        self.place_of_receipt = self.job_id.place_dest_id.address

    def get_place_of_loading(self):
        self.place_of_loading = self.job_id.place_loading_id.address

    def get_voyage(self):
        self.voyage = self.job_id.voyage_id.voyage_number

    def get_vessel(self):
        self.vessel = self.job_id.vessel_id.name

    def get_port_dest(self):
        self.port_dest = self.job_id.port_dest_id.name

    def get_port_loading(self):
        self.port_loading = self.job_id.port_loading_id.name

    def get_contract_no(self):
        self.contract_no = self.job_id.contract_no

    def get_add_notify(self):
        self.add_notify = self.job_id.add_notify_id.name

    def get_first_notify(self):
        self.first_notify = self.job_id.first_notify_id.name

    def get_booking_no(self):
        self.booking_no = self.job_id.booking_no

    def get_consignee(self):
        self.consignee = self.job_id.consignee_id.name

    def get_shipper(self):
        self.shipper = self.job_id.shipper_id.name

    def get_bill_lading_no(self):
        self.bill_lading_no = self.job_id.bill_lading_no

    def get_shipping_line(self):
        self.shipping_line = self.job_id.shipping_line_id.line_id.name

    
    @api.model
    def default_get(self, fields_list): 
        res = super(ExternalBillOfLoading, self).default_get(fields_list)
        job_id = self.env['job'].browse(self._context.get('default_job_id',[]))
        if self._context.get('default_show_get'):
            res.update({'shipping_line':job_id.shipping_line_id.line_id.name,
                   'bill_lading_no':job_id.bill_lading_no,
                   'shipper':job_id.shipper_id.name,
                   'consignee':job_id.consignee_id.name,
                   'first_notify':job_id.first_notify_id.name,
                   'add_notify':job_id.add_notify_id.name,
                   'booking_no':job_id.booking_no,
                   'contract_no':job_id.contract_no,
                   'port_loading':job_id.port_loading_id.name,
                   'port_dest':job_id.port_dest_id.name,
                   'vessel':job_id.vessel_id.name,
                   'voyage':job_id.voyage_id.voyage_number,
                   'place_of_loading':job_id.place_loading_id.address,
                   'place_of_receipt':job_id.place_dest_id.address,
                   'job_id':job_id.id
                   })
        elif self._context.get('default_job_id',[]):
            ebol_ids = self.search([('job_id','=',self._context.get('default_job_id'))], order='id desc',limit=1)
            if ebol_ids:
                res.update({'shipping_line':ebol_ids.shipping_line,
                   'bill_lading_no':ebol_ids.bill_lading_no,
                   'shipper':ebol_ids.shipper,
                   'consignee':ebol_ids.consignee,
                   'first_notify':ebol_ids.first_notify,
                   'add_notify':ebol_ids.add_notify,
                   'booking_no':ebol_ids.booking_no,
                   'contract_no':ebol_ids.contract_no,
                   'port_loading':ebol_ids.port_loading,
                   'port_dest':ebol_ids.port_dest,
                   'vessel':ebol_ids.vessel,
                   'voyage':ebol_ids.voyage,
                   'place_of_loading':ebol_ids.place_of_loading,
                   'place_of_receipt':ebol_ids.place_of_receipt,
                   'job_id':ebol_ids.job_id.id
                   })
                
        return res
    
    
