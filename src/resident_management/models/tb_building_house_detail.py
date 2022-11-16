from odoo import models, fields


class tb_building_house_detail(models.Model):
    _name = 'tb_building_house_detail'
    _description = 'Chi tiết căn hộ'

    address = fields.Char(string='Địa chỉ', size=200, copy=False, )
    house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ")
    building_floors_id = fields.Many2one(comodel_name='tb_building_floors', string="Tầng số")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Toà nhà")
    owner = fields.Many2one(comodel_name='res.users', string="Chủ sở hữu")
    resident_info_json = fields.Char(string='thông tin cư dân json', copy=False, )

