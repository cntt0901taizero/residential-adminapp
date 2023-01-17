from pyfcm import FCMNotification
from odoo import models, fields, http, api
from odoo.exceptions import ValidationError
from odoo.tools import GettextAlias

_ = GettextAlias()
push_service = FCMNotification(
    api_key="AAAAz6dhWnM:APA91bE2nkH_zcfTAlAuMkCLfnZ1m2y7zg_YMEmQnYBPkZ6JHpUQpNkYqh8f9vtRckFZX1Pl50aUXCbfni23b81OyMkDEPwnctsj4Sg9-IZx_tpgFVajvZMamtVz7_aZInJaRMtaGk_5")
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"


class tb_notification(models.Model):

    _name = 'tb_notification'
    _description = 'Thông báo'

    name = fields.Char(string='Tiêu đề', required=True, copy=False, )
    content = fields.Html(string='Nội dung', copy=False, required=True, )
    type = fields.Selection([
        ('NEWS', 'Bản tin'),
        ('ACTIVE_BY_ADMIN', 'Thông báo từ quản trị viên'),
    ], required=True, default='ACTIVE_BY_ADMIN', tracking=True, string="Loại thông báo", )
    is_push = fields.Boolean(string='Đẩy thông báo', default=True)
    status = fields.Selection([
        ('PENDING', 'Chờ duyệt'),
        ('ACTIVE', 'Đã duyệt'),
        ('REJECT', 'Chưa duyệt'),
    ], required=True, default='PENDING', tracking=True, string="Trạng thái", )
    receiver = fields.Selection([
        ('PROJECT_APARTMENT', 'Dự án'),
        ('BUILDING', 'Tòa nhà'),
        ('APARTMENT', 'Căn hộ'),
        ('USER_GROUP', 'Người dùng'),
    ], required=True, default='PROJECT_APARTMENT', string="Gửi tới")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="dự án",
                                    ondelet="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelet="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ",
                                        domain="[('building_id', '=', building_id)]",
                                        ondelet="cascade")
    user_ids = fields.Many2many('res.users', string='Người nhận', ondelet="cascade")


    @api.onchange('blockhouse_id')
    def on_change_blockhouse_id(self):
        self.building_id = None
        self.building_house_id = None

    @api.onchange('building_id')
    def on_change_building_id(self):
        self.building_house_id = None

    def set_status_active(self):
        try:
            self.write({'status': 'ACTIVE'})
            user_id_list = self.user_ids.ids
            for user_id in user_id_list:
                http.request.env['tb_push_notification'].sudo().create({
                    'name': self.name,
                    'notification_id': self.id,
                    'notification_status': 'SENT',
                    'content': self.content,
                    'type': self.type,
                    'user_id': user_id
                })
            token_list = []
            fcm_token_list = http.request.env['tb_fcm_token'].sudo().search([('user_id', 'in', user_id_list)],
                                                                            order="id asc")
            for item in fcm_token_list:
                token_list.append(item.name)
            push_service.notify_multiple_devices(
                registration_ids=token_list,
                message_title="Bản tin mới",
                message_body=self.name)

        except Exception as e:
            print(e)

    def set_status_reject(self):
        self.write({'status': 'REJECT'})

    @api.model
    def create(self, values):
        if 'receiver' in values and values['receiver'] == 'PROJECT_APARTMENT':
            values['building_id'] = None
            values['building_house_id'] = None
            values['user_ids'] = None
        if 'receiver' in values and values['receiver'] == 'BUILDING':
            values['building_house_id'] = None
            values['user_ids'] = None
        if 'receiver' in values and values['receiver'] == 'APARTMENT':
            values['user_ids'] = None
        if 'receiver' in values and values['receiver'] == 'USER_GROUP':
            values['building_id'] = None
            values['building_house_id'] = None
            values['blockhouse_id'] = None
        return super(tb_notification, self).create(values)


    def write(self, values):
        if 'receiver' in values and values['receiver'] == 'PROJECT_APARTMENT':
            values['building_id'] = None
            values['building_house_id'] = None
            values['user_ids'] = None
        if 'receiver' in values and values['receiver'] == 'BUILDING':
            values['building_house_id'] = None
            values['user_ids'] = None
        if 'receiver' in values and values['receiver'] == 'APARTMENT':
            values['user_ids'] = None
        if 'receiver' in values and values['receiver'] == 'USER_GROUP':
            values['building_id'] = None
            values['building_house_id'] = None
            values['blockhouse_id'] = None
        if 'status' in values and self.env.user.has_group('resident_management.group_management'):
            raise ValidationError(_("Vui lòng liên hệ ban quản trị để được duyệt thông báo!"))
        if 'status' not in values:
            values['status'] = 'PENDING'
        # here you can do accordingly
        return super(tb_notification, self).write(values)
