# -*- coding: utf-8 -*-
# from odoo import http
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from base64 import b64encode
from dateutil.parser import parse

from odoo.http import request, route

from odoo.addons.purchase.controllers import portal

from collections import OrderedDict
from dateutil.parser import parse
from odoo import http
from odoo.http import request, route
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.addons.purchase.controllers import portal
from odoo.addons.web.controllers.main import Binary
import logging
_logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):

	def _prepare_home_portal_values(self):

		values = super(CustomerPortal, self)._prepare_home_portal_values()
		values['purchase_count_new'] = request.env['purchase.order'].search_count(
			[('x_studio_status', '=', 'new')])
		values['purchase_count_confirmed'] = request.env['purchase.order'].search_count(
			[('x_studio_status', '=', 'confirmed')])
		values['purchase_count_ready_for_delivery'] = request.env['purchase.order'].search_count(
			[('x_studio_status', '=', 'ready for delivery')])
		values['purchase_count_delivered'] = request.env['purchase.order'].search_count(
			[('x_studio_status', '=', 'delivered')])
		values['purchase_count_billed'] = request.env['purchase.order'].search_count(
			[('x_studio_status', '=', 'billed')])
		values['purchase_count_paid'] = request.env['purchase.order'].search_count(
			[('x_studio_status', '=', 'paid')])
		values['x_lieferanten'] = request.env['x_lieferanten'].search(
			[('x_studio_field_kontakt', '=', request.env.user.partner_id.id)])
		
		if (request.env.user.partner_id.supplier_rank > 0):
			values['invoice_count'] = 0
			values['purchase_count'] = 0
			myvalue = request.env['x_lieferanten'].search([('x_studio_field_kontakt', '=', request.env.user.partner_id.id)])		
			
		return values

	@http.route(['/my/purchase', '/my/purchase/page/<int:page>'], type='http', auth="user", website=True)
	def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
		values = self._prepare_portal_layout_values()

		PurchaseOrder = request.env['purchase.order']
		domain = []
		archive_groups = self._get_archive_groups(
			'purchase.order', domain) if values.get('my_details') else []
		if date_begin and date_end:
			domain += [('create_date', '>', date_begin),
						('create_date', '<=', date_end)]

		searchbar_sortings = {
			'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
			'name': {'label': _('Name'), 'order': 'name asc, id asc'},
			'x_studio_marke': {'label': _('Marke'), 'order': 'x_studio_marke asc, id asc'},
			'amount_total': {'label': _('Total'), 'order': 'amount_total desc, id desc'},
		}
	# default sort by value
		if not sortby:
			sortby = 'date'
		order = searchbar_sortings[sortby]['order']

		searchbar_filters = {
			'all': {'label': _('all'), 'domain': [('x_studio_status', 'in', ['paid', 'billed', 'delivered', 'confirmed', 'new'])]},
			'new': {'label': _('new'), 'domain': [('x_studio_status', '=', 'new')]},
			'paid': {'label': _('paid'), 'domain': [('x_studio_status', '=', ['paid'])]},
			'billed': {'label': _('billed'), 'domain': [('x_studio_status', '=', 'billed')]},
			'delivered': {'label': _('delivered'), 'domain': [('x_studio_status', '=', 'delivered')]},
			'confirmed': {'label': _('confirmed'), 'domain': [('x_studio_status', '=', 'confirmed')]},
			'ready_for_delivery': {'label': _('ready for delivery'), 'domain': [('x_studio_status', '=', 'ready for delivery')]},
		}
	# default filter by value
		if not filterby:
			filterby = 'all'
		domain += searchbar_filters[filterby]['domain']

	# count for pager
		purchase_count = PurchaseOrder.search_count(domain)
	# make pager
		pager = portal_pager(
			url="/my/purchase",
			url_args={'date_begin': date_begin, 'date_end': date_end},
			total=purchase_count,
			page=page,
			step=self._items_per_page
		)
	# search the purchase orders to display, according to the pager data
		orders = PurchaseOrder.search(
			domain,
			order=order,
			limit=self._items_per_page,
			offset=pager['offset']
		)
		request.session['my_purchases_history'] = orders.ids[:100]

		values.update({
			'date': date_begin,
			'orders': orders,
			'page_name': 'purchase',
			'pager': pager,
			'archive_groups': archive_groups,
			'searchbar_sortings': searchbar_sortings,
			'sortby': sortby,
			'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
			'filterby': filterby,
			'default_url': '/my/purchase',
		})
		return request.render("rednuxportal.rednux_portal_purchase_orders", values)

	# @http.route(['/my/purchase/<int:order_id>'], type='http', auth="public", website=True)
	# def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):

	# 	try:
	# 		order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
	# 	except (AccessError, MissingError):
	# 		return request.redirect('/my')

	# 	values = self._purchase_order_get_page_view_values(order_sudo, access_token, **kw)
	# 	if order_sudo.company_id:
	# 		values['res_company'] = order_sudo.company_id

	# 	lieferant = request.env['x_lieferanten'].search([('x_studio_field_kontakt', '=', order_sudo.partner_id.id)])

	# 	if lieferant:
	# 		values['x_lieferant'] = lieferant
	# 	_logger.warning(values['x_lieferant'])
	# 	return request.render("purchase.portal_my_purchase_order", values)

	@route(route='/my/purchase/<int:order_id>', type='http', auth='public', website=True)
	def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):
		try:
			order_sudo = self._document_check_access(
				'purchase.order', order_id, access_token=access_token)
		except (AccessError, MissingError):
			return request.redirect('/my')
		values = self._purchase_order_get_page_view_values(order_sudo, access_token, **kw)
		values['carrier'] = request.env['delivery.carrier'].sudo().search([])

		

		if order_sudo.company_id:
			values['res_company'] = order_sudo.company_id

		return request.render("purchase.portal_my_purchase_order", values)


	@http.route(route='/my/purchase/<int:order_id>/update_remarks', type='json', auth='user', methods=['post'], website=True)
	def rednux_portal_my_purchase_update_remarks(self, order_id=None, x_studio_shipment_remarks=None, access_token=None, **kw):
		if x_studio_shipment_remarks:
			purchase_order = request.env['purchase.order'].sudo().browse(order_id)
			purchase_order.write({
				'x_studio_shipment_remarks': x_studio_shipment_remarks,
			})
		
	#	res = super().portal_my_purchase_order(order_id, access_token, **kw)
	#	return res

	@route(route='/my/picking/<int:picking_id>', type='json', auth='user', website=True)
	def update_picking_info(self, picking_id=None, access_token=None, **kw):
		vals = {}

		carrier_name = kw.get('carrier')
		carrier_tracking_ref = kw.get('tracking_ref')
		if carrier_tracking_ref:
			vals['carrier_tracking_ref'] = carrier_tracking_ref
		
		carrier_id = False
		carrier_name = kw.get('carrier')
		if carrier_name:
			carrier_id = request.env['delivery.carrier'].sudo().search(
				[('name', '=', carrier_name)],
				limit=1
			)

		if carrier_id:
			vals['carrier_id'] = carrier_id.id

		date = kw.get('date')
		if date:
			vals['scheduled_date'] = parse(date)

		if picking_id:
			picking_id = request.env['stock.picking'].sudo().browse(picking_id)
			picking_id.write(vals)


				
		
		
				
	@http.route(route='/my/purchase/<int:order_id>/update_status', type='json', auth='user', methods=['post'], website=True)
	def rednux_portal_my_purchase_update_status(self, order_id=None, shipmentdate=None, access_token=None, **kw):
		if shipmentdate:
			purchase_order = request.env['purchase.order'].sudo().browse(
				order_id)
			try:
				purchase_order.write({
					'x_studio_shipmentdate': shipmentdate,
					'x_studio_status': 'confirmed'
				})
			except:
				pass
			picking_ids = purchase_order.picking_ids

			for picking in picking_ids:
					picking.write({
						'scheduled_date': shipmentdate
					})

	@http.route(route='/my/purchase/<int:order_id>/update_delayed_date', type='json', auth='user', methods=['post'], website=True)
	def rednux_portal_my_purchase_update_delayed_date(self, order_id=None, delayed_shipmentdate=None, access_token=None, **kw):
		if delayed_shipmentdate:
			purchase_order = request.env['purchase.order'].sudo().browse(
				order_id)

			try:
				purchase_order.write({
					'x_studio_delayed_shipment_date': delayed_shipmentdate

				})
			except Exception as e:
				_logger.info(e)

		
	#@route(route='/my/purchase/<int:order_id>/upload', type='http', auth='user', methods=['post'], website=True)
	#def portal_my_purchase_order_upload_bill(self, order_id=None, file=None, access_token=None, **kw):
	#	if file:
	#		purchase_order = request.env['purchase.order'].sudo().browse(order_id)
	#		purchase_order.invoice_ids.unlink()
	#		invoice = request.env['account.move'].sudo().create(
	#			{
	#				'type': 'in_invoice',
	#				'company_id': purchase_order.company_id.id,
	#				'partner_id': purchase_order.partner_id.id,
	#				'invoice_origin': purchase_order.name,
	#				'ref': purchase_order.partner_ref,
	#			}
	#		)
	#		invoice.purchase_id = purchase_order.id
	#		invoice.with_context(portal=True)._onchange_purchase_auto_complete()
	#		invoice._onchange_partner_id()
	#		purchase_order.write({
	#			'x_studio_upload_bill': b64encode(file.read()),
	#			'x_studio_status' : 'billed'
	#			})
	#	return self.portal_my_purchase_order(order_id=order_id, access_token=access_token)

	@route(route='/my/picking/<int:picking_id>/validate', type='json', auth='user', website=True)
	def validate_picking(self, picking_id=None, access_token=None, **kw):
		data = {int(move_id): float(qty) for move_id, qty in kw.items()}
		picking_id = request.env['stock.picking'].sudo().browse(picking_id)
		
		for move_id in picking_id.move_ids_without_package:
			move_id.sudo().write({'quantity_done': data[move_id.id]})
		picking_id.with_context(create_backorder=True).button_validate()
		if (picking_id.state == 'done'):
			purchase_order = request.env['purchase.order'].sudo().browse(picking_id.purchase_id.id)
			ids = []
			for picking_id in purchase_order.picking_ids:
				if (picking_id.state == 'done'):
					ids.append(picking_id)
			if (len(ids) == int(purchase_order.picking_count)):
				purchase_order.write({
					'x_studio_status': 'delivered'
		
					})
		