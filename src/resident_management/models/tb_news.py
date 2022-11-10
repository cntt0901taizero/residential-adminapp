import datetime

from odoo import models, fields, api
from pyfcm import FCMNotification

from odoo.exceptions import ValidationError
from odoo.tools import GettextAlias

_ = GettextAlias()
push_service = FCMNotification(
    api_key="AAAAz6dhWnM:APA91bE2nkH_zcfTAlAuMkCLfnZ1m2y7zg_YMEmQnYBPkZ6JHpUQpNkYqh8f9vtRckFZX1Pl50aUXCbfni23b81OyMkDEPwnctsj4Sg9-IZx_tpgFVajvZMamtVz7_aZInJaRMtaGk_5")
registration_id = 'dsaQ4hK8Tt2BiYcpstSQz7:APA91bGJHEkaWqlzOky-a9uNJzMhVa2f708tcYXLV-9IrXpqhqkDemI0UZ1uaSnV1TSlQjlCu54fO59AmN0P3ubYDBZDk9zaW8oIDLxTtDa1EzuPwnNUL0stkkPn1kutHOqmnOx7h0UB'
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"


class tb_news(models.Model):
    _name = 'tb_news'
    _description = 'Bảng tin'

    name = fields.Char(string='Tiêu đề bảng tin', required=True, )
    content = fields.Html(string='Nội dung', copy=False, )
    file = fields.Binary(string='Tài liệu', attachment=True, help='Chọn tài liệu tải lên')
    file_name = fields.Char(string='Tên tài liệu')
    image = fields.Image(string="Ảnh bảng tin")
    create_date = fields.Date(string="Ngày tạo", default=datetime.datetime.today())
    # active = fields.Boolean(string='Trạng thái', default=True)
    expired_date = fields.Date(string="Ngày hết hạn", default=datetime.datetime.today())
    state = fields.Selection([
        ('DRAFT', 'Nháp'),
        ('ACTIVE', 'Đã đăng'),
        ('REJECT', 'Chưa duyệt'),
    ], required=True, default='DRAFT', tracking=True, string="Trạng thái", )

    def set_status_active(self):
        try:
            result = push_service.notify_single_device(registration_id=registration_id, message_title="Bản tin mới",
                                                       message_body=self.name)
        except Exception as e:
            print(e)

        self.write({'state': 'ACTIVE'})

    def set_status_reject(self):
        # for rec in self:
        #     rec.state = 'ACTIVE'
        self.write({'state': 'REJECT'})

    def set_status_draft(self):
        # for rec in self:
        #     rec.state = 'DRAFT'
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