from odoo import models, fields, api

class tb_users_blochouse_res_groups_rel(models.Model):
    _name = 'tb_users_blochouse_res_groups_rel'

    user_id = fields.Many2one(comodel_name='res_user')
    blochouse_id = fields.Many2one(comodel_name='tb_blockhouse')
    building_id = fields.Many2one(comodel_name='tb_building')
    building_house_id = fields.Many2one(comodel_name='tb_building_house')
    owner = fields.Boolean(string='Chủ sở hữu', default=False)
    role = fields.Selection([
        ('ADMINISTRATION', 'Ban quản trị'),
        ('MANAGEMENT', 'Ban quản lý'),
        ('RESIDENT', 'Cư dân'),
    ], required=True, default='RESIDENT', string="Nhóm người dùng",)