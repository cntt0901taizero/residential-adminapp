import datetime

from odoo import models, fields, api
from pyfcm import FCMNotification

from odoo.exceptions import ValidationError
from odoo.tools import GettextAlias

_ = GettextAlias()
registration_id = 'fOSDRZ9fQDylz6B6EDjQky:APA91bHVSGvQM7C6HYwgTnWI_RgPEZI0G4J2_IQ-UobBZsAK1HrKTI1Y0QlBm7ABd8BLMLCBMWqjSGBM2WhN6pLxj4xt2I4qjNMa3pylwj43jyUVubG9ZdLFKJuiYUus8299RKtDuhA_'
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
        # try:
        #     push_service.notify_single_device(
        #         registration_id=registration_id,
        #         message_title="Bản tin mới",
        #         message_body=self.name
        #     )
        # except Exception as e:
        #     print(e)

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
