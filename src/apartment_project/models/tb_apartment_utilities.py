from odoo import models, fields

DAYS_LIST = [
    ('2', 'Thứ 2'),
    ('3', 'Thứ 3'),
    ('4', 'Thứ 4'),
    ('5', 'Thứ 5'),
    ('6', 'Thứ 6'),
    ('7', 'Thứ 7'),
    ('cn', 'Chủ nhật'),
]

class tb_apartment_utilities(models.Model):
    _name = 'tb_apartment_utilities'
    _description = 'Tiện ích chung cư'

    name = fields.Char(string='Tên', required=True, copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    description = fields.Text(string='Ghi chú', copy=False, help='')
    active_day = fields.Many2many(string='Ngày hoạt động', selection=DAYS_LIST, default=DAYS_LIST[0][0])
    active_time = fields.Char(string='Giờ hoạt động', size=50,  help='9h30p - 21h')
    is_active = fields.Boolean(string='Trạng thái', default=True)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    ondelet="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelet="cascade")

    def set_status_active(self):
        self.is_active = True




