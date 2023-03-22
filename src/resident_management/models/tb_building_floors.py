from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from odoo.http import request
import random

from odoo.addons.resident_management.enum import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]

FLOORS_TYPES = [
    ('none', '--'),
    ('tang_ham', 'Tầng hầm'),
    ('ki_thuat', 'Kĩ thuật'),
    ('thuong_mai', 'Thương mại'),
    ('van_phong', 'Văn phòng'),
    ('can_ho', 'Căn hộ'),
]


class tb_building_floors(models.Model):
    _name = 'tb_building_floors'
    _description = 'Tầng sàn'

    row_number = fields.Integer(string='STT', compute='_compute_row_number', store=False)
    name = fields.Char(string='Tên tầng sàn', size=200, copy=False, readonly=True)
    name_display = fields.Char(string='Tên hiển thị', size=200, required=True, copy=False)
    code = fields.Char(string='Mã', size=50, copy=False, readonly=True)
    sort = fields.Integer(string='Thứ tự', copy=False)
    total_house = fields.Integer(string='Tổng căn hộ', copy=False)
    floors_type = fields.Selection(string='Loại tầng', selection=FLOORS_TYPES, default=FLOORS_TYPES[0][0])
    is_active = fields.Boolean(string='Có hiệu lực', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")

    building_house_ids = fields.One2many(comodel_name='tb_building_house', string="Căn hộ",
                                         inverse_name='building_floors_id')

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên tầng không được trùng lặp'),
        ('code', 'unique(code)', 'Mã tầng không được trùng lặp'),
        ('unique_building_floors', 'unique(name_display, building_id, blockhouse_id)', 'Tên tầng bị trùng lặp.')
    ]

    @api.depends('create_date')
    def _compute_row_number(self):
        index_row = 0
        for record in self:
            index_row += 1
            record.row_number = index_row

    def set_status_active(self):
        self.is_active = True

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
        res = super(tb_building_floors, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
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
        res = super(tb_building_floors, self).search_read(domain, fields, offset, limit, order)
        return res

    @api.model
    def create(self, vals):
        per_name = 'perm_create_floor'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            today = date.today()
            d = today.strftime('%d%m%y')
            code = 'BDF' + str(d) + str(random.randint(1000, 9999))
            vals["code"] = code
            vals["name"] = code + " - " + str(vals["name_display"]).strip()
            res = super(tb_building_floors, self).create(vals)
            self.clear_caches()
            return res
        raise ValidationError(error_messenger)

    def write(self, vals):
        per_name = 'perm_write_floor'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            if self.code and vals.get("name_display"):
                vals["name"] = self.code + " - " + vals["name_display"]
            res = super(tb_building_floors, self).write(vals)
            self.clear_caches()
            return res
        raise ValidationError(error_messenger)

    def create_building_house(self):
        per_name = 'perm_create_apartment'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Tạo mới Căn hộ',
                'res_model': 'tb_building_house',
                'target': 'new',
                'view_id': self.env.ref('apartment_project.view_tb_building_house_form').id,
                'view_mode': 'form',
                'context': {
                    'default_building_floors_id': self.id,
                    'default_building_id': self.building_id.id,
                    'default_blockhouse_id': self.blockhouse_id.id,
                },
            }
        raise ValidationError(error_messenger)

    @api.model
    def default_get(self, data):
        res = super(tb_building_floors, self).default_get(data)
        return res

    def open_edit_form(self):
        per_name = 'perm_write_floor'
        error_messenger = 'Bạn chưa được phân quyền này!'
        can_do = self.check_permission(per_name, raise_exception=False)
        if can_do:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sửa tầng ' + self.name,
                'res_model': 'tb_building_floors',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('apartment_project.view_tb_building_floors_form').id,
                'context': {'form_view_initial_mode': 'edit'},
                'target': 'current',
            }
        raise ValidationError(error_messenger)

    def confirm_delete(self):
        per_name = 'perm_delete_floor'
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

