from odoo import models, fields, api


class tb_users_blockhouse_res_groups_rel(models.Model):
    _name = 'tb_users_blockhouse_res_groups_rel'

    group_id = fields.Many2one(comodel_name='res.groups', string='Nhóm người dùng',
                               domain="[('category_id', '=', 104)]")
    selected_group = fields.Char(related='group_id.name')
    name = fields.Selection([
        ('ADMINISTRATION', 'Ban quản trị'),
        ('MANAGEMENT', 'Ban quản lý'),
        ('RESIDENT', 'Cư dân'),
    ], required=True, default='RESIDENT', string="Nhóm người dùng", )
    user_id = fields.Many2one(comodel_name='res.users')
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string='Khối nhà')
    building_id = fields.Many2one(comodel_name='tb_building', string='Tòa nhà',
                                  domain="[('blockhouse_id', '=', blockhouse_id)]")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string='Căn hộ',
                                        domain="[('building_id', '=', building_id)]")
    owner = fields.Boolean(string='Chủ sở hữu', default=False)

    @api.onchange('blockhouse_id')
    def _on_change_blockhouse_id(self):
        self.building_id = None
        self.building_house_id = None

    @api.onchange('building_id')
    def _on_change_building_id(self):
        self.building_house_id = None
