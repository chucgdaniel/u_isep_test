# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    experience = fields.One2many('u_isep_test.experience','partner_id',string='Experiencia')
    level_experience = fields.Integer(compute='_get_level_experience',string='Lenguajes o herramientas')
    empty_skills = fields.Boolean()

    """
        Inherit method create
        create a new record empty in experience field when no exist another register
    """
    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if not res.experience:
            experience = [(0, 0, {'partner_id': res.id, 'year': 0, 'percentage': 0 ,'is_blank': True})]
            res.update({'experience': experience})
        return res

    """
        Open wizard for add skills or tools
        context:
            'default_partner_id': id of record
            'skills_ignore': object with added skills or tools
    """
    def open_massive_skills(self):
        return {
            'name':_("Seleccione skills"),
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': False,
            'res_model': 'u_isep_test.load_skill',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_partner_id': self.id, 'skills_ignore': self.experience.skill.ids or []},
        }

    """
        Counter to know how many skills the contact has
    """
    def _get_level_experience(self):
        for s in self:
            s.level_experience = len(s.experience)

    """
        Method to calculate how many skills have been used and limit the wizard
        'skills': count of all skills or tools
        
    """
    @api.onchange('experience')
    def _get_empty_skills(self):
        skills = len(self.env['u_isep_test.skill'].sudo().search([]))
        for s in self:
            if s.experience:
                # if the added skills exceed the existing ones, the option to open the wizard is disabled
                s.empty_skills = True if len(s.experience) >= skills else False

    """
        Validate that the years and percentage are positive
    """
    @api.constrains('experience')
    def _constrains_validate(self):
        for s in self:
            for e in s.experience:
                # if the record is not blank (the default if not exist records)
                if not e.is_blank and not e.is_massive:
                    # validate
                    if e.year <= 0 or e.percentage <= 0:
                        raise ValidationError("Los años de experiencia o el porcentaje no debe ser 0")
                    elif e.percentage > 100:
                        raise ValidationError("El porcentaje no puede ser mayor a 100")