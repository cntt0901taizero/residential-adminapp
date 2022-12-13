from odoo import models, fields, api
from datetime import date
import random

HOUSE_TYPES = [
    ('null)', '...'),
    ('nha_o', 'Nhà ở'),
    ('thue_dv', 'Thuê dịch vụ'),
]


class tb_building_house(models.Model):
    _name = 'tb_building_house'
    _description = 'Căn hộ'

    name = fields.Char(string='Số nhà', size=50, copy=False)
    code = fields.Char(string='Mã căn hộ', size=50, required=True, copy=False, readonly=True)
    address = fields.Char(string='Địa chỉ', size=200, copy=False)
    # resident_info_json = fields.Char(string='thông tin cư dân json', copy=False)
    house_type = fields.Selection(string='Loại căn hộ', selection=HOUSE_TYPES, default=HOUSE_TYPES[0][0])
    is_active = fields.Boolean(string='Trạng thái', default=True)

    owner = fields.Many2one(comodel_name='res.users', string="Chủ sở hữu")
    building_floors_id = fields.Many2one(comodel_name='tb_building_floors', string="Tầng sàn", required=True)
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà", required=True)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà", required=True)

    def set_status_active(self):
        self.is_active = True

    @api.model
    def create(self, vals):
        today = date.today()
        d = today.strftime('%d%m%y')
        vals["code"] = 'BDH' + str(d) + str(random.randint(1000, 9999))
        return super(tb_building_house, self).create(vals)

    @api.model
    def default_get(self, data):
        res = super(tb_building_house, self).default_get(data)
        return res

    _sql_constraints = [
        ('code', 'unique(code)', 'Mã căn hộ không được trùng lặp')
    ]


