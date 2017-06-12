# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class UnrelatedDocumentsReport(models.Model):
    """Documents not related to any concession"""

    _name = "sicon.unrelated_documents.report"
    _auto = False

    dependence_id = fields.Many2one(
        comodel_name='tmc.dependence',
        readonly=True
    )

    document_type_id = fields.Many2one(
        comodel_name='tmc.document_type',
        readonly=True
    )

    number = fields.Integer(
        readonly=True
    )

    period = fields.Integer(
        readonly=True
    )

    document_object = fields.Char(
        readonly=True
    )

    name = fields.Char(
        string='Document',
        readonly=True
    )

    _depends = {
        'tmc.document': ['name', 'document_object', 'main_topic_ids'],
        'sicon.event': ['document_id']
    }

    def _select(self):
        select_str = """
            SELECT
                doc.id,
                doc.document_object,
                doc.name
        """
        return select_str

    def _from(self):
        from_str = """
            tmc_document doc
                LEFT JOIN document_main_topic_rel rel
                    ON (rel.tmc_document_id = doc.id)
                LEFT JOIN tmc_document_topic doc_topic
                    ON (rel.tmc_document_topic_id = doc_topic.id)
                LEFT JOIN tmc_dependence dep
                    ON doc.dependence_id = dep.id
                LEFT JOIN tmc_document_type doc_type
                    ON doc.document_type_id = doc_type.id
            """
        return from_str

    def _where(self):
        where_str = """
            WHERE doc_topic.name = 'Concesiones Generales'
                AND doc.id NOT IN (
                    SELECT
                        document_id
                        FROM sicon_event e WHERE document_id IS NOT NULL)
        """
        return where_str

    def _order_by(self):
        order_str = """
            ORDER BY doc.period, doc.number
        """
        return order_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._where(),
            self._order_by())
        )
