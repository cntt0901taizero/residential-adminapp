from pkg_resources import _
from odoo import models, fields, api
from datetime import date
import random


class tb_building(models.Model):
    _name = 'tb_building'
    _description = 'Toà nhà'

    name = fields.Char(string='Tên toà nhà', size=200, required=True, copy=False)
    code = fields.Char(string='Mã toà nhà', default='_generate_code', size=50, required=True, copy=False, readonly=True)
    total_floors = fields.Integer(string='Tổng số tầng sàn', copy=False)
    founding_date = fields.Date(string='Ngày thành lập', copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    address = fields.Char(string='Địa chỉ', size=500, copy=False)
    website = fields.Char(string='Website', size=200, copy=False)
    phone = fields.Char(string='Điện thoại', size=50, copy=False)
    location_link = fields.Char(string='Link vị trí', size=500, copy=False)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà", required=True)
    building_floors_ids = fields.One2many('tb_building_floors', 'building_id', string="Tầng sàn")
    building_house_ids = fields.One2many('tb_building_house', 'building_id', string="Căn hộ")

    def set_status_active(self):
        self.is_active = True

    @api.model
    def generate_code(self):
        today = date.today()
        d = today.strftime('%d%m%y')
        return str('BD' + d + random.randint(1000, 9999))

    def create_building_floors(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới Tầng sàn',
            'res_model': 'tb_building_floors',
            'target': 'new',
            'view_id': self.env.ref('resident_management.view_tb_building_floors_form').id,
            'view_mode': 'form',
            'context': {
                'default_building_id': self.id,
                'default_blockhouse_id': self.blockhouse_id.id,
            },
        }

    def create_building_house(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Building house'),
            'res_model': 'tb_building_house',
            'target': 'new',
            'view_id': self.env.ref('resident_management.view_tb_building_house_form').id,
            'view_mode': 'form',
            'context': {
                'default_building_id': self.id,
                'default_blockhouse_id': self.blockhouse_id.id,
            },
        }

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên tòa nhà không được trùng lặp'),
        ('code', 'unique(code)', 'Mã tòa nhà không được trùng lặp')
    ]




