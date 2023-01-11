from odoo import models, fields

VEHICLE_TYPES = [
    ('bicycle', 'Xe đạp'),
    ('motorbike', 'Xe máy'),
    ('car', 'Ô tô'),
]

class tb_vehicle(models.Model):
    _name = 'tb_vehicle'
    _description = 'Phương tiện'

    name = fields.Char(string='Tên phí', required=True, copy=False)  # license_plates
    vehicle_type = fields.Selection(string='Loại xe', selection=VEHICLE_TYPES, default=VEHICLE_TYPES[0][0])
    note = fields.Text(string='Ghi chú', copy=False, help='Ghi rõ ràng các khoản phí (nếu có)')
    is_active = fields.Boolean(string='Trạng thái', default=True)
    user_id = fields.Many2one(comodel_name='res.users', string="Chủ xe", ondelet="cascade")

    def set_status_active(self):
        self.is_active = True




