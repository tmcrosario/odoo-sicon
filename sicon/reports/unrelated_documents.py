# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class unrelated_documents(models.Model):
    """Documents not related to any concession"""

    _name = "sicon.unrelated_documents"
    _auto = False

    dependence_id = fields.Many2one(
        comodel_name='tmc.dependence'
    )

    document_type_id = fields.Many2one(
        comodel_name='tmc.document_type'
    )

    number = fields.Integer()

    period = fields.Integer()

    reference = fields.Char()

    name = fields.Char(
        string='Document'
    )

    def _select(self):
        select_str = """
            SELECT
                doc.id,
                doc.reference,
                doc.name
        """
        return select_str

    def _from(self):
        from_str = """
            tmc_document doc
                LEFT JOIN document_main_purpose_rel rel
                    ON (rel.tmc_document_id = doc.id)
                LEFT JOIN tmc_document_purpose doc_purpose
                    ON (rel.tmc_document_purpose_id = doc_purpose.id)
                LEFT JOIN tmc_dependence dep
                    ON doc.dependence_id = dep.id
                LEFT JOIN tmc_document_type doc_type
                    ON doc.document_type_id = doc_type.id
            """
        return from_str

    def _where(self):
        where_str = """
            WHERE doc_purpose.name = 'Concesiones Generales'
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

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
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
