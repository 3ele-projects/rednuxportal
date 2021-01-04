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
        self.lieferant_id = [lieferant_id]



# class rednuxLieferantenInherit(models.Model):
#     _inherit = 'x_lieferanten'
#     carrier_ids = fields.Many2one(
#        'delivery.carrier',
#        string='Carriers'
       
#        )

#class rednuxLieferantenInherit(models.Model):
    # _inherit = 'studio_customization.lieferanten_7cc2b9e0-6ac1-4585-b3f6-f1a2fac4de40'
    # carrier_ids = fields.Many2one(
    #    'delivery.carrier',
    #    string='Carriers'
       
    #    )


    


