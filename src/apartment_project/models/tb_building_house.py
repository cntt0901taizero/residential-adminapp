from odoo import models, fields, api
from datetime import date
import random
from odoo.http import request
from odoo.exceptions import ValidationError

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]

HOUSE_TYPES = [
    ('none', '--'),
    ('studio', 'Studio'),
    ('officetel', 'Officetel'),
    ('shophouse', 'Shophouse'),
    ('dualkey', 'Dualkey'),
    ('penhouse', 'Penhouse'),
    ('duplex', 'Duplex'),
    ('skyvilla', 'Skyvilla'),
    ('normal', 'Normal'),
]


class tb_building_house(models.Model):
    _name = 'tb_building_house'
    _description = 'Căn hộ'

    name = fields.Char(string='Số nhà', size=50, copy=False)
    code = fields.Char(string='Mã', size=50, copy=False, readonly=True)
    address = fields.Char(string='Địa chỉ', size=200, copy=False)
    house_type = fields.Selection(string='Loại hình căn hộ', selection=HOUSE_TYPES, default=HOUSE_TYPES[0][0])

    area_apartment = fields.Float(string='Diên tích căn hộ (m²)', copy=False)
    bedroom_number = fields.Integer(string='Số phòng ngủ', copy=False)
    bathroom_number = fields.Integer(string='Số phòng tắm', copy=False)
    balcony_number = fields.Integer(string='Số ban công', copy=False)
    fee_base = fields.Float(string='Phí cơ bản (vnđ)', copy=False)
    detailed_description = fields.Text(string='Mô tả chi tiết', copy=False)

    is_active = fields.Boolean(string='Trạng thái', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")
    building_floors_id = fields.Many2one(comodel_name='tb_building_floors', string="Tầng sàn",
                                         domain="[('building_id', '=', building_id)]",
                                         ondelete="cascade")

    _sql_constraints = [
        ('code', 'unique(code)', 'Mã căn hộ không được trùng lặp')
    ]

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
        res = super(tb_building_house, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
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
        res = super(tb_building_house, self).search_read(domain, fields, offset, limit, order)
        return res

    @api.model
    def create(self, vals):
        today = date.today()
        d = today.strftime('%d%m%y')
        vals["code"] = 'BDH' + str(d) + str(random.randint(1000, 9999))
        return super(tb_building_house, self).create(vals)

    @api.model
    def default_get(self, data):
        res = super(tb_building_house, self).default_get(data)
        return res

    def open_edit_form(self):
        can_do = self.check_access_rights('write', raise_exception=False)
        if not can_do:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin!')
        form_id = self.env.ref('view_tb_building_house_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sửa căn hộ / biệt thự ' + self.name,
            'res_model': 'tb_building_house',
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




