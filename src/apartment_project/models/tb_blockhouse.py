from odoo import models, fields, api
from odoo.http import request
from datetime import date
import random


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

    def set_status_active(self):
        self.is_active = True

    @api.model
    def search_read(self, domain=[], fields=None, offset=0, limit=10, order=None):
        # user = request.env.user
        # aa = filter(user.tb_users_blockhouse_res_groups_rel_ids)
        # domain = [('is_active', '=', True)]
        res = super(tb_blockhouse, self).search_read(domain, fields, offset, limit, order)
        return res

    # def filter_group(self):

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

    _sql_constraints = [
        ('name', 'unique(name)', 'Tên dự án không được trùng lặp'),
        ('code', 'unique(code)', 'Mã dự án không được trùng lặp')
    ]
