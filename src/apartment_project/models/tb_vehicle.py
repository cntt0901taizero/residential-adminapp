from odoo import models, fields, api
from odoo.http import request

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]

VEHICLE_TYPES = [
    ('bicycle', 'Xe đạp'),
    ('motorbike', 'Xe máy'),
    ('car', 'Ô tô'),
]

class tb_vehicle(models.Model):
    _name = 'tb_vehicle'
    _description = 'Phương tiện'

    name = fields.Char(string='Biển số xe', copy=False)  # license_plates
    image = fields.Image(string='Ảnh', copy=False)
    vehicle_type = fields.Selection(string='Loại xe', selection=VEHICLE_TYPES, default=VEHICLE_TYPES[0][0])
    note = fields.Text(string='Ghi chú', copy=False, help='Loại xe - màu xe - ...')
    is_active = fields.Boolean(string='Trạng thái', default=True)
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    domain=lambda self: self._domain_blockhouse_id(),
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ",
                                        domain="[('building_id', '=', building_id)]",
                                        ondelete="cascade")
    user_id = fields.Many2one(comodel_name='res.users', string="Chủ sở hữu",
                              domain=lambda self: self._domain_user_id(),
                              # domain="[('users_blockhouse_groups_rel_ids.building_id', '=', building_id)]",
                              ondelete="cascade")

    def set_status_active(self):
        self.is_active = True

    def _domain_user_id(self):
        user = request.env.user
        bqt_bh_id = []  # ban quan tri - blockhouse - id
        bqt_bd_id = []  # ban quan tri - building - id
        bql_bh_id = []  # ban quan ly - blockhouse - id
        bql_bd_id = []  # ban quan ly - building - id
        users_id = []
        if user and user.id != 1 and user.id != 2:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and str_bqt in item.user_group_code:
                    bqt_bh_id.append(int(item.blockhouse_id.id))
                    bqt_bd_id.append(int(item.building_id.id))
                if item.group_id.name and str_bql in item.user_group_code:
                    bql_bh_id.append(int(item.blockhouse_id.id))
                    bql_bd_id.append(int(item.building_id.id))

            users = self.env['tb_users_blockhouse_res_groups_rel'].sudo()\
                .search([('building_id', 'in', list(set(bqt_bd_id + bql_bd_id)))])

            for item in users:
                users_id.append(item.id)
            return [("active", "=", True), ("id", "in", users_id)]
        else:
            return [("active", "=", True)]

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

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        user = request.env.user
        bqt_bh_id = []  # ban quan tri - blockhouse - id
        bqt_bd_id = []  # ban quan tri - building - id
        bql_bh_id = []  # ban quan ly - blockhouse - id
        bql_bd_id = []  # ban quan ly - building - id
        if user and  user.id != 1 and user.id != 2:
            for item in user.tb_users_blockhouse_res_groups_rel_ids:
                if item.group_id.name and str_bqt in item.user_group_code:
                    bqt_bh_id.append(int(item.blockhouse_id.id))
                    bqt_bd_id.append(int(item.building_id.id))
                if item.group_id.name and str_bql in item.user_group_code:
                    bql_bh_id.append(int(item.blockhouse_id.id))
                    bql_bd_id.append(int(item.building_id.id))
            domain.append(('building_id', 'in', list(set(bqt_bd_id + bql_bd_id))))
            domain.append(('blockhouse_id', 'in', list(set(bqt_bh_id + bql_bh_id))))
        res = super(tb_vehicle, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
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
        res = super(tb_vehicle, self).search_read(domain, fields, offset, limit, order)
        return res




