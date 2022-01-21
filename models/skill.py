# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Skill(models.Model):
    _name = 'u_isep_test.skill'
    _description = 'tools or programming language skills'

    name = fields.Char(string='Nombre',required=True)
    active = fields.Boolean(string='Activo',default=True)