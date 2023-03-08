from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request

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

str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_users_blockhouse_res_groups_rel(models.Model):
    _name = 'tb_users_blockhouse_res_groups_rel'

    group_id = fields.Many2one(comodel_name='res.groups', string='Nhóm người dùng',
                               # domain=lambda self: [
                               #     ('category_id', '=',
                               #      self.env['ir.module.category'].search([('name', 'ilike', 'Quản lý cư dân')]).id)]
                               )
    selected_group = fields.Char(related='group_id.name')
    user_id = fields.Many2one(comodel_name='res.users', string="Tài khoản", ondelete="cascade")
    job_title = fields.Char(string='Chức danh')
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string='Dự án', ondelete="cascade",
                                    domain=lambda self: self._domain_blockhouse_id(), )

    building_id = fields.Many2one(comodel_name='tb_building', string='Tòa nhà',
                                  domain="[('blockhouse_id', '=', blockhouse_id)]", ondelete="cascade")
    building_floors_id = fields.Many2one(comodel_name='tb_building_floors', string='Tầng',
                                         domain="[('building_id', '=', building_id)]", ondelete="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string='Căn hộ',
                                        domain="[('building_floors_id', '=', building_floors_id)]",
                                        ondelete="cascade")
    owner = fields.Boolean(string='Chủ sở hữu', default=False)

    relationship_type = fields.Selection(string='Quan hệ với chủ hộ', selection=RELATIONSHIP_TYPES,
                                         default=RELATIONSHIP_TYPES[0][0])
    user_group_code = fields.Selection(string='Mã nhóm quyền', selection=USER_GROUP_CODE,
                                       default=USER_GROUP_CODE[0][0])

    def _domain_blockhouse_id(self):
        user = request.env.user
        bqt_bh_id = []  # ban quan tri - blockhouse - id
        bqt_bd_id = []  # ban quan tri - building - id
        bql_bh_id = []  # ban quan ly - blockhouse - id
        bql_bd_id = []  # ban quan ly - building - id
        if user and user.id != 1 and user.id != 2:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and str_bqt in item.user_group_code:
                    bqt_bh_id.append(int(item.blockhouse_id.id))
                    bqt_bd_id.append(int(item.building_id.id))
                if item.group_id.name and str_bql in item.user_group_code:
                    bql_bh_id.append(int(item.blockhouse_id.id))
                    bql_bd_id.append(int(item.building_id.id))
            return [("is_active", "=", True), ("id", "in", list(set(bqt_bh_id + bql_bh_id)))]
        else:
            return [("is_active", "=", True)]

    @api.onchange('relationship_type')
    def _on_change_relationship_type(self):
        if self.relationship_type == RELATIONSHIP_TYPES[1][0]:
            self.owner = True
        else:
            self.owner = False

    @api.onchange('blockhouse_id')
    def _on_change_blockhouse_id(self):
        self.building_id = None
        self.building_floors_id = None
        self.building_house_id = None

    @api.onchange('building_id')
    def _on_change_building_id(self):
        self.building_floors_id = None
        self.building_house_id = None

    @api.onchange('building_floors_id')
    def _on_change_building_floors_id(self):
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
        # self.blockhouse_id = None
        # self.building_id = None
        # self.building_house_id = None
        # self.building_floors_id = None

    @api.model
    def create(self, value):
        uid = None
        gid = None
        blockhouse_id = None
        building_id = None
        building_house_id = None
        if 'user_id' in value:
            uid = value["user_id"]
        if 'group_id' in value:
            gid = value["group_id"]
        else:
            gid = self.env['res.groups'].search([('name', 'like', '%[CD]%')]).id
        if 'blockhouse_id' in value:
            blockhouse_id = value["blockhouse_id"]
        if 'building_id' in value:
            building_id = value["building_id"]
        if 'owner' in value:
            owner = value['owner']
        if "building_house_id" not in value:
            self.env.cr.execute("""SELECT count(*) FROM tb_users_blockhouse_res_groups_rel WHERE user_id=%s AND 
                                   blockhouse_id=%s AND building_id=%s AND group_id=%s""",
                                (uid, blockhouse_id, building_id, gid))
            total = self.env.cr.fetchone()[0]
            if total > 0:
                raise ValidationError("Bạn đã là ban quản trị/ ban quản lý của tòa nhà này")
            else:
                self._insert_record_res_groups_users_rel(uid, gid)
        else:
            building_house_id = value["building_house_id"]
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
        res = super(tb_users_blockhouse_res_groups_rel, self).create(value)
        # self.env['bus.bus']._sendone((self._cr.dbname, 'tb_users_blockhouse_res_groups_rel', self.env.uid),
        #                              {'type': 'create', 'id': res.id},
        #                              {'type': 'ir.actions.act_window_close', 'context': {'form_view_ref': False}})
        return res
        # return super(tb_users_blockhouse_res_groups_rel, self).create(value)
        # return self._notification(type_message="success", title="Thông báo", message="Đã thành công")

    def _insert_record_res_groups_users_rel(self, uid, gid, *args, **kwargs):
        self.env.cr.execute("""SELECT count(*) FROM res_groups_users_rel WHERE uid=%s AND gid=%s""", (uid, gid))
        total = self.env.cr.fetchone()[0]
        if total == 0:
            self.env.cr.execute("""INSERT INTO res_groups_users_rel(uid, gid) VALUES(%s, %s)""", (uid, gid))

    def unlink(self):
        for record in self:
            query = """DELETE FROM res_groups_users_rel WHERE uid = %s and gid = %s"""
            self.env.cr.execute(query, (record.user_id.id, record.group_id.id))
        self.env['ir.actions.actions'].clear_caches()
        return super(tb_users_blockhouse_res_groups_rel, self).unlink()

    def open_edit_form(self):
        can_do = self.check_access_rights('write', raise_exception=False)
        if not can_do:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin!')

        view_id = ''
        name = ''
        context = {}
        if self.user_id.user_type != 'RESIDENT':
            name = 'Phân quyền quản lý quản trị'
            view_id = self.env.ref('resident_management.view_tb_users_blockhouse_res_groups_rel_form').id
        else:
            name = 'Phân quyền căn hộ cư dân'
            context['default_group_id'] = self.env['res.groups'].search([('name', 'like', '%[CD]%')]).id
            view_id = self.env.ref('resident_management.view_tb_users_blockhouse_res_groups_rel_form_resident').id
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': 'tb_users_blockhouse_res_groups_rel',
            'res_id': self.id,
            # 'view_id': view_id,
            'views': [(view_id, 'form')],
            'view_type': 'form',
            'view_mode': 'form',
            'context': context,
            'target': 'new',
            # 'nodestroy': True,
            # 'flags': {
            #     'action_buttons': True,
            # },
        }

    def confirm_delete(self):
        candelete = self.check_access_rights('unlink', raise_exception=False)
        if not candelete:
            raise ValidationError('Bạn không có quyền xóa bản ghi này!')
        message = """Bạn có chắc muốn xóa bản ghi này?"""
        value = self.env['dialog.box.confirm'].sudo().create({'message': message})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Xóa bản ghi',
            'res_model': 'dialog.box.confirm',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': value.id
        }

    def del_record(self):
        for record in self:
            record.unlink()
            pass

    # def close_dialog(self):
    #     return {
    #         'type': 'ir.actions.act_window_close',
    #         'context': {'form_view_ref': False},
    #     }
    #
    # def _notification(self, type_message="info", title="", message="", action_form=None, model=None):
    #     action = self.env.ref(action_form)
    #     if action_form:
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': _(title),
    #                 'message': _(message),
    #                 'type': type_message,
    #                 'sticky': False,
    #                 'links': [{
    #                     'label': 'string',
    #                     'url': f'#action={action.id}&id={self.id}&model={model}',
    #                 }],
    #                 'next': {
    #                     'type': 'ir.actions.act_window_close',
    #                     'context': {'form_view_ref': False},
    #                 },
    #             }
    #         }
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': _(title),
    #             'message': _(message),
    #             'type': type_message,
    #             'sticky': False,
    #             'next': {
    #                 'type': 'ir.actions.act_window_close',
    #                 'context': {'form_view_ref': False},
    #             },
    #         }
    #     }

