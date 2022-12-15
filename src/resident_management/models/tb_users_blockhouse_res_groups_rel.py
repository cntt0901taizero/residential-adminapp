from odoo import models, fields, api

class tb_users_blockhouse_res_groups_rel(models.Model):
    _name = 'tb_users_blockhouse_res_groups_rel'

    name = fields.Selection([
        ('ADMINISTRATION', 'Ban quản trị'),
        ('MANAGEMENT', 'Ban quản lý'),
        ('RESIDENT', 'Cư dân'),
    ], required=True, default='RESIDENT', string="Nhóm người dùng", )
    user_id = fields.Many2one(comodel_name='res_user')
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string='Khối nhà')
    building_id = fields.Many2one(comodel_name='tb_building', string='Tòa nhà')
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string='Căn hộ')
    owner = fields.Boolean(string='Chủ sở hữu', default=False)
