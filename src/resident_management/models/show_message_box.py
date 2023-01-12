from odoo import models, fields


class dialog_box_confirm(models.TransientModel):
    _name = 'dialog.box.confirm'
    _description = "Show Message"

    message = fields.Text(default='Xác nhận')
    content = fields.Text(required=True)


    # def action_confirm(self):
    #     print("111111111111111111111")
    #     return {
    #         'type': 'ir.actions.act_window_close',
    # }





