from odoo import api, fields, models, tools


class UnrelatedDocumentsReport(models.Model):

    _name = "sicon.unrelated_documents.report"
    _description = 'Documents not related yet to any concession'
    _auto = False

    dependence_id = fields.Many2one(comodel_name='tmc.dependence',
                                    readonly=True)

    document_type_id = fields.Many2one(comodel_name='tmc.document_type',
                                       readonly=True)

    number = fields.Integer(readonly=True)

    period = fields.Integer(readonly=True)

    document_object = fields.Char(readonly=True)

    name = fields.Char(string='Document', readonly=True)

    _depends = {
        'tmc.document': ['name', 'document_object', 'main_topic_ids'],
        'sicon.event': ['document_id']
    }

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW sicon_unrelated_documents_report AS (
                SELECT
                    doc.id,
                    doc.document_object,
                    doc.name
                FROM (
                    tmc_document doc
                        LEFT JOIN document_main_topic_rel rel
                            ON (rel.tmc_document_id = doc.id)
                        LEFT JOIN tmc_document_topic doc_topic
                            ON (rel.tmc_document_topic_id = doc_topic.id)
                        LEFT JOIN tmc_dependence dep
                            ON doc.dependence_id = dep.id
                        LEFT JOIN tmc_document_type doc_type
                            ON doc.document_type_id = doc_type.id
                )
                WHERE doc_topic.name = 'Concesiones Generales'
                    AND doc_type.abbreviation = 'DEC'
                    AND doc.id NOT IN (
                        SELECT
                            document_id
                            FROM sicon_event e WHERE document_id IS NOT NULL)
                ORDER BY doc.period, doc.number
            )
        """)
