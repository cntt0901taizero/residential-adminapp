odoo.define('resident_management.button_create_admin_user', async function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var FormController = require('web.FormController');
    var rpc = require('web.rpc');
    var ListView = require('web.ListView');
    var FormView = require('web.FormView');
    var model_name = 'res.users'
    var viewRegistry = require('web.view_registry');
    var perm_create_admin_user = await rpc.query({
                                model: 'res.users',
                                method: 'check_perm_create',
                                args: ["perm_create_admin_user"],
                            });
    var perm_write_admin_user = await rpc.query({
                                model: 'res.users',
                                method : 'check_perm_create',
                                args: ["perm_write_admin_user"],
                            });
//    var form_id = await rpc.query({
//        model: 'ir.ui.view',
//        method: 'search_read',
//        args: [[
//                ['name', '=', 'res.users.admin.form.inherit'],
//              ]]
//    })

    var TreeButton = ListController.extend({
       renderButtons: async function($node) {
            this._super.apply(this, arguments);
            if(this.$buttons && perm_create_admin_user) {
                this.$buttons.find('.btn.btn-primary.o_list_button_add').show();
            }
            else{
                this.$buttons.find('.btn.btn-primary.o_list_button_add').hide();
            }
       }
    });
    var AdminUserListView = ListView.extend({
       config: _.extend({}, ListView.prototype.config, {
           Controller: TreeButton,

       }),
    });
    viewRegistry.add('tree_action_admin_user', AdminUserListView);

    var FormActionController = FormController.extend({
        renderButtons: async function($node) {
            this._super.apply(this, arguments);
            if(this.$buttons && perm_create_admin_user) {
                this.$buttons.find('.btn.btn-secondary.o_form_button_create').show();
            }
            else{
                this.$buttons.find('.btn.btn-secondary.o_form_button_create').hide();
            }
            if(this.$buttons && perm_write_admin_user) {
                this.$buttons.find('.btn.btn-primary.o_form_button_edit').show();
            }
            else{
                this.$buttons.find('.btn.btn-primary.o_form_button_edit').hide();
            }
       }

    });

    var FormActionView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: FormActionController
        }),
    });

    viewRegistry.add('form_action_admin_user', FormActionView);

});





