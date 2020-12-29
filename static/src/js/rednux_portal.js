odoo.define('rednuxportal.portal_my_purchase_order', function (require) {
	'use strict';

	var publicWidget = require('web.public.widget');

	publicWidget.registry.delivery_order = publicWidget.Widget.extend({
		selector: '.o_form_rednux_lieferanten',
		events: {

			'click #remark_update': '_remark_update',
		},

		//--------------------------------------------------------------------------
		// Handlers
		//--------------------------------------------------------------------------

	
        
        		/**
		 * @private
		 */
		_remark_update (e) {
            let x_studio_shipment_remarks = $('#x_studio_shipment_remarks').val();

            let params = {}
            params['x_studio_shipment_remarks'] = x_studio_shipment_remarks
            params['order_id'] = 13
            var url = window.location.href +'/update_remarks';
            //window.location.reload();
            console.log(url);
            return this._rpc({
				route: url,params,
            }).then(function () {
                $('#x_studio_shipment_remarks').val(params['x_studio_shipment_remarks']);
				//window.location.reload();
			});
		
		//	this._validate_picking(picking_id, params);
		},
	
	});
});
