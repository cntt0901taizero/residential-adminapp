from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_resident_handbook(models.Model):
    _name = 'tb_resident_handbook'
    _description = 'Cẩm nang cư dân'

    name = fields.Char(string='Chủ đề', required=True, copy=False)
    # image = fields.Image(string='Ảnh', copy=False)
    description = fields.Char(string='Tiêu đề', copy=False)
    detail_description = fields.Html(string='Mô tả', copy=False)
    is_active = fields.Boolean(string='Trạng thái', default=True)

    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")

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
        res = super(tb_resident_handbook, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
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
        res = super(tb_resident_handbook, self).search_read(domain, fields, offset, limit, order)
        return res

    def set_status_active(self):
        self.is_active = True

    def open_edit_form(self):
        can_do = self.check_access_rights('write', raise_exception=False)
        if not can_do:
            raise ValidationError('Bạn không có quyền chỉnh sửa thông tin!')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sửa: ' + self.name,
            'res_model': 'tb_resident_handbook',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('apartment_service_support.view_tb_resident_handbook_form').id,
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




