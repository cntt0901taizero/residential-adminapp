import datetime
from odoo import models, fields, api, exceptions
from pyfcm import FCMNotification

from odoo.exceptions import ValidationError
from odoo.tools import GettextAlias


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
    image = fields.Image(string="Ảnh bản tin")
    create_date = fields.Date(string="Ngày tạo", default=datetime.datetime.today())
    # active = fields.Boolean(string='Trạng thái', default=True)
    expired_date = fields.Date(string="Ngày hết hạn", default=datetime.datetime.today())
    status = fields.Selection([
        ('DRAFT', 'Nháp'),
        ('ACTIVE', 'Đã đăng'),
        ('REJECT', 'Chưa duyệt'),
    ], required=True, default='DRAFT', tracking=True, string="Trạng thái", )
    news_type = fields.Selection([
        ('PROJECT_APARTMENT', 'Dự án'),
        ('BUILDING', 'Tòa nhà'),
    ], required=True, default='PROJECT_APARTMENT', string="Gửi tới")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    ondelet="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Toà nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelet="cascade")

    @api.onchange('news_type')
    def on_change_news_type(self):
        self.blockhouse_id = None
        self.building_id = None

    @api.onchange('blockhouse_id')
    def on_change_news_type(self):
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
        if 'status' in values and self.env.user.has_group('resident_management.group_management'):
            raise ValidationError(_("Vui lòng liên hệ ban quản trị để được duyệt bản tin!"))
            return super(tb_news, self).write(values)
        if 'status' not in values:
            values['status'] = 'DRAFT'
            return super(tb_news, self).write(values)
        else:
            return super(tb_news, self).write(values)
        # here you can do accordingly

    def action_date(self):
        print("")

    def open_edit_form_news(self):
        form_id = self.env.ref('apartment_news.view_tb_news_form')
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