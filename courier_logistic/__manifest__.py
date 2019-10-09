# -*- coding: utf-8 -*-
{
    'name': "Courier Management",
    'summary': """
        Courier Management.""",

    'description': """
        Courier Management.
    """,

    'author': "Codesk Company",
    'website': "http:www.codesk.systems",

    'category': 'Uncategorized',
    'version': '12.0.1.0',
    'depends': ['base','base_enh','mail','hr_attendance','contacts','base_address_city','hr','base_address_city','base_address_extended'],

    'data': [
       'security/ir.model.access.csv',
       'views/dhl_logistic_views.xml', 
    ],
}
