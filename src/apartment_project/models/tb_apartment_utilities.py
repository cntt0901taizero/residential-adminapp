from odoo import models, fields, api
from odoo.http import request
import random

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]

DAYS_LIST = [
    ('2', 'Thứ 2'),
    ('3', 'Thứ 3'),
    ('4', 'Thứ 4'),
    ('5', 'Thứ 5'),
    ('6', 'Thứ 6'),
    ('7', 'Thứ 7'),
    ('cn', 'Chủ nhật'),
]

class tb_apartment_utilities(models.Model):
    _name = 'tb_apartment_utilities'
    _description = 'Tiện ích chung cư'

    name = fields.Char(string='Tên', required=True, copy=False)
    image = fields.Image(string='Ảnh', copy=False)
    description = fields.Text(string='Mô tả', copy=False, help='')
    detail_description = fields.Html(string='Mô tả chi tiết', copy=False, help='')
    # active_days = fields.Selection(string='Ngày hoạt động', selection=DAYS_LIST)
    # active_time = fields.Char(string='Giờ hoạt động', size=50,  help='9h30p - 21h')
    is_active = fields.Boolean(string='Trạng thái', default=True)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    ondelet="cascade")

    def set_status_active(self):
        self.is_active = True

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        user = request.env.user
        bqt_bh_id = []  # ban quan tri - blockhouse - id
        bqt_bd_id = []  # ban quan tri - building - id
        bql_bh_id = []  # ban quan ly - blockhouse - id
        bql_bd_id = []  # ban quan ly - building - id
        if user.id != 1 and user.id != 2:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and str_bqt in item.user_group_code:
                    bqt_bh_id.append(int(item.blockhouse_id.id))
                    bqt_bd_id.append(int(item.building_id.id))
                if item.group_id.name and str_bql in item.user_group_code:
                    bql_bh_id.append(int(item.blockhouse_id.id))
                    bql_bd_id.append(int(item.building_id.id))
            domain.append(('id', 'in', list(set(bqt_bh_id + bql_bh_id))))
        res = super(tb_apartment_utilities, self).read_group(domain, fields, groupby, offset=offset,
                                                             limit=limit, orderby=orderby, lazy=lazy)
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=10, order=None):
        user = request.env.user
        bqt_bh_id = []  # ban quan tri - blockhouse - id
        bqt_bd_id = []  # ban quan tri - building - id
        bql_bh_id = []  # ban quan ly - blockhouse - id
        bql_bd_id = []  # ban quan ly - building - id
        if user.id != 1 and user.id != 2:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and str_bqt in item.user_group_code:
                    bqt_bh_id.append(int(item.blockhouse_id.id))
                    bqt_bd_id.append(int(item.building_id.id))
                if item.group_id.name and str_bql in item.user_group_code:
                    bql_bh_id.append(int(item.blockhouse_id.id))
                    bql_bd_id.append(int(item.building_id.id))
            domain.append(('id', 'in', list(set(bqt_bh_id + bql_bh_id))))
        res = super(tb_apartment_utilities, self).search_read(domain, fields, offset, limit, order)
        return res






