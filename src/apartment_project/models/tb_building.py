from odoo import models, fields, api
from datetime import date
import random

BUILDING_LEVEL = [
    ('none)', '--'),
    ('a', 'Hạng A'),
    ('b', 'Hạng B'),
    ('c', 'Hạng C'),
]

class tb_building(models.Model):
    _name = 'tb_building'
    _description = 'Toà nhà'

    name = fields.Char(string='Tên toà nhà', size=200, required=True, copy=False)
    code = fields.Char(string='Mã toà nhà', size=50, copy=False, readonly=True)
    founding_date = fields.Date(string='Ngày thành lập', copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    address = fields.Char(string='Địa chỉ', size=500, copy=False)
    website = fields.Char(string='Website', size=200, copy=False)
    phone = fields.Char(string='Điện thoại', size=50, copy=False)
    location_link = fields.Char(string='Link vị trí', size=500, copy=False)
    floors_above_ground_number = fields.Integer(string='Số tầng nổi', copy=False)
    floors_below_ground_number = fields.Integer(string='Số tầng hầm', copy=False)
    building_level = fields.Selection(string='Hạng tòa nhà', selection=BUILDING_LEVEL, default=BUILDING_LEVEL[0][0])
    is_active = fields.Boolean(string='Trạng thái', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà", ondelet="cascade")

    building_floors_ids = fields.One2many(comodel_name='tb_building_floors', inverse_name='building_id', string="Tầng sàn")
    building_house_ids = fields.One2many(comodel_name='tb_building_house', inverse_name='building_id', string="Căn hộ")

    def set_status_active(self):
        self.is_active = True

    @api.model
    def create(self, vals):
        today = date.today()
        d = today.strftime('%d%m%y')
        vals["code"] = 'BD' + str(d) + str(random.randint(1000, 9999))
        return super(tb_building, self).create(vals)

    def create_building_floors(self):
        max_number: int = 0
        if self.building_floors_ids.ids:
            max_number = max(self.building_floors_ids.ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới Tầng sàn',
            'res_model': 'tb_building_floors',
            'target': 'new',
            'view_id': self.env.ref('apartment_project.view_tb_building_floors_form').id,
            'view_mode': 'form',
            'context': {
                'default_building_id': self.id,
                'default_blockhouse_id': self.blockhouse_id.id,
                'default_sort': max_number + 1,
            },
        }

    def create_building_house(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới Căn hộ',
            'res_model': 'tb_building_house',
            'target': 'new',
            'view_id': self.env.ref('apartment_project.view_tb_building_house_form').id,
            'view_mode': 'form',
            'context': {
                'default_building_id': self.id,
                'default_blockhouse_id': self.blockhouse_id.id,
            },
        }

    # def create_building(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Tạo mới khu/tòa nhà',
    #         'res_model': 'tb_building',
    #         'target': 'new',
    #         'view_id': self.env.ref('apartment_project.view_tb_building_form').id,
    #         'view_mode': 'form',
    #         'context': {
    #             'default_blockhouse_id': self.blockhouse_id.id,
    #         },
    #     }

    _sql_constraints = [
        ('code', 'unique(code)', 'Mã tòa nhà không được trùng lặp')
    ]




