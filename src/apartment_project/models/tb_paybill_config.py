from builtins import print

from odoo import models, fields


class tb_paybill_config(models.Model):
    _name = 'tb_paybill_config'
    _description = 'Cấu hình thanh toán'

    name = fields.Char(string='Ghi chú', copy=False)
    price = fields.Char(string='giá phí thanh toán', copy=False)
    is_active = fields.Boolean(string='Trạng thái', default=True)
    feekind_id = fields.Many2one(comodel_name='tb_feekind', string="Loại phí", ondelet="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ", ondelet="cascade")

    def set_status_active(self):
        self.is_active = True

