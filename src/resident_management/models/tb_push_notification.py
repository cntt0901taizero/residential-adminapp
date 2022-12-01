from builtins import print

from odoo import models, fields


class tb_push_notification(models.Model):
    _name = 'tb_push_notification'
    # _description = 'Quản lý thiết bị'

    name = fields.Char(string='Tiêu đề', required=True, copy=False)
    # user_id = fields.Integer(string="Người dùng")
    notification_id = fields.Integer(string="Thông báo")
    notification_status = fields.Integer(string="Trạng thái")
    content = fields.Text(string='Nội dung', required=True, copy=False, )
    type = fields.Selection([
        ('NEWS', 'Bản tin'),
        ('ACTIVE_BY_ADMIN', 'Thông báo từ quản trị viên'),
    ], required=True, default='ACTIVE_BY_ADMIN', tracking=True, string="Loại thông báo", )
    notification_status = fields.Selection([
        ('SENT', 'Đã gửi'),
        ('SEEN', 'Đã đọc'),
        ('DELETE', 'Đã xóa'),
    ], required=True, default='SENT', tracking=True, string="Trạng thái", )
    user_id = fields.Many2one(comodel_name='res.users')






