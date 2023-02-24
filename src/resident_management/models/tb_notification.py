from pyfcm import FCMNotification
from odoo import models, fields, http, api
from odoo.exceptions import ValidationError
from odoo.tools import GettextAlias
from odoo.addons.resident_management.models.tb_users_blockhouse_res_groups_rel import USER_GROUP_CODE

_ = GettextAlias()
push_service = FCMNotification(
    api_key="AAAAz6dhWnM:APA91bE2nkH_zcfTAlAuMkCLfnZ1m2y7zg_YMEmQnYBPkZ6JHpUQpNkYqh8f9vtRckFZX1Pl50aUXCbfni23b81OyMkDEPwnctsj4Sg9-IZx_tpgFVajvZMamtVz7_aZInJaRMtaGk_5")
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
str_bql = USER_GROUP_CODE[2][0]
str_bqt = USER_GROUP_CODE[3][0]


class tb_notification(models.Model):
    _name = 'tb_notification'
    _description = 'Thông báo'

    name = fields.Char(string='Tiêu đề', required=True, copy=False, )
    content = fields.Html(string='Nội dung', copy=False, required=True, )
    image = fields.Image(string="Ảnh", required=True)
    type = fields.Selection([
        ('NEWS', 'Bản tin'),
        ('ACTIVE_BY_ADMIN', 'Thông báo từ quản trị viên'),
    ], required=True, default='ACTIVE_BY_ADMIN', tracking=True, string="Loại thông báo", )
    is_push = fields.Boolean(string='Đẩy thông báo', default=True)
    status = fields.Selection([
        ('PENDING', 'Chờ duyệt'),
        ('REJECT', 'Chưa duyệt'),
        ('ACTIVE', 'Đã đăng'),
    ], required=True, default='PENDING', tracking=True, string="Trạng thái", )
    receiver = fields.Selection([
        ('PROJECT_APARTMENT', 'Dự án'),
        ('BUILDING', 'Tòa nhà'),
        ('APARTMENT', 'Căn hộ'),
        ('USER_GROUP', 'Người dùng'),
    ], required=True, default='PROJECT_APARTMENT', string="Gửi tới")
    blockhouse_id = fields.Many2one(comodel_name='tb_blockhouse', string="Dự án",
                                    domain=lambda self: self._domain_blockhouse_id(),
                                    ondelete="cascade")
    building_id = fields.Many2one(comodel_name='tb_building', string="Tòa nhà",
                                  domain="[('blockhouse_id', '=', blockhouse_id)]",
                                  ondelete="cascade")
    building_house_id = fields.Many2one(comodel_name='tb_building_house', string="Căn hộ",
                                        domain="[('building_id', '=', building_id)]",
                                        ondelete="cascade")
    user_ids = fields.Many2many('res.users', string='Người nhận', ondelete="cascade")

    def _domain_blockhouse_id(self):
        user = http.request.env.user
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
        self.building_house_id = None

    @api.onchange('building_id')
    def on_change_building_id(self):
        self.building_house_id = None

    def set_status_active(self):
        try:
            user_id_list = []
            blockhouse_id = self.blockhouse_id.id
            building_id = self.building_id.id
            building_house_id = self.building_house_id.id
            if self.receiver == 'PROJECT_APARTMENT':
                self.env.cr.execute("""SELECT user_id FROM tb_users_blockhouse_res_groups_rel WHERE blockhouse_id=%s""",
                                    [blockhouse_id])
                user_id_list = self.env.cr.fetchall()
            if self.receiver == 'BUILDING':
                self.env.cr.execute(
                    """SELECT user_id FROM tb_users_blockhouse_res_groups_rel WHERE blockhouse_id=%s AND building_id=%s""",
                    (blockhouse_id, building_id))
                user_id_list = self.env.cr.fetchall()
            if self.receiver == 'APARTMENT':
                self.env.cr.execute(
                    """SELECT user_id FROM tb_users_blockhouse_res_groups_rel WHERE blockhouse_id=%s AND building_id=%s AND building_house_id=%s""",
                    (blockhouse_id, building_id, building_house_id))
                user_id_list = self.env.cr.fetchall()
            if self.receiver == 'USER_GROUP':
                user_id_list = self.user_ids.ids

            self.write({'status': 'ACTIVE'})
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
        if 'receiver' in values:
            if values['receiver'] == 'PROJECT_APARTMENT':
                values['building_id'] = None
                values['building_house_id'] = None
                values['user_ids'] = None
            if values['receiver'] == 'BUILDING':
                values['building_house_id'] = None
                values['user_ids'] = None
            if values['receiver'] == 'APARTMENT':
                values['user_ids'] = None
            if values['receiver'] == 'USER_GROUP':
                values['building_id'] = None
                values['building_house_id'] = None
                values['blockhouse_id'] = None
        # if 'user_ids' in values:
        #     if len(values['user_ids'][0][2]) == 0:
        #         raise ValidationError('Vui lòng chọn người nhận thông báo')
        return super(tb_notification, self).create(values)

    def write(self, values):
        if 'receiver' in values:
            if values['receiver'] == 'PROJECT_APARTMENT':
                values['building_id'] = None
                values['building_house_id'] = None
                values['user_ids'] = None
            if values['receiver'] == 'BUILDING':
                values['building_house_id'] = None
                values['user_ids'] = None
            if values['receiver'] == 'APARTMENT':
                values['user_ids'] = None
            if values['receiver'] == 'USER_GROUP':
                values['building_id'] = None
                values['building_house_id'] = None
                values['blockhouse_id'] = None
        if 'user_ids' in values and values['user_ids'] is not None:
            if len(values['user_ids'][0][2]) == 0:
                raise ValidationError('Vui lòng chọn người nhận thông báo')
        if 'status' in values:
            if not self.env.user.has_group('resident_management.group_administration'):
                raise ValidationError(_("Vui lòng liên hệ ban quản trị để được duyệt thông báo!"))
        if 'status' not in values:
            values['status'] = 'PENDING'
        # here you can do accordingly
        return super(tb_notification, self).write(values)


    def open_edit_form(self):
        form_id = self.env.ref('apartment_service_support.view_tb_notification_form')
        per_name = 'perm_write_notification'
        error_messenger = 'Bạn không có quyền chỉnh sửa thông báo.'
        can_do = self.check_permission(per_name, raise_exception=False)
        if not can_do:
            raise ValidationError(error_messenger)
        self.check_access_rights('write')
        # then open the form
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cập nhật thông báo',
            'res_model': 'tb_notification',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {'form_view_initial_mode': 'edit'},
            # if you want to open the form in edit mode direclty
            'target': 'current',
        }


    def confirm_delete(self):
        per_name = 'perm_delete_notification'
        error_messenger = 'Bạn không có quyền xóa thông báo.'
        can_do = self.check_permission(per_name, raise_exception=False)
        if not can_do:
            raise ValidationError(error_messenger)
        message = """Bạn có chắc muốn xóa bản tin này?"""
        value = self.env['dialog.box.confirm'].sudo().create({'message': message})
        return {
            'type': 'ir.actions.act_window',
            'name': 'Xóa thông báo',
            'res_model': 'dialog.box.confirm',

            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': value.id
        }
