from odoo import models, fields, api
from datetime import date
import random

HOUSE_TYPES = [
    ('none)', '...'),
    ('studio', 'Studio'),
    ('officetel', 'Officetel'),
    ('shophouse', 'Shophouse'),
    ('dualkey', 'Dualkey'),
    ('penhouse', 'Penhouse'),
    ('duplex', 'Duplex'),
    ('skyvilla', 'Skyvilla'),
    ('normal', 'Normal'),
]


class tb_building_house(models.Model):
    _name = 'tb_building_house'
    _description = 'Căn hộ'

    name = fields.Char(string='Số nhà', size=50, copy=False)
    code = fields.Char(string='Mã căn hộ', size=50, copy=False, readonly=True)
    address = fields.Char(string='Địa chỉ', size=200, copy=False)
    # resident_info_json = fields.Char(string='thông tin cư dân json', copy=False)
    house_type = fields.Selection(string='Loại hình căn hộ', selection=HOUSE_TYPES, default=HOUSE_TYPES[0][0])

    area_apartment = fields.Float(string='Diên tích căn hộ (m²)', copy=False)
    bedroom_number = fields.Integer(string='Số phòng ngủ', copy=False)
    bathroom_number = fields.Integer(string='Số phòng tắm', copy=False)
    balcony_number = fields.Integer(string='Số ban công', copy=False)
    fee_base = fields.Float(string='Phí cơ bản (vnđ)', copy=False)
    detailed_description = fields.Text(string='Mô tả chi tiết', copy=False)

    is_active = fields.Boolean(string='Trạng thái', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà", required=True)
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]", required=True)
    building_floors_id = fields.Many2one(comodel_name='tb_building_floors', string="Tầng sàn",
                                         domain="[('building_id', '=', building_id)]", required=True)

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


