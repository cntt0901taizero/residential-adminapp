from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.resident_management.enum import STATUS_TYPES, VEHICLE_TYPES, USER_GROUP_CODE

str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_complain(models.Model):
    _name = 'tb_complain'
    _description = 'Phương tiện'

    name = fields.Char(string='Tiêu đề', copy=False)
    content = fields.Html(string='Nội dung')
    image = fields.Image(string="Ảnh")
    file = fields.Binary(string='Tài liệu', attachment=True, help='Chọn tài liệu tải lên')
    status_description = fields.Html(string='Phản hồi từ quản lý')
    status = fields.Selection(string='Trạng thái', selection=STATUS_TYPES, default=STATUS_TYPES[0][0])

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    domain=lambda self: self._domain_blockhouse_id(),
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà",
                                  domain="[('is_active', '=', True), ('blockhouse_id', '!=', None), ('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ",
                                        domain="[('is_active', '=', True), ('building_id', '!=', None), ('building_id', '=', building_id)]",
                                        ondelete="cascade")
    user_id = fields.Many2one(comodel_name='res.users', string="Người khiếu nại",
                              domain=lambda self: self._domain_user_id(),
                              ondelete="cascade")

    def set_status_active(self):
        for item in self:
            item.status = 'ACTIVE'

    def set_status_reject(self):
        for item in self:
            item.status = 'REJECT'

    @api.model
    def _domain_user_id(self):
        user = request.env.user
        if user and user.id != 1 and user.id != 2:
            user_ids = (self.env['tb_users_blockhouse_res_groups_rel'].sudo()
                        .search([('building_id', 'in', self.building_house_id)])).user_id.ids
            return ["&", ("active", "=", True), ("id", "in", user_ids)]
        else:
            return [("active", "=", True)]

    @api.model
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
            return ["&", ("is_active", "=", True), ("id", "in", list(set(bqt_bh_id + bql_bh_id)))]
        else:
            return [("is_active", "=", True)]

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
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
            domain.append(('building_id', 'in', list(set(bqt_bd_id + bql_bd_id))))
            domain.append(('blockhouse_id', 'in', list(set(bqt_bh_id + bql_bh_id))))
        res = super(tb_complain, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                 orderby=orderby, lazy=lazy)
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10, order=None):
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
            domain.append(('building_id', 'in', list(set(bqt_bd_id + bql_bd_id))))
            domain.append(('blockhouse_id', 'in', list(set(bqt_bh_id + bql_bh_id))))
        res = super(tb_complain, self).search_read(domain, fields, offset, limit, order)
        return res

    def open_edit_form(self):
        per_name = 'perm_write_complain'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sửa phương tiện ' + self.name,
                'res_model': 'tb_complain',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('apartment_service_support.view_tb_complain_form').id,
                'context': {'form_view_initial_mode': 'edit'},
                'target': 'current',
            }
        raise ValidationError(error_messenger)

    def open_edit_approve_form(self):
        per_name = 'perm_approve_complain'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sửa phương tiện ' + self.name,
                'res_model': 'tb_complain',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('apartment_service_support.view_tb_complain_approve_form').id,
                'context': {'form_view_initial_mode': 'edit'},
                'target': 'current',
            }
        raise ValidationError(error_messenger)

    def confirm_delete(self):
        per_name = 'perm_delete_complain'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
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
        raise ValidationError(error_messenger)

    def del_record(self):
        for record in self:
            record.unlink()
            pass




