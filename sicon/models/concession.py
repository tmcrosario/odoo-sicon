# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, Warning


class Concession(models.Model):

    _name = 'sicon.concession'
    _order = 'name'

    _expiration_types_ = [
        ('certain', 'Certain'),
        ('uncertain', 'Uncertain'),
    ]

    _certain_expiration_options_ = [
        ('date', 'Date'),
        ('duration', 'Duration'),
    ]

    _date_units_ = [
        ('days', 'Day(s)'),
        ('months', 'Month(s)'),
        ('years', 'Year(s)'),
    ]

    states = [
        ('tendered', 'Tendered'),
        ('awarded', 'Awarded'),
        ('on_term', 'On Term'),
        ('extended', 'Extended'),
        ('precarious', 'Precarious'),
        ('rescinded', 'Rescinded'),
        ('caducous', 'Caducous'),
    ]

    name = fields.Char(
        required=True
    )

    expired = fields.Boolean(
        compute='_check_if_expired'
    )

    state = fields.Selection(
        selection=states,
        string='State'
    )

    location = fields.Char(
        required=True
    )

    business_category_ids = fields.Many2many(
        comodel_name='sicon.business_category',
        compute='_get_business_categories',
        readonly=True
    )

    concessionaire_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('concessionaire', '=', 'True')]
    )

    event_ids = fields.One2many(
        comodel_name='sicon.event',
        inverse_name='concession_id',
    )

    canon = fields.Char()

    start_date = fields.Date()

    expiration_date = fields.Date()

    term_expiration = fields.Selection(
        selection=_expiration_types_
    )

    term_certain_expiration = fields.Selection(
        selection=_certain_expiration_options_,
    )

    term_duration = fields.Integer(
        size=4
    )

    term_unit = fields.Selection(
        selection=_date_units_,
        default='years'
    )

    term_due_date = fields.Date()

    term_description = fields.Text()

    planned_extension = fields.Boolean()

    extension_expiration = fields.Selection(
        selection=_expiration_types_
    )

    extension_certain_expiration = fields.Selection(
        selection=_certain_expiration_options_
    )

    extension_duration = fields.Integer(
        size=4
    )

    extension_unit = fields.Selection(
        selection=_date_units_,
        default='years'
    )

    extension_due_date = fields.Date()

    extension_description = fields.Text()

    highest_highlight = fields.Selection(
        selection=[('high', 'High'),
                   ('medium', 'Medium')],
        compute='_get_highest_highlight'

    )

    highlight_ids = fields.One2many(
        comodel_name='tmc.highlight',
        inverse_name='concession_id'
    )

    highlights_count = fields.Integer(
        compute='_highlights_count'
    )

    event_id = fields.Many2one(
        comodel_name='sicon.event',
        ondelete='cascade'
    )

    event_date = fields.Date(
        related='event_id.date',
        store=True
    )

    concession_id = fields.Many2one(
        comodel_name='sicon.concession',
        ondelete='cascade'
    )

    concession_history_ids = fields.One2many(
        comodel_name='sicon.concession',
        inverse_name='concession_id'
    )

    url_mr = fields.Char()

    url_images = fields.Char()

    @api.model
    def create(self, values):
        if 'concession_id' not in values:
            domain = [
                ('name', '=', values['name']),
                ('concession_id', '=', False)
            ]
            if self.env['sicon.concession'].search(domain, limit=1):
                raise Warning(_('Integrity Error: Duplicated concession'))
            else:
                res_id = super(Concession, self).create(values)
                values['concession_id'] = res_id.id
                super(Concession, self).create(values)
        else:
            res_id = super(Concession, self).create(values)
        return res_id

    @api.onchange('planned_extension')
    def _onchange_planned_extension(self):
        self.extension_expiration = False
        self.extension_certain_expiration = False
        self.extension_duration = False
        self.extension_due_date = False

    @api.onchange('term_expiration')
    def _onchange_term_expiration(self):
        self.term_certain_expiration = False
        self.term_duration = False
        self.term_due_date = False

    @api.onchange('term_certain_expiration')
    def _onchange_term_certain_expiration(self):
        self.term_duration = False
        self.term_due_date = False

    @api.one
    @api.depends('highlight_ids')
    def _highlights_count(self):
        applicable_highlight_ids = self.highlight_ids.filtered(
            lambda record: record.applicable is True
        )
        self.highlights_count = len(applicable_highlight_ids)

    @api.one
    @api.depends('highlight_ids')
    def _get_priority_and_color(self):
        domain = [
            ('concession_id', '=', self.id),
            ('applicable', '=', True)
        ]
        related_highlights = self.env['tmc.highlight'].search(domain)

        highest = related_highlights.sorted(
            key=lambda r: r.highlight_level_id.priority,
            reverse=True)

        if highest:
            highlight = highest[0]
            highlight_level = highlight.highlight_level_id
            self.priority = highlight_level.priority
            self.color = highlight.color

    @api.one
    @api.depends('concessionaire_id')
    def _get_business_categories(self):
        domain = [
            ('concessionaire_id', '=', self.concessionaire_id.id)
        ]
        concessionaire_drei_accounts = self.env['sicon.drei'].search(domain)
        self.business_category_ids = concessionaire_drei_accounts.mapped(
            'business_category_ids'
        )

    @api.multi
    def add_event(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sicon.add_event_wizard',
            'target': 'new'
        }

    @api.one
    @api.depends('expiration_date')
    def _check_if_expired(self):
        if self.expiration_date:
            today = fields.Date.from_string(fields.Date.today())
            if fields.Date.from_string(self.expiration_date) <= today:
                self.expired = True
            else:
                self.expired = False

    @api.one
    @api.depends('highlight_ids')
    def _get_highest_highlight(self):
        high_highlights = self.env['tmc.highlight'].search([
            ('concession_id', '=', self.id),
            ('applicable', '=', True),
            ('level', '=', 'high')]
        )
        medium_highlights = self.env['tmc.highlight'].search([
            ('concession_id', '=', self.id),
            ('applicable', '=', True),
            ('level', '=', 'medium')]
        )
        if high_highlights:
            self.highest_highlight = 'high'
        elif medium_highlights:
            self.highest_highlight = 'medium'

    @api.multi
    def open_url(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.env.context['url'],
            'target': 'new',
        }

    @api.model
    def _prepare_url(self, url, replace):
        assert url, 'Missing URL'
        for key, value in replace.iteritems():
            if not isinstance(value, (str, unicode)):
                # For latitude and longitude which are floats
                value = unicode(value)
            url = url.replace(key, value)
        return url

    @api.multi
    def open_map(self):
        self.ensure_one()
        map_website = self.env.user.context_map_website_id
        if not map_website:
            raise UserError(
                _('Missing map provider: '
                  'you should set it in your preferences.'))
        else:
            if not map_website.address_url:
                raise UserError(
                    _("Missing parameter 'URL that uses the address' "
                      "for map website '%s'.") % map_website.name)
            addr = []
            if self.location:
                addr.append(self.location)
                addr.append('Rosario')
                url = self._prepare_url(
                    map_website.address_url,
                    {'{ADDRESS}': ' '.join(addr)})
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
