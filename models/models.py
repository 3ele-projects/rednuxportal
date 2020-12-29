# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rednuxMyPurchase(models.Model):
    _inherit = 'purchase.order'

class rednuxResPartnerInherit(models.Model):
    _inherit = 'res.partner'
   # lieferant_id = fields.One2many('x_lieferanten','x_studio_field_kontakt' )


