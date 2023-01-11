from builtins import print

from odoo import models, fields


class tb_paybill_configrender(models.Model):
    _name = 'tb_paybill_configrender'
    _description = 'Cấu hình file thanh toán phí'

    fee_kind_id = fields.Char(string='Id loại phí', copy=False)
    fee_kind_code = fields.Char(string='Mã loại phí', copy=False)
    fee_kind_name = fields.Char(string='Tên loại phí', copy=False)

    block_house_id = fields.Char(string='Id dự án', copy=False)
    block_house_code = fields.Char(string='Mã dự án', copy=False)
    block_house_name = fields.Char(string='Tên dự án', copy=False)

    building_id = fields.Char(string='Id tòa nhà', copy=False)
    building_code = fields.Char(string='Mã tòa nhà', copy=False)
    building_name = fields.Char(string='Tên tòa nhà', copy=False)

    house_id = fields.Char(string='Id căn hộ', copy=False)
    house_code = fields.Char(string='Mã căn hộ', copy=False)
    house_number = fields.Char(string='Số nhà', copy=False)

    price = fields.Char(string='giá phí thanh toán', copy=False)

    is_active = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.is_active = True

