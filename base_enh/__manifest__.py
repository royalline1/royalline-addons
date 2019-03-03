# -*- coding: utf-8 -*-
{
    'name': "Base Enhancement",
    'summary': """
        Summary""",

    'description': """
        description
    """,

    'author': "author",
    'website': "website",

    'category': 'Uncategorized',
    'version': '12.0.1.0',
    'depends': ['base','contacts','sale','base_address_city','product'],

    'data': [
       'security/ir.model.access.csv',
       'views/views.xml',
       'views/final_dest_view.xml',
       'views/container_size_view.xml',
       'views/agreement_method_view.xml',
       'views/custoemr_class_view.xml',
       'report/sale_report.xml',
       'views/customs_declaration_view.xml',
       'views/insurance_type_view.xml',
       'views/track_type_view.xml',
       'views/weight_type_view.xml',
       'views/vesel_views.xml'
    ],
}