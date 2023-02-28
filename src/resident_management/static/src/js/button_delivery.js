odoo.define('resident_management.button_delivery', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var ListController = require('web.ListController');
    var FormController = require('web.FormController');
    var rpc = require('web.rpc');
    var ListView = require('web.ListView');
    var FormView = require('web.FormView');
    var model_name = 'res.users'
    var viewRegistry = require('web.view_registry');
    var perm_create = rpc.query({
                                    model: 'res.users',
                                    method: 'check_perm_user',
                                    args: ["perm_create_delivery"],
                                });
    var perm_delete = rpc.query({
                                    model: 'res.users',
                                    method: 'check_perm_user',
                                    args: ["perm_delete_delivery"],
                                });
    var perm_write = rpc.query({
                                    model: 'res.users',
                                    method : 'check_perm_user',
                                    args: ["perm_write_delivery"],
                                });
    var perm_approve = rpc.query({
                                    model: 'res.users',
                                    method : 'check_perm_user',
                                    args: ["perm_approve_delivery"],
                                });

    var TreeButton = ListController.extend({
       updateButtons: async function() {
            this._super.apply(this, arguments);
            Promise.all([perm_create])
            .then(perm=>{
                 if(this.$buttons && perm[0]) {
                            this.$buttons.find('.btn.btn-primary.o_list_button_add').show();
                 }
                 else{
                        this.$buttons.find('.btn.btn-primary.o_list_button_add').hide();
                 }
            })
        },
    });
    var AdminUserListView = ListView.extend({
       config: _.extend({}, ListView.prototype.config, {
           Controller: TreeButton,

       }),
    });
    viewRegistry.add('tree_action_delivery', AdminUserListView);

    var FormActionController = FormController.extend({
        renderButtons: async function($node) {
            this._super.apply(this, arguments);
            if(this.$buttons){
                Promise.all([perm_create, perm_write])
                .then(perm=>{
                      if(perm[0]) this.$buttons.find('.btn.btn-secondary.o_form_button_create').show();
                      else this.$buttons.find('.btn.btn-secondary.o_form_button_create').hide();
                      if(perm[1]) this.$buttons.find('.btn.btn-primary.o_form_button_edit').show();
                      else this.$buttons.find('.btn.btn-primary.o_form_button_edit').hide();
                })
            }
       },
       _getActionMenuItems: function (state) {
            if (!this.hasActionMenus || this.mode === 'edit') {
                return null;
            }
            const props = this._super(...arguments);
            const activeField = this.model.getActiveField(state);
            const otherActionItems = [];
            if (this.archiveEnabled && activeField in state.data) {
                if (state.data[activeField]) {
                    otherActionItems.push({
                        description: _t("Archive"),
                        callback: () => {
                            Dialog.confirm(this, _t("Are you sure that you want to archive this record?"), {
                                confirm_callback: () => this._toggleArchiveState(true),
                            });
                        },
                    });
                } else {
                    otherActionItems.push({
                        description: _t("Unarchive"),
                        callback: () => this._toggleArchiveState(false),
                    });
                }
            }
            if (this.activeActions.create && this.activeActions.duplicate) {
                otherActionItems.push({
                    description: _t("Duplicate"),
                    callback: () => this._onDuplicateRecord(this),
                });
            }
            Promise.all([perm_delete])
                .then(perm=>{
                       if (this.activeActions.delete && perm[0]) {
                            otherActionItems.push({
                                description: _t("Delete"),
                                callback: () => this._onDeleteRecord(this),
                            });
                        }
                        if (!perm[1] && this.toolbarActions.action) {
                           var newActions = this.toolbarActions.action.filter(k=> k.id != 70)
                           this.toolbarActions = newActions
                        }
                })

            return Object.assign(props, {
                items: Object.assign(this.toolbarActions, { other: otherActionItems }),
            });
       },
    });

    var FormActionView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: FormActionController
        }),
    });

    viewRegistry.add('form_action_delivery', FormActionView);

});





