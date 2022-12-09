from odoo import models, fields

FLOORS_TYPES = [
    ('ki_thuat)', 'Kĩ thuật'),
    ('tang_ham', 'Tầng hầm'),
    ('thuong_mai', 'Thương mại'),
    ('van_phong', 'Văn phòng'),
    ('can_ho', 'Căn hộ'),
]


class tb_building_floors(models.Model):
    _name = 'tb_building_floors'
    _description = 'Tầng sàn'

    name = fields.Char(string='Tên tầng sàn', size=100, required=True, copy=False)
    sort = fields.Integer(string='Thứ tự', copy=False)
    total_house = fields.Integer(string='Tổng căn hộ', copy=False)
    floors_type = fields.Selection(string='Loại tầng', selection=FLOORS_TYPES)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà", required=True)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà", required=True)
    building_house_ids = fields.One2many('tb_building_house', 'building_floors_id', string="Căn hộ")

    def set_status_active(self):
        self.is_active = True

