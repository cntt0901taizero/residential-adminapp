from odoo import models, fields, api
from datetime import date
from odoo.http import request
from odoo.exceptions import ValidationError
import random

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]

BUILDING_LEVEL = [
    ('none', '--'),
    ('a', 'Hạng A'),
    ('b', 'Hạng B'),
    ('c', 'Hạng C'),
]

class tb_building(models.Model):
    _name = 'tb_building'
    _description = 'Toà nhà'

    row_number = fields.Integer(string='STT', compute='_compute_row_number', store=False)
    name = fields.Char(string='Tên toà nhà', size=200, required=True, copy=False)
    code = fields.Char(string='Mã', size=50, copy=False, readonly=True)
    founding_date = fields.Date(string='Ngày thành lập', copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    address = fields.Char(string='Địa chỉ', size=500, copy=False)
    website = fields.Char(string='Website', size=200, copy=False)
    phone = fields.Char(string='Điện thoại', size=50, copy=False)
    location_link = fields.Char(string='Link vị trí', size=500, copy=False)
    # floors_above_ground_number = fields.Integer(string='Số tầng nổi', copy=False)
    # floors_below_ground_number = fields.Integer(string='Số tầng hầm', copy=False)
    building_level = fields.Selection(string='Hạng tòa nhà', selection=BUILDING_LEVEL, default=BUILDING_LEVEL[0][0])
    is_active = fields.Boolean(string='Có hiệu lực', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án", ondelete="cascade")
    apartment_utilities_ids = fields.Many2many('tb_apartment_utilities', string="Tiện ích chung cư",
                                               domain="[('blockhouse_id', '=', blockhouse_id)]", ondelete="cascade")

    building_floors_ids = fields.One2many(comodel_name='tb_building_floors', inverse_name='building_id', string="Tầng sàn")
    building_house_ids = fields.One2many(comodel_name='tb_building_house', inverse_name='building_id', string="Căn hộ")

    _sql_constraints = [
        ('code', 'unique(code)', 'Mã tòa nhà không được trùng lặp')
    ]

    # def open_parent_record(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'parent.model',
    #         'res_id': self.parent_id.id,
    #         'view_mode': 'form',
    #         'target': 'current',
    #     }

    @api.depends('create_date')
    def _compute_row_number(self):
        for record in self:
            record.row_number = self.search([], order='create_date').ids.index(record.id) + 1

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
            domain.append(('id', 'in', list(set(bqt_bd_id + bql_bd_id))))
        res = super(tb_building, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
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
            domain.append(('id', 'in', list(set(bqt_bd_id + bql_bd_id))))
        res = super(tb_building, self).search_read(domain, fields, offset, limit, order)
        return res

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     res = self._search(args, offset=offset, limit=limit, order=order, count=count)
    #     return res if count else self.browse(res)

    @api.model
    def create(self, vals):
        today = date.today()
        d = today.strftime('%d%m%y')
        vals["code"] = 'BD' + str(d) + str(random.randint(1000, 9999))
        return super(tb_building, self).create(vals)

    def create_building_floors(self):
        max_number: int = 0
        if self.building_floors_ids.ids:
            max_number = max(self.building_floors_ids.ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới Tầng sàn',
            'res_model': 'tb_building_floors',
            'target': 'new',
            'view_id': self.env.ref('apartment_project.view_tb_building_floors_form').id,
            'view_mode': 'form',
            'context': {
                'default_building_id': self.id,
                'default_blockhouse_id': self.blockhouse_id.id,
                'default_sort': max_number + 1,
            },
        }

    def create_building_house(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới Căn hộ',
            'res_model': 'tb_building_house',
            'target': 'new',
            'view_id': self.env.ref('apartment_project.view_tb_building_house_form').id,
            'view_mode': 'form',
            'context': {
                'default_building_id': self.id,
                'default_blockhouse_id': self.blockhouse_id.id,
            },
        }

    # def create_building(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Tạo mới khu/tòa nhà',
    #         'res_model': 'tb_building',
    #         'target': 'new',
    #         'view_id': self.env.ref('apartment_project.view_tb_building_form').id,
    #         'view_mode': 'form',
    #         'context': {
    #             'default_blockhouse_id': self.blockhouse_id.id,
    #         },
    #     }

    def open_edit_form(self):
        can_do = self.check_access_rights('write', raise_exception=False)
        if not can_do:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin!')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sửa khu / tòa nhà ' + self.name,
            'res_model': 'tb_building',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('apartment_project.view_tb_building_form').id,
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






