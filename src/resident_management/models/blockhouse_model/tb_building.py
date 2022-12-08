from odoo import models, fields


class tb_building(models.Model):
    _name = 'tb_building'
    _description = 'Toà nhà'

    name = fields.Char(string='Tên toà nhà', size=200, required=True, copy=False)
    code = fields.Char(string='Mã toà nhà', size=50, required=True, copy=False)
    total_floors = fields.Integer(string='Tổng số tầng sàn', copy=False)
    founding_date = fields.Date(string='Ngày thành lập', copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    address = fields.Char(string='Địa chỉ', size=500, copy=False)
    website = fields.Char(string='Website', size=200, copy=False)
    phone = fields.Char(string='Điện thoại', size=50, copy=False)
    location_link = fields.Char(string='link vị trí', size=500, copy=False)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Khối nhà", required=True)
    building_floors_id = fields.One2many('tb_building_floors', 'building_id', string="Tầng sàn")
    building_house_id = fields.One2many('tb_building_house', 'building_id', string="Căn hộ")

    def set_status_active(self):
        self.is_active = True

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên tòa nhà không được trùng lặp'),
        ('code', 'unique(code)', 'Mã tòa nhà không được trùng lặp')
    ]




