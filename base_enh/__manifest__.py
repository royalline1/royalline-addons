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
    'depends': ['base','contacts','sale'],

    'data': [
       'security/ir.model.access.csv',
       'views/views.xml',
       'views/final_dest_view.xml',
       'views/container_size_view.xml',
       'views/agreement_method_view.xml',
       'views/custoemr_class_view.xml',
       'report/sale_report.xml'
    ],
}