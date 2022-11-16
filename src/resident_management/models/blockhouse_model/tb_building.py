from odoo import models, fields


class tb_building(models.Model):
    _name = 'tb_building'
    _description = 'Toà nhà'

    name = fields.Char(string='Tên toà nhà', size=200, required=True, copy=False,)
    code = fields.Char(string='Mã toà nhà', size=50, required=True, copy=False,)
    total_floors = fields.Integer(string='Tổng số tầng', copy=False,)
    founding_date = fields.Date(string='Ngày thành lập', copy=False,)
    image = fields.Image(string='Ngày thành lập', copy=False,)
    address = fields.Char(string='Địa chỉ', size=500, copy=False,)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Toà nhà")
    is_active = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.is_active = True

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên tòa nhà không được trùng lặp'),
        ('code', 'unique(code)', 'Mã tòa nhà không được trùng lặp')
    ]



