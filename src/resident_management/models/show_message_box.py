from odoo import models, fields


class dialog_box_confirm(models.TransientModel):
    _name = 'dialog.box.confirm'
    _description = "Show Message"

    message = fields.Text(default='Xác nhận')

    def action_confirm(self):
        for selected_item in self._context.get('active_ids'):
            record = self.env[self._context.get('active_model')].browse(selected_item)
            record.del_record()
            return {
                'type': 'ir.actions.act_window_close',
            }





