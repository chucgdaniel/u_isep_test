# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Experience(models.Model):
    _name = 'u_isep_test.experience'
    _description = 'show the experience of contacts'

    name = fields.Char(string='Nombre',compute='_get_name')
    partner_id = fields.Many2one('res.partner',string='Contacto')
    skill = fields.Many2one('u_isep_test.skill',string='Lenguaje o herramienta')
    year = fields.Integer(string='Años de experiencia',required=True)
    percentage = fields.Integer(string='Porcentaje %',required=True)
    company_id = fields.Many2one('res.company',string='Compañia',default=lambda self: self.env.user.company_id)
    is_blank = fields.Boolean(default=False) # flags
    is_massive = fields.Boolean(default=False) # flags

    """
        Compute name based in name of partner, skill and percentage 
    """
    @api.depends('skill','percentage')
    def _get_name(self):
        for s in self:
            if s.skill != False and (s.percentage != 0 and s.percentage != False):
                s.name = s.partner_id.name + ' / ' + s.skill.name + ' / ' + str(s.percentage)
            else:
                s.name = ''

    """
        Create a domain so as not to repeat skills
    """
    @api.onchange('partner_id','skill')
    def _change_skill(self):
        if self.partner_id:
            return {'domain': {'skill': [('id', 'not in', self.partner_id.experience.skill.ids)]}}

    """
        Validate that the years and percentage are positive
    """
    @api.constrains('year','percentage')
    def _constrains_validate(self):
        for s in self:
            # if the record is not blank (the default if not exist records)
            if not s.is_blank and not s.is_massive:
                if s.year <= 0 or s.percentage <= 0:
                    raise ValidationError("Los años de experiencia o el porcentaje no debe ser 0")
                elif s.percentage > 100:
                    raise ValidationError("El porcentaje no puede ser mayor a 100")