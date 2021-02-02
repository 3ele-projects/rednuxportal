# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
class rednuxMyPurchase(models.Model):
    _inherit = 'purchase.order'

class rednuxResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    lieferant_id = fields.Many2one(
        'x_lieferanten',
        string='Lieferant',
        compute='_get_x_lieferanten_record_id'
        )

    def _get_x_lieferanten_record_id(self):
        lieferant_id = self.env['x_lieferanten'].search(
            [('x_studio_field_kontakt', '=', self.id)])   
        self.lieferant_id = lieferant_id






    


