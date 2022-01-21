# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LoadSkill(models.TransientModel):
    _name = 'u_isep_test.load_skill'
    _description = 'load skills in view res_partner'

    skills = fields.Many2many('u_isep_test.skill',string='Skills',required=True,domain="[('id', 'not in', context.get('skills_ignore'))]")
    partner_id = fields.Many2one('res.partner')
    empty_skills = fields.Boolean(default=False)

    """
        add records to one2many in res_partner
    """
    def load_skills(self):
        if not self.skills:
            raise ValidationError("Los campos son requeridos")
        else:
            line_skills = []
            # create dictonary
            for s in self.skills:
                line_skill = {
                    'partner_id': self.partner_id.id,
                    'skill': s.id,
                    'year': 0, 
                    'percentage': 0,
                    'is_massive': True
                }
                line_skills.append((0,0,line_skill))
            # in this case delete record if exist in blank
            blank_record = [e for e in self.partner_id.experience if e.is_blank]
            if blank_record:
                blank_record[len(blank_record) - 1].unlink()
            # add
            self.partner_id.experience = line_skills
            # update the limit
            self.partner_id._get_empty_skills()