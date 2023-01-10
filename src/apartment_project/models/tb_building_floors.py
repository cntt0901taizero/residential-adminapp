from odoo import models, fields, api

FLOORS_TYPES = [
    ('none)', '...'),
    ('tang_ham', 'Tầng hầm'),
    ('ki_thuat)', 'Kĩ thuật'),
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
    floors_type = fields.Selection(string='Loại tầng', selection=FLOORS_TYPES, default=FLOORS_TYPES[0][0])
    is_active = fields.Boolean(string='Trạng thái', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà",
                                    ondelet="cascade", required=True)
    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelet="cascade", required=True)

    building_house_ids = fields.One2many(comodel_name='tb_building_house', string="Căn hộ",
                                         inverse_name='building_floors_id')

    def set_status_active(self):
        self.is_active = True

    def create_building_house(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới Căn hộ',
            'res_model': 'tb_building_house',
            'target': 'new',
            'view_id': self.env.ref('apartment_project.view_tb_building_house_form').id,
            'view_mode': 'form',
            'context': {
                'default_building_floors_id': self.id,
                'default_building_id': self.building_id.id,
                'default_blockhouse_id': self.blockhouse_id.id,
            },
        }

    @api.model
    def default_get(self, data):
        res = super(tb_building_floors, self).default_get(data)
        return res

