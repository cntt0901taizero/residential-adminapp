from builtins import print

from odoo import models, fields


class tb_feekind(models.Model):
    _name = 'tb_feekind'
    _description = 'Danh mục phí'

    name = fields.Char(string='Tên phí', required=True, copy=False)
    code = fields.Char(string='Mã', required=True, copy=False)
    note = fields.Text(string='Ghi chú', copy=False, help='Ghi rõ ràng các khoản phí (nếu có)')
    is_active = fields.Boolean(string='Trạng thái', default=True)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án", ondelet="cascade")

    def set_status_active(self):
        self.is_active = True




