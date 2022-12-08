from odoo import models, fields


class tb_building_house(models.Model):
    _name = 'tb_building_house'
    _description = 'Căn hộ'

    code = fields.Char(string='Mã căn hộ', size=50, required=True, copy=False)
    name = fields.Char(string='Số nhà', size=50, copy=False)
    address = fields.Char(string='Địa chỉ', size=200, copy=False)
    # resident_info_json = fields.Char(string='thông tin cư dân json', copy=False)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    owner = fields.Many2one(comodel_name='res.users', string="Chủ sở hữu")
    building_floors_id = fields.Many2one(comodel_name='tb_building_floors', string="Tầng sàn", required=True)
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà", required=True)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà", required=True)

    def set_status_active(self):
        self.is_active = True

    _sql_constraints = [
        ('code', 'unique(code)', 'Mã căn hộ không được trùng lặp')
    ]


