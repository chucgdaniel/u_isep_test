# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GenerateReport(models.TransientModel):
    _name = 'u_isep_test.generate_report'
    _description = 'generate reports'

    skills = fields.Many2many('u_isep_test.skill',string='Filtre por lenguajes o herramientas')
    order = fields.Selection(selection=
        [('DESC', 'Descendente'),
        ('ASC', 'Asendente')],
        string=('Seleccione orden de resultados'),default="DESC"
    )
    by_year = fields.Boolean(string='Por años',default=True)
    by_percentage = fields.Boolean(string='Por porcentaje',default=True)
    limit = fields.Integer(string='Seleccione el limite de registros',default=10)

    """
        Validate if limit is negative
        return error
    """
    def _validate_limit(self):
        if self.limit <= 0:
            raise ValidationError("El limite no puede ser 0")

    """
        Validate if exist records
        return error if not
        return the result, opposite case
    """
    def _validate_records(self,result):
        if not result:
            raise ValidationError("No se encontraron registros")
        else:
            return result

    """
        Find records based in conditions of wizard
    """
    def find(self):
        domain = []
        order_selection = (self.order).lower() if self.order else ''
        self._validate_limit() # call validation
        # conditions
        if self.skills:
            domain.append(('skill','in',self.skills.ids))
        if self.by_year == True and self.by_percentage == True:
            order = 'year ' + order_selection + ',' + 'percentage ' + order_selection
        elif self.by_year:
            order = 'year ' + order_selection
        elif self.by_percentage:
            order = 'percentage ' + order_selection
        else:
            order = 'year asc, percentage asc'
        # find result
        result = self.env['u_isep_test.experience'].sudo().search(domain,order=order,limit=self.limit)
        # validate result
        result = self._validate_records(result)
        # create dict with the result
        result = self._parse_data(result)
        # generate pdf
        return self.env.ref('u_isep_test.action_report_experience').report_action(self,data=result,config=False)

    """
        Parse the data for to loop through it in the template and display the results
        return the dictonary + object with another dictonary
    """
    def _parse_data(self,result):
        records = []
        # create object
        for r in result:
            record = {
                'name' : r.partner_id.name,
                'skill': r.skill.name,
                'year': r.year,
                'percentage': r.percentage
            }
            # save in object
            records.append(record)
        # add to a dict
        return {'records':records}

