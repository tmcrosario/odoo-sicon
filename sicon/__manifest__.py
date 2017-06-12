# -*- coding: utf-8 -*-

{
    'name': "TMC SICON",
    'version': '10.0.1.0.0',
    'summary': 'Sistema de Concesiones Generales',
    'author': 'Tribunal Municipal de Cuentas - Municipalidad de Rosario',
    'website': 'https://www.tmcrosario.gob.ar',
    'license': 'AGPL-3',
    'sequence': 150,
    'depends': [
        'tmc',
        'partner_tmc',
        'partner_fiscal',
        'municipal',
        'partner_municipal',
        'partner_external_map'
    ],
    'data': [
        # 'security/sicon_group.xml',
        # 'security/ir.model.access.csv',
        'views/highlight.xml',
        'views/concession.xml',
        'views/event.xml',
        'views/event_type.xml',
        'views/partner.xml',
        'report/unrelated_documents.xml',
        'views/menu.xml',
        'views/wizards.xml',
        # 'schedule/schedule.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'qweb': []
}
