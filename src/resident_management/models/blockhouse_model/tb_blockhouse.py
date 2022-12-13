from odoo import models, fields, api
from datetime import date
import random


class tb_blockhouse(models.Model):
    _name = 'tb_blockhouse'
    _description = 'Khối nhà'

    name = fields.Char(string='Tên khối nhà', size=200, required=True, copy=False)
    code = fields.Char(string='Mã khối nhà', default='_generate_code', size=50, required=True, copy=False, readonly=True)
    address = fields.Char(string='Địa chỉ', size=500, copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    website = fields.Char(string='Website', size=200, copy=False)
    phone = fields.Char(string='Điện thoại', size=50, copy=False)
    location_link = fields.Char(string='Link vị trí', size=500, copy=False)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    building_ids = fields.One2many('tb_building', 'blockhouse_id', string="Tòa nhà")

    def set_status_active(self):
        self.is_active = True

    @api.model
    def _generate_code(self):
        today = date.today()
        d = today.strftime('%d%m%y')
        return str('BH' + d + random.randint(1000, 9999))

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên khối nhà không được trùng lặp'),
        ('code', 'unique(code)', 'Mã khối nhà không được trùng lặp')
    ]
