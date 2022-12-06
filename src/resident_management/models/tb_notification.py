from pyfcm import FCMNotification

from odoo import models, fields, http

from odoo.exceptions import ValidationError
from odoo.tools import GettextAlias

_ = GettextAlias()
push_service = FCMNotification(
    api_key="AAAAz6dhWnM:APA91bE2nkH_zcfTAlAuMkCLfnZ1m2y7zg_YMEmQnYBPkZ6JHpUQpNkYqh8f9vtRckFZX1Pl50aUXCbfni23b81OyMkDEPwnctsj4Sg9-IZx_tpgFVajvZMamtVz7_aZInJaRMtaGk_5")
registration_id = 'fOSDRZ9fQDylz6B6EDjQky:APA91bHVSGvQM7C6HYwgTnWI_RgPEZI0G4J2_IQ-UobBZsAK1HrKTI1Y0QlBm7ABd8BLMLCBMWqjSGBM2WhN6pLxj4xt2I4qjNMa3pylwj43jyUVubG9ZdLFKJuiYUus8299RKtDuhA_'
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
class tb_notification(models.Model):
    _name = 'tb_notification'
    _description = 'Thông báo'

    name = fields.Char(string='Tiêu đề', required=True, copy=False, )
    content = fields.Text(string='Nội dung', required=True, copy=False, )
    type = fields.Selection([
        ('NEWS', 'Bản tin'),
        ('ACTIVE_BY_ADMIN', 'Thông báo từ quản trị viên'),
    ], required=True, default='ACTIVE_BY_ADMIN', tracking=True, string="Loại thông báo", )
    state = fields.Selection([
        ('PENDING', 'Chờ duyệt'),
        ('ACTIVE', 'Đã duyệt'),
        ('REJECT', 'Chưa duyệt'),
    ], required=True, default='PENDING', tracking=True, string="Trạng thái", )
    # recipient_list = fields.Many2one(comodel_name='res.users', string="Người nhận")
    # user_ids = fields.One2many('res.users', 'notification_id', string='Users', help="Chọn người nhận")
    user_ids = fields.Many2many('res.users', string='Chọn người nhận')
    def set_status_active(self):
        try:
            self.write({'state': 'ACTIVE'})
            users_list = self.user_ids.ids
            token_list = []
            fcm_token_list = http.request.env['tb_fcm_token'].sudo().search([('user_id', 'in', users_list)], order="id asc")
            for item in users_list:
                http.request.env['tb_push_notification'].sudo().create({
                    'name': self.name,
                    'notification_id': self.id,
                    'notification_status': 'SENT',
                    'content': self.content,
                    'type': self.type,
                    'user_id': item.user_id
                })
            for item in fcm_token_list:
                token_list.append(item.name)
            # push_service.notify_multiple_devices(registration_ids=token_list,
            #                                               message_title="Bản tin mới", message_body=self.name)

        except Exception as e:
            print(e)
    def set_status_reject(self):
        self.write({'state': 'REJECT'})

    def write(self, values):
        if 'state' in values and self.env.user.has_group('resident_management.group_management'):
            raise ValidationError(_("Vui lòng liên hệ ban quản trị để được duyệt bản tin!"))
            return super(tb_news, self).write(values)
        if 'state' not in values:
            values['state'] = 'PENDING'
            return super(tb_notification, self).write(values)
        else:
            return super(tb_notification, self).write(values)
        # here you can do accordingly
