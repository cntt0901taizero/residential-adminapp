from odoo import models, fields, api


class tb_users_blockhouse_res_groups_rel(models.Model):
    _name = 'tb_users_blockhouse_res_groups_rel'

    group_id = fields.Many2one(comodel_name='res.groups', string='Nhóm người dùng',
                               domain="[('category_id', '=', 104)]")
    selected_group = fields.Char(related='group_id.name')
    # name = fields.Selection([
    #     ('ADMINISTRATION', 'Ban quản trị'),
    #     ('MANAGEMENT', 'Ban quản lý'),
    #     ('RESIDENT', 'Cư dân'),
    # ], default='RESIDENT', string="Nhóm người dùng", )
    user_id = fields.Many2one(comodel_name='res.users')
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string='Khối nhà', )
    building_id = fields.Many2one(comodel_name='tb_building', string='Tòa nhà',
                                  domain="[('blockhouse_id', '=', blockhouse_id)]", )
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string='Căn hộ',
                                        domain="[('building_id', '=', building_id)]", )
    owner = fields.Boolean(string='Chủ sở hữu', default=False)

    _sql_constraints = [
        ('building_house_id_unique', 'unique(building_house_id)', 'Bạn đã là cư dân của căn hộ này.'),
    ]

    @api.onchange('blockhouse_id')
    def _on_change_blockhouse_id(self):
        self.building_id = None
        self.building_house_id = None

    @api.onchange('building_id')
    def _on_change_building_id(self):
        self.building_house_id = None

    @api.onchange('group_id')
    def _on_change_blockhouse_id(self):
        self.blockhouse_id = None
        self.building_id = None
        self.building_house_id = None

    # @api.model
    # def create(self, value):
    #     try:
    #         a = value['group_id']
    #         print(value['group_id'])
    #
    #         # self.env.cr.execute("""SELECT count(*) FROM res_groups_users_rel
    #         #                            WHERE uid=%s AND gid=%s""",
    #         #                     (value.user_id, self.group_id))
    #         # total = self.env.cr.fetchone()[0]
    #         # if total == 0:
    #         #     self.env.cr.execute("""INSERT INTO res_groups_users_rel(uid, gid) VALUES(%s, %s)""",
    #         #                         (self.user_id, self.group_id))
    #         super(tb_users_blockhouse_res_groups_rel, self).create(value)
    #     except Exception as e:
    #         print(e)
    #         # super(tb_users_blockhouse_res_groups_rel, self).create(value)
