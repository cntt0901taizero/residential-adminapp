from odoo import models, fields


class tb_blockhouse(models.Model):
    _name = 'tb_blockhouse'
    _description = 'Khối nhà'

    name = fields.Char(string='Tên khối nhà', size=200, required=True, copy=False,)
    code = fields.Char(string='Mã khối nhà', size=50,  copy=False,)
    address = fields.Char(string='Địa chỉ', size=500, copy=False, )
    image = fields.Image(string='Ảnh', copy=False,)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.is_active = True

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên khối nhà không được trùng lặp'),
        ('code', 'unique(code)', 'Mã khối nhà không được trùng lặp')
    ]
