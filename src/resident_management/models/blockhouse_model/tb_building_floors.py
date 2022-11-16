from odoo import models, fields


class tb_building_floors(models.Model):
    _name = 'tb_building_floors'
    _description = 'Tầng sàn'

    floors_number = fields.Char(string='Số tầng', size=50, copy=False, )
    total_house = fields.Integer(string='Tổng căn hộ', copy=False, )
    is_active = fields.Boolean(string='Trạng thái', default=True)

    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà")

    buiding_house_id = fields.One2many('tb_building_house', 'building_floors_id', string="Căn hộ")

    def set_status_active(self):
        self.is_active = True

