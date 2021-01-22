odoo.define('vendor_purchase_order.delivery_order', function (require) {
	'use strict';

	var publicWidget = require('web.public.widget');

	publicWidget.registry.delivery_order = publicWidget.Widget.extend({
		selector: '.o_form_delivery',
		events: {
			'click .o_purchase_stock_picking button#picking_update'  : '_on_update',
			'click .o_purchase_stock_picking button#picking_submit'  : '_on_submit',
			'click .o_purchase_stock_picking button#picking_validate': '_on_validate',
		},

		//--------------------------------------------------------------------------
		// Handlers
		//--------------------------------------------------------------------------

		/**
		 * @private
		 */
		_on_update (e) {
			let picking_element = $(e.target.parentElement.parentElement);
			picking_element.find('.editonly').removeClass('d-none');
			picking_element.find('.readonly').addClass('d-none');
		},

		/**
		 * @private
		 */
		_on_submit (e) {
			let picking_element = $(e.target.parentElement.parentElement);
			picking_element.find('.editonly').addClass('d-none');
			picking_element.find('.readonly').removeClass('d-none');

			let picking_id = picking_element.find('input#picking_id').val();
			let params = {
				'date'        : picking_element.find('input[name="scheduled_date"]').val(),
				'carrier'     : picking_element.find('select[name="carrier"]').val(),
				'tracking_ref': picking_element.find('input[name="tracking_ref"]').val(),
			};
			this._update_picking_info(picking_id, params);
		},
		
		/**
		 * Calls the route to get updated values of the line and order
		 * when the quantity of a product has changed
		 *
		 * @private
		 * @param {integer} picking_id
		 * @param {Object} params
		 * @return {Deferred}
		 */
		_update_picking_info (picking_id, params) {
			var url = '/my/picking/' + picking_id;
			return this._rpc({
				route: url, params,
			}).then(function() {
				window.location.reload();
			});
		},

		/**
		 * @private
		 */
		_on_validate (e) {
			let picking_id = $('div.o_purchase_stock_picking input#picking_id').val();
			let params = {};
			let moves = $('div#picking_box').find('tbody tr');
			for (let move of moves) {
				move = $(move)
				params[move.find('input#move_id').val()] = move.find('input#quantity_done').val()
			}
			this._validate_picking(picking_id, params);
		},
		
		/**
		 * Calls the route to get updated values of the line and order
		 * when the quantity of a product has changed
		 *
		 * @private
		 * @param {integer} picking_id
		 * @param {Object} params
		 * @return {Deferred}
		 */
		_validate_picking (picking_id, params) {
			var url = '/my/picking/' + picking_id + '/validate';

			return this._rpc({
				route: url, params,
			}).then(function() {
				window.location.reload();
			});
		},
	});
});



odoo.define('rednuxportal.portal_my_purchase_order', function (require) {
	'use strict';

	var publicWidget = require('web.public.widget');

	publicWidget.registry.delivery_order_rednux = publicWidget.Widget.extend({
		selector: '.o_form_rednux_lieferanten',
		events: {
			'click button#picking_update'  : '_on_update',
			'click button#picking_submit'  : '_on_submit',
			'click button#picking_validate': '_on_validate',
			'click #x_studio_shipmentdate': '_shipmentdate_update',
			'click #x_studio_delayed_shipmentdate': '_delayed_shipmentdate_update',
			'click #remark_update': '_remark_update',

			//'click .o_purchase_stock_picking button#picking_submit'  : '_on_submit',

		},


		
		//--------------------------------------------------------------------------
		// Handlers
		//--------------------------------------------------------------------------

		/**
		 * @private
		 */
		_on_update (e) {
			let picking_element = $(e.target.parentElement.parentElement);
			picking_element.find('.editonly').removeClass('d-none');
			picking_element.find('.readonly').addClass('d-none');
		},

		/**
		 * @private
		 */
		_on_submit (e) {
			let picking_element = $(e.target.parentElement.parentElement);
			picking_element.find('.editonly').addClass('d-none');
			picking_element.find('.readonly').removeClass('d-none');

			let picking_id = picking_element.find('input#picking_id').val();
			let params = {
				'date'        : picking_element.find('input[name="scheduled_date"]').val(),
				'carrier'     : picking_element.find('select[name="carrier"]').val(),
				'tracking_ref': picking_element.find('input[name="tracking_ref"]').val(),
			};
			this._update_picking_info(picking_id, params);
		},
		
		/**
		 * Calls the route to get updated values of the line and order
		 * when the quantity of a product has changed
		 *
		 * @private
		 * @param {integer} picking_id
		 * @param {Object} params
		 * @return {Deferred}
		 */
		_update_picking_info (picking_id, params) {
			var url = '/my/picking/' + picking_id;
			return this._rpc({
				route: url, params,
			}).then(function() {
				window.location.reload();
			});
		},

		/**
		 * @private
		 */
		_on_validate (e) {
			let picking_id = $('div.o_purchase_stock_picking input#picking_id').val();
			let params = {};
			let moves = $('div#picking_box').find('tbody tr');
			for (let move of moves) {
				move = $(move)
				params[move.find('input#move_id').val()] = move.find('input#quantity_done').val()
			}
			this._validate_picking(picking_id, params);
		},
		
		/**
		 * Calls the route to get updated values of the line and order
		 * when the quantity of a product has changed
		 *
		 * @private
		 * @param {integer} picking_id
		 * @param {Object} params
		 * @return {Deferred}
		 */
		_validate_picking (picking_id, params) {
			var url = '/my/picking/' + picking_id + '/validate';

			return this._rpc({
				route: url, params,
			}).then(function() {
				window.location.reload();
			});
		},
	
        
        		/**
		 * @private
		 */
		_remark_update (e) {
            let x_studio_shipment_remarks = $('#x_studio_shipment_remarks').val();
			
			let params = {}

            params['x_studio_shipment_remarks'] = x_studio_shipment_remarks
			params['order_id'] = $('#remark_update').val();
            var url = '/my/purchase/'+params['order_id']+'/update_remarks';
         
            return this._rpc({
				route: url,params,
            }).then(function () {
                $('#x_studio_shipment_remarks').val(params['x_studio_shipment_remarks']);
				window.location.reload();
			});
		

        },
                
        		/**
		 * @private
		 */
        _shipmentdate_update(e) {
        
            let x_studio_shipmentdate = $('#shipmentdate').val();

            let params = {}
            params['shipmentdate'] = x_studio_shipmentdate
            params['order_id'] = $('#order_id').val();

			console.log(e);
            var url = '/my/purchase/'+params['order_id']+'/update_status';
          

            return this._rpc({
				route: url,params,
            }).then(function () {
              
				window.location.reload();
			});
		
		//	this._validate_picking(picking_id, params);
		},

        _delayed_shipmentdate_update(e) {
        
            let x_studio_shipmentdate = $('#delayed_shipmentdate').val();

            let params = {}
            params['delayed_shipmentdate'] = x_studio_shipmentdate
            params['order_id'] = $('#order_id').val();

			console.log(e);
            var url = '/my/purchase/'+params['order_id']+'/update_delayed_date';
          

            return this._rpc({
				route: url,params,
            }).then(function () {
              
				window.location.reload();
			});
		
		//	this._validate_picking(picking_id, params);
		},



	
	});
});
