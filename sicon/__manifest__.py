# -*- coding: utf-8 -*-

{
    'name': "TMC SICON",
    'version': '10.0.1.0.0',
    'summary': 'Sistema de Concesiones Generales',
    'author': 'Tribunal Municipal de Cuentas - Municipalidad de Rosario',
    'website': 'https://www.tmcrosario.gob.ar',
    'license': 'AGPL-3',
    'depends': [
        'tmc',
        'document_index',
        'tmc_data',
        'partner_tmc',
        'partner_fiscal',
        'municipal',
        'partner_municipal',
        'partner_external_map'
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/highlight.xml',
        'views/concession.xml',
        'views/event.xml',
        'views/event_type.xml',
        'views/partner.xml',
        'report/unrelated_documents.xml',
        'report/concessions_listing.xml',
        'report/concession.xml',
        'views/wizards.xml',
        'views/menu.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'qweb': []
}
