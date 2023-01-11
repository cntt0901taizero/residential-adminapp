from builtins import print

from odoo import models, fields


class tb_banner(models.Model):
    _name = 'tb_banner'
    _description = 'Quản lý banner'

    name = fields.Char(string='Tên banner', required=True, copy=False)
    banner_description = fields.Text(string='Mô tả', copy=False)
    image = fields.Image(string="Ảnh")
    link = fields.Char(string='Link', size=500, copy=False)
    sort = fields.Integer(string='Thứ tự', copy=False)
    status = fields.Selection([
        ('PENDING', 'Chờ duyệt'),
        ('ACTIVE', 'Đã duyệt'),
        ('REJECT', 'Chưa duyệt'),
    ], required=True, default='PENDING', tracking=True, string="Trạng thái")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="dự án", ondelet="cascade")





