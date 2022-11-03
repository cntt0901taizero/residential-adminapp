from odoo import models, fields


class tb_khoinha(models.Model):
    _name = 'tb_khoinha'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Khối nhà'

    name = fields.Char(string='Tên khối nhà', required=True, copy=False,)
    ma = fields.Char(string='Mã khối nhà',  copy=False,)
    toa_nha_ids = fields.One2many('tb_toanha', 'khoi_nha_id', string='Toà nhà')
    trang_thai = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.trang_thai = True

    _sql_constraints = [
        ('ma', 'unique(ma)', 'Mã khối nhà không được trùng lặp')
    ]
