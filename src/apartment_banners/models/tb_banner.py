from builtins import print

from odoo import models, fields


class tb_banner(models.Model):
    _name = 'tb_banner'
    _description = 'Quản lý banner'

    name = fields.Char(string='Tên banner', required=True, copy=False)
    banner_description = fields.Text(string='Mô tả', copy=False)
    image = fields.Image(string="Ảnh")





