# -*- coding: utf-8 -*-
from odoo import http

# class ExamenUt3(http.Controller):
#     @http.route('/examen_ut3/examen_ut3/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/examen_ut3/examen_ut3/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('examen_ut3.listing', {
#             'root': '/examen_ut3/examen_ut3',
#             'objects': http.request.env['examen_ut3.examen_ut3'].search([]),
#         })

#     @http.route('/examen_ut3/examen_ut3/objects/<model("examen_ut3.examen_ut3"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('examen_ut3.object', {
#             'object': obj
#         })