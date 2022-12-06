import datetime

from odoo import models, fields, api
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
    state = fields.Selection([
        ('DRAFT', 'Nháp'),
        ('ACTIVE', 'Đã đăng'),
        ('REJECT', 'Chưa duyệt'),
    ], required=True, default='DRAFT', tracking=True, string="Trạng thái", )

    def set_status_active(self):
        push_service.notify_single_device(
            registration_id=registration_id,
            message_title="Bản tin mới",
            message_body=self.name
        )
        self.write({'state': 'ACTIVE'})

    def set_status_reject(self):
        self.write({'state': 'REJECT'})

    def set_status_draft(self):
        self.write({'state': 'DRAFT'})

    def write(self, values):
        if 'state' in values and self.env.user.has_group('resident_management.group_management'):
            raise ValidationError(_("Vui lòng liên hệ ban quản trị để được duyệt bản tin!"))
            return super(tb_news, self).write(values)
        if 'state' not in values:
            values['state'] = 'DRAFT'
            return super(tb_news, self).write(values)
        else:
            return super(tb_news, self).write(values)
        # here you can do accordingly

    def action_date(self):
        print("")
