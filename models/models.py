# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Incidencia(models.Model):
    _name = 'examen_ut3.incidencia'

    name = fields.Char(compute="_calcular_nombre")
    description = fields.Text(required=True)
    fecha_inicio = fields.Date(required=True, default=fields.Date.today)
    fecha_fin = fields.Date(compute="_calcular_fecha_devolucion", store=True)
    cerrada = fields.Boolean(default=False)
    description_fin = fields.Text()
    responsable = fields.Many2one('res.users', string="Usuario", required=True)
    dispositivo_id = fields.Many2one('examen_ut3.dispositivo', required=True, ondelete="cascade")
    ubicacion_id = fields.Many2one('examen_ut3.ubicacion', ondelete="cascade")

    @api.depends('create_date')
    def _calcular_nombre(self):
        for r in self:
            r.name = str(r.create_date).replace("-", "").replace(",", "").replace(":", "").replace(" ", "").replace(".",
                                                                                                                    "")

    @api.onchange('dispositivo_id')
    def _cambiar_ubicacion(self):
        if self.dispositivo_id:
            self.ubicacion_id = self.dispositivo_id.ubicacion_id

    @api.onchange('ubicacion_id')
    def _cambiar_dispositivos(self):
        lista_disp = self.env["examen_ut3.dispositivo"].search([('ubicacion_id.id', '=', self.ubicacion_id.id)])
        if (len(lista_disp) == 1):
            self.dispositivo_id = lista_disp[0]
        elif (len(lista_disp) > 1):
            if (self.dispositivo_id):
                if (self.dispositivo_id.ubicacion_id != self.ubicacion_id):
                    self.dispositivo_id = False

    @api.onchange('fecha_inicio')
    def _nombre_metodo(self):
        if(str(self.fecha_inicio) > str(fields.Date.today(self))):
            warning = {
                'title': ('Error.'),
                'message': ('La fecha de inicio no puede ser superior a la fecha actual.')
            }
            self.fecha_inicio = fields.Date.today(self)
            return {'warning': warning}

    class Dispositivo(models.Model):
        _name = 'examen_ut3.dispositivo'

        name = fields.Char(string="Nombre", required=True)
        description = fields.Text()
        image = fields.Binary(string="Imagen")
        incidencia_ids = fields.One2many('examen_ut3.incidencia', 'dispositivo_id')
        ubicacion_id = fields.Many2one('examen_ut3.ubicacion', required=True, ondelete="cascade")
        num_incidencias = fields.Integer(compute="_calcular_num_incidencias");

        def name_get(self):
            res = []
            for r in self:
                name = r.name + "/" + r.ubicacion_id.name
                res.append((r.id, name))
            return res

        @api.depends('incidencia_ids')
        def _calcular_incidencias(self):
            for r in self:
                r.num_incidencias = len(r.incidencia_ids)

    class Ubicacion(models.Model):
        _name = 'examen_ut3.ubicacion'

        name = fields.Char(required=True)
        description = fields.Text()
        dispositivo_ids = fields.One2many('examen_ut3.dispositivo', 'ubicacion_id')

    class Wizard(models.TransientModel):
        _name = 'examen_ut3.incidenciaswizard'

        def default_incidencias(self):
            return self.env['examen_ut3.incidencia'].browse(self._context.get('active_id'))

        incidencia_id = fields.Many2one('examen_ut3.incidencia', string="Incidencia", required=True, default=default_incidencias,
                                      ondelete="cascade")

        fecha_inicio = fields.Date()
        cerrada = fields.Boolean(default= True)
        description_fin = fields.Text(string="Descripcion", required= True)
        fecha_fin = fields.Date(default=fields.Date.today, required=True)

        @api.onchange('fecha_fin')
        def _nombre_metodo(self):
            if (str(self.fecha_fin) > str(fields.Date.today(self)) or str(self.fecha_fin) < str(self.fecha_inicio)):
                warning = {
                    'title': ('Error.'),
                    'message': ('La fecha de inicio no puede ser superior a la fecha actual ni anterior a la fecha de inicio.')
                }
                self.fecha_fin = fields.Date.today(self)
                return {'warning': warning}

        @api.onchange('incidencia_id')
        def _obtener_fecha(self):
            self.fecha_inicio = self.incidencia_id.fecha_inicio

        @api.multi
        def cerrar_incidencia(self):
            self.incidencia_id.cerrada = self.cerrada
            self.incidencia_id.description_fin = self.description_fin
            self.incidencia_id.fecha_fin = self.fecha_fin
            return{}
