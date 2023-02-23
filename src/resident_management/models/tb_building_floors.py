from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    name = fields.Char(string='Tên tầng sàn', size=100, required=True, copy=False)
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

    @api.depends('create_date')
    def _compute_row_number(self):
        for record in self:
            record.row_number = self.search([], order='create_date').ids.index(record.id) + 1

    def set_status_active(self):
        self.is_active = True

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

