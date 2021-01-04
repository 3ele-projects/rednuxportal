# -*- coding: utf-8 -*-
{
    'name': "rednuxportal",

    'summary': """
        Customize odoo myPortal for Rednux""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sebastian Weiss",
    'website': "https://lightweb-media.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
	'depends' : ['base','website','purchase','vendor_purchase_order','sale', 'delivery', 'purchase_stock', 'portal'],

    # always loaded
    'data': [
   		'security/security.xml',
        'views/views.xml',
         'views/web.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
      #  'demo/demo.xml',
    ],
}
