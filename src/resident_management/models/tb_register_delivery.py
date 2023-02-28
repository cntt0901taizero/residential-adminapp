from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
from odoo.addons.resident_management.enum import STATUS_TYPES, VEHICLE_TYPES

str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]

SHIPPING_METHOD = [
    ('chuyen_ra', 'Chuyển đồ ra'),
    ('chuyen_vao', 'Chuyển đồ vào')
]

THROUGH_METHOD = [
    ('chuyen_qua_sanh', 'Chuyển qua sảnh'),
    ('chuyen_qua_ham', 'Chuyển qua hầm'),
]


class tb_register_delivery(models.Model):
    _name = 'tb_register_delivery'
    _description = 'Đăng ký chuyển đồ'

    name = fields.Char(string='Người đăng ký', copy=False)
    shipping_method = fields.Selection(string='Phương thức chuyển đồ', selection=SHIPPING_METHOD,
                                       default=SHIPPING_METHOD[0][0])
    through_method = fields.Selection(string='Vận chuyển qua', selection=THROUGH_METHOD,
                                      default=THROUGH_METHOD[0][0])
    time_start = fields.Datetime(string='Thời gian bắt đầu', copy=False)
    time_end = fields.Datetime(string='Thời gian kết thúc', copy=False)
    freight_detail = fields.Text(string='Chi tiết vận chuyển', copy=False)
    use_freight_elevator = fields.Boolean(string='Sử dụng thang hàng', default=True, copy=False)
    status = fields.Selection(string='Trạng thái', selection=STATUS_TYPES, default=STATUS_TYPES[0][0])

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    domain=lambda self: self._domain_blockhouse_id(),
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà",
                                  domain="[('blockhouse_id', '!=', None), ('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ",
                                        domain="[('building_id', '!=', None), ('building_id', '=', building_id)]",
                                        ondelete="cascade")
    user_id = fields.Many2one(comodel_name='res.users', string="Chủ sở hữu",
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

            user_ids_1 = self.env['tb_users_blockhouse_res_groups_rel'].sudo()\
                .search([('building_id', 'in', list(set(bqt_bd_id + bql_bd_id)))])
            user_ids_2 = self.env['tb_users_blockhouse_res_groups_rel'].sudo()\
                .search([('blockhouse_id', 'in', list(set(bqt_bh_id + bql_bh_id)))])

            return ["&", ("active", "=", True), ("id", "in", list(set(user_ids_1 + user_ids_2)))]
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
        res = super(tb_register_delivery, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
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
        res = super(tb_register_delivery, self).search_read(domain, fields, offset, limit, order)
        return res

    def open_edit_form(self):
        can_do = self.check_access_rights('write', raise_exception=False)
        if not can_do:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin!')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sửa: ' + self.name,
            'res_model': 'tb_register_delivery',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('apartment_service_support.view_tb_register_delivery_form').id,
            'context': {'form_view_initial_mode': 'edit'},
            'target': 'current',
        }

    def open_edit_approve_form(self):
        can_do = self.check_access_rights('write', raise_exception=False)
        if not can_do:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin!')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sửa: ' + self.name,
            'res_model': 'tb_register_delivery',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('apartment_service_support.view_tb_register_delivery_approve_form').id,
            'context': {'form_view_initial_mode': 'edit'},
            'target': 'current',
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




