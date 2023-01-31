from odoo import models, fields, api
from odoo.http import request
from datetime import date
from odoo.exceptions import ValidationError
import random

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_blockhouse(models.Model):
    _name = 'tb_blockhouse'
    _description = 'Dự án'

    name = fields.Char(string='Tên dự án', size=200, required=True, copy=False)
    code = fields.Char(string='Mã', size=50, copy=False, readonly=True)
    address = fields.Char(string='Địa chỉ', size=500, copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    website = fields.Char(string='Website', size=200, copy=False)
    phone = fields.Char(string='Điện thoại', size=50, copy=False)
    location_link = fields.Char(string='Link vị trí', size=500, copy=False)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    building_ids = fields.One2many(comodel_name='tb_building', inverse_name='blockhouse_id', string="Tòa nhà")

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên dự án không được trùng lặp'),
        ('code', 'unique(code)', 'Mã dự án không được trùng lặp')
    ]

    def set_status_active(self):
        self.is_active = True

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        user = request.env.user
        if user and user.id != 1 and user.id != 2:
            bh_ids = []
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and (str_bql in item.user_group_code or str_bqt in item.user_group_code):
                    bh_ids.append(int(item.blockhouse_id.id))
            domain.append(('id', 'in', bh_ids))
        res = super(tb_blockhouse, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10, order=None):
        user = request.env.user
        if user and user.id != 1 and user.id != 2:
            bh_ids = []
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and (str_bql in item.user_group_code or str_bqt in item.user_group_code):
                    bh_ids.append(int(item.blockhouse_id.id))
            domain.append(('id', 'in', bh_ids))

        res = super(tb_blockhouse, self).search_read(domain, fields, offset, limit, order)
        return res

    @api.model
    def create(self, vals):
        today = date.today()
        d = today.strftime('%d%m%y')
        vals["code"] = 'BH' + str(d) + str(random.randint(1000, 9999))
        return super(tb_blockhouse, self).create(vals)

    def create_building(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới khu / tòa nhà',
            'res_model': 'tb_building',
            'target': 'new',
            'view_id': self.env.ref('apartment_project.view_tb_building_form').id,
            'view_mode': 'form',
            'context': {
                'default_blockhouse_id': self.id,
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
                'default_blockhouse_id': self.id,
            },
        }

    def create_apartment_utilities(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo mới tiện ích',
            'res_model': 'tb_apartment_utilities',
            'target': 'new',
            'view_id': self.env.ref('apartment_project.view_tb_apartment_utilities_form').id,
            'view_mode': 'form',
            'context': {
                'default_blockhouse_id': self.id,
            },
        }

    def open_edit_form(self):
        can_do = self.check_access_rights('write', raise_exception=False)
        if not can_do:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin!')
        form_id = self.env.ref('view_tb_blockhouse_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sửa dự án ' + self.name,
            'res_model': 'tb_blockhouse',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id,
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


