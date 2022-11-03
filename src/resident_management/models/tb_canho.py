from odoo import models, fields

class tb_canho(models.Model):
    _name = 'tb_canho'
    _description = 'Căn hộ'

    name = fields.Char(string='Tên căn hộ', required=True, copy=False, )
    ma = fields.Char(string='Mã căn hộ', required=True, copy=False, )
    chu_so_huu = fields.Many2one(comodel_name='res.users', string="Chủ sở hữu")
    toa_nha_ids = fields.Many2one(comodel_name='tb_toanha', string="Toà nhà")
    trang_thai = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.trang_thai = True

    _sql_constraints = [
        ('ma', 'unique(ma)', 'Mã căn hộ không được trùng lặp')
    ]