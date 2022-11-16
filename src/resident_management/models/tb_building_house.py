from odoo import models, fields


class tb_building_house(models.Model):
    _name = 'tb_building_house'
    _description = 'Căn hộ'

    code = fields.Char(string='Mã căn hộ', size=50, required=True, copy=False, )
    house_number = fields.Char(string='Số nhà', size=50, copy=False, )
    address = fields.Char(string='Địa chỉ', size=200, copy=False, )
    building_floors_id = fields.Many2one(comodel_name='tb_building_floors', string="Tầng số")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Toà nhà")
    owner = fields.Many2one(comodel_name='res.users', string="Chủ sở hữu")
    is_active = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.is_active = True

    _sql_constraints = [
        ('code', 'unique(code)', 'Mã căn hộ không được trùng lặp')
    ]