from odoo import models, fields
from odoo.http import request
from odoo import models, fields, api
import random

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_paybill_config(models.Model):
    _name = 'tb_paybill_config'
    _description = 'Cấu hình thanh toán'

    description = fields.Char(string='Ghi chú', copy=False)
    price = fields.Char(string='giá phí thanh toán', copy=False)
    is_active = fields.Boolean(string='Có hiệu lực', default=True)
    feekind_id = fields.Many2one(comodel_name='tb_feekind', string="Loại phí", ondelete="cascade")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ",
                                        domain="[('building_id', '=', building_id)]",
                                        ondelete="cascade")

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
            domain.append(('blockhouse_id', 'in', bh_ids))
        res = super(tb_paybill_config, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                        orderby=orderby, lazy=lazy)
        return res

