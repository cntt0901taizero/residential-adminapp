import datetime
from odoo import models, fields, api, exceptions
from pyfcm import FCMNotification

from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import GettextAlias
from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE

str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]
_ = GettextAlias()
push_service = FCMNotification(
    api_key="AAAAz6dhWnM:APA91bE2nkH_zcfTAlAuMkCLfnZ1m2y7zg_YMEmQnYBPkZ6JHpUQpNkYqh8f9vtRckFZX1Pl50aUXCbfni23b81OyMkDEPwnctsj4Sg9-IZx_tpgFVajvZMamtVz7_aZInJaRMtaGk_5")
registration_id = 'eP9mbUhLTZujCbTfJd3Dct:APA91bGwPa8vG2e4Vp1MkOlWdoQIVI-xEdgXIwB0JXoxGMWragEXulseCHMMt82UHzRbx3iD_hF-C2jSW6H2WKsCuMlMGtB8d5MuJ0GvjT-wJB0btvzK2VyM30xDnU7eZPQCLw8srGiK'
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"


class tb_news(models.Model):
    _name = 'tb_news'
    _description = 'Bản tin'

    name = fields.Char(string='Tiêu đề bản tin', required=True, )
    content = fields.Html(string='Nội dung', copy=False, )
    file = fields.Binary(string='Tài liệu', attachment=True, help='Chọn tài liệu tải lên')
    file_name = fields.Char(string='Tên tài liệu')
    news_description = fields.Char(string="Mô tả")
    image = fields.Image(string="Ảnh bản tin")
    create_date = fields.Date(string="Ngày tạo", default=datetime.datetime.today())
    # active = fields.Boolean(string='Có hiệu lực', default=True)
    expired_date = fields.Date(string="Ngày hết hạn", default=datetime.datetime.today())
    status = fields.Selection([
        ('DRAFT', 'Chờ phê duyệt'),
        ('REJECT', 'Từ chối duyệt'),
        ('ACTIVE', 'Đã đăng'),
    ], required=True, default='DRAFT', tracking=True, string="Trạng thái", )
    news_type = fields.Selection([
        ('PROJECT_APARTMENT', 'Dự án'),
        ('BUILDING', 'Tòa nhà'),
    ], required=True, default='PROJECT_APARTMENT', string="Gửi tới")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    domain=lambda self: self._domain_blockhouse_id(),
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")

    perm_approve = fields.Boolean(string='Phê duyệt', compute='_compute_perm_approve')

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



    @api.onchange('blockhouse_id')
    def on_change_blockhouse_id(self):
        self.building_id = None

    def set_status_active(self):
        push_service.notify_single_device(
            registration_id=registration_id,
            message_title="Bản tin mới",
            message_body=self.name
        )
        self.write({'status': 'ACTIVE'})

    def set_status_reject(self):
        self.write({'status': 'REJECT'})

    def set_status_draft(self):
        self.write({'status': 'DRAFT'})

    def write(self, values):
        if 'news_type' in values:
            if values["news_type"] == 'PROJECT_APARTMENT':
                values["building_id"] = None
        if 'status' not in values:
            values['status'] = 'DRAFT'
        return super(tb_news, self).write(values)

        # here you can do accordingly

    @api.model
    def create(self, vals):
        if vals["news_type"] == 'PROJECT_APARTMENT':
          vals["building_id"] = None
        return super(tb_news, self).create(vals)


    def open_edit_form_news(self):
        form_id = self.env.ref('apartment_service_support.view_tb_news_form')
        canwrite = self.check_access_rights('write', raise_exception=False)
        if not canwrite:
            raise ValidationError('Bạn không có quyền chỉnh sửa bản tin.')
        self.check_access_rights('write')
        # then open the form
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cập nhật bản tin',
            'res_model': 'tb_news',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {'form_view_initial_mode': 'edit'},
            # if you want to open the form in edit mode direclty
            'target': 'current',
        }

    # @api.multi
    def confirm_delete_news(self):
        candelete = self.check_access_rights('unlink', raise_exception=False)
        if not candelete:
            raise ValidationError('Bạn không có quyền xóa bản tin.')
        message = """Bạn có chắc muốn xóa bản tin này?"""
        value = self.env['dialog.box.confirm'].sudo().create({'message': message})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Xóa bản tin',
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