from odoo import models, fields


class tb_toanha(models.Model):
    _name = 'tb_toanha'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Chung cư/Toà nhà'

    name = fields.Char(string='Tên toà nhà', required=True, copy=False,)
    ma = fields.Char(string='Mã toà nhà', required=True, copy=False,)
    dia_chi = fields.Char(string='Địa chỉ',  copy=False,)
    so_tang = fields.Char(string='Số tầng', copy=False,)
    khoi_nha_id = fields.Many2one(comodel_name='tb_khoinha', string="Toà nhà")
    chat_luong = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], default='2', string="Chất lượng", select=True)
    can_ho_ids = fields.One2many('tb_canho', 'toa_nha_ids', string='Căn hộ')
    trang_thai = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.trang_thai = True


