from odoo import models, fields, api
from odoo.exceptions import ValidationError

RELATIONSHIP_TYPES = [
    ('none', '--'),
    ('chuho', 'Chủ hộ'),
    ('ongba', 'Ông bà'),
    ('bome', 'Bố mẹ'),
    ('vochong', 'Vợ chồng'),
    ('concai', 'Con cái'),
    ('anhchiem', 'Anh chị em'),
    ('nguoithue', 'Người thuê'),
]

USER_GROUP_CODE = [
    ('none', '--'),
    ('[CD]', '[CD]'),
    ('[BQL]', '[BQL]'),
    ('[BQT]', '[BQT]'),
]


class tb_users_blockhouse_res_groups_rel(models.Model):
    _name = 'tb_users_blockhouse_res_groups_rel'

    group_id = fields.Many2one(comodel_name='res.groups', string='Nhóm người dùng',
                               # domain=lambda self: [
                               #     ('category_id', '=',
                               #      self.env['ir.module.category'].search([('name', 'ilike', 'Quản lý cư dân')]).id)]
                               )
    selected_group = fields.Char(related='group_id.name')
    user_id = fields.Many2one(comodel_name='res.users', string="Tài khoản")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string='Dự án')
    building_id = fields.Many2one(comodel_name='tb_building', string='Tòa nhà',
                                  domain="[('blockhouse_id', '=', blockhouse_id)]")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string='Căn hộ',
                                        domain="[('building_id', '=', building_id)]")
    owner = fields.Boolean(string='Chủ sở hữu', default=False)
    relationship_type = fields.Selection(string='Quan hệ với chủ hộ', selection=RELATIONSHIP_TYPES,
                                         default=RELATIONSHIP_TYPES[0][0])
    user_group_code = fields.Selection(string='Mã nhóm quyền', selection=USER_GROUP_CODE,
                                       default=USER_GROUP_CODE[0][0])

    @api.onchange('relationship_type')
    def _on_change_relationship_type(self):
        if self.relationship_type == RELATIONSHIP_TYPES[1][0]:
            self.owner = True
        else:
            self.owner = False

    @api.onchange('blockhouse_id')
    def _on_change_blockhouse_id(self):
        self.building_id = None
        self.building_house_id = None

    @api.onchange('building_id')
    def _on_change_building_id(self):
        self.building_house_id = None

    @api.onchange('group_id')
    def _on_change_group_id(self):
        if self.group_id.name:
            if USER_GROUP_CODE[1][0] in self.group_id.name:
                self.user_group_code = USER_GROUP_CODE[1][0]
            elif USER_GROUP_CODE[2][0] in self.group_id.name:
                self.user_group_code = USER_GROUP_CODE[2][0]
            elif USER_GROUP_CODE[3][0] in self.group_id.name:
                self.user_group_code = USER_GROUP_CODE[3][0]
        self.blockhouse_id = None
        self.building_id = None
        self.building_house_id = None

    @api.model
    def create(self, value):
        uid = value["user_id"]
        gid = value["group_id"]
        blockhouse_id = value["blockhouse_id"]
        building_id = value["building_id"]
        building_house_id = value["building_house_id"]
        owner = value['owner']
        if not building_house_id:
            self.env.cr.execute("""SELECT count(*) FROM tb_users_blockhouse_res_groups_rel WHERE user_id=%s AND 
                                   blockhouse_id=%s AND building_id=%s AND group_id=%s""",
                                (uid, blockhouse_id, building_id, gid))
            total = self.env.cr.fetchone()[0]
            if total > 0:
                raise ValidationError("Bạn đã là ban quản trị/ ban quản lý của tòa nhà này")
            else:
                self._insert_record_res_groups_users_rel(uid, gid)
        else:
            self.env.cr.execute("""SELECT count(*) FROM tb_users_blockhouse_res_groups_rel
                                                                       WHERE user_id=%s AND building_house_id=%s AND group_id=%s""",
                                (uid, building_house_id, gid))
            total = self.env.cr.fetchone()[0]
            self.env.cr.execute("""SELECT count(*) FROM tb_users_blockhouse_res_groups_rel
                                                                       WHERE building_house_id=%s AND group_id=%s AND owner=TRUE""",
                                (building_house_id, gid))
            count_owner = self.env.cr.fetchone()[0]
            if total > 0:
                raise ValidationError("Bạn đã là cư dân của căn hộ này")
            if owner is True and count_owner > 0:
                raise ValidationError("Bạn không thể là chủ sở hữu của căn hộ do căn hộ này đã có chủ sở hữu.")
            else:
                self._insert_record_res_groups_users_rel(uid, gid)

        self.env['ir.actions.actions'].clear_caches()
        return super(tb_users_blockhouse_res_groups_rel, self).create(value)

    def _insert_record_res_groups_users_rel(self, uid, gid, *args, **kwargs):
        self.env.cr.execute("""SELECT count(*) FROM res_groups_users_rel
                                               WHERE uid=%s AND gid=%s""",
                            (uid, gid))
        total = self.env.cr.fetchone()[0]
        if total == 0:
            self.env.cr.execute("""INSERT INTO res_groups_users_rel(uid, gid) VALUES(%s, %s)""", (uid, gid))

    def unlink(self):
        for record in self:
            query = """DELETE FROM res_groups_users_rel WHERE uid = %s and gid = %s"""
            self.env.cr.execute(query, (record.user_id.id, record.group_id.id))
        self.env['ir.actions.actions'].clear_caches()
        return super(tb_users_blockhouse_res_groups_rel, self).unlink()
