from odoo import models, fields
from pyfcm import FCMNotification

push_service = FCMNotification(
    api_key="AAAAz6dhWnM:APA91bE2nkH_zcfTAlAuMkCLfnZ1m2y7zg_YMEmQnYBPkZ6JHpUQpNkYqh8f9vtRckFZX1Pl50aUXCbfni23b81OyMkDEPwnctsj4Sg9-IZx_tpgFVajvZMamtVz7_aZInJaRMtaGk_5")
registration_id = 'dsaQ4hK8Tt2BiYcpstSQz7:APA91bGJHEkaWqlzOky-a9uNJzMhVa2f708tcYXLV-9IrXpqhqkDemI0UZ1uaSnV1TSlQjlCu54fO59AmN0P3ubYDBZDk9zaW8oIDLxTtDa1EzuPwnNUL0stkkPn1kutHOqmnOx7h0UB'
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
    ], required=True, default='NEWS', tracking=True, string="Loại thông báo", )
    state = fields.Selection([
        ('PENDING', 'Chờ duyệt'),
        ('ACTIVE', 'Đã duyệt'),
        ('REJECT', 'Chưa duyệt'),
    ], required=True, default='PENDING', tracking=True, string="Trạng thái", )
    def set_status_active(self):
        self.write({'state': 'ACTIVE'})
    def set_status_reject(self):
        self.write({'state': 'REJECT'})
