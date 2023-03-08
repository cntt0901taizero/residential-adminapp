odoo.define('toaster_mixin.success', function (require) {
    "use strict";

    var messaging = require('web.messaging');
    var ToasterMixin = {
        /**
         * Display a toaster message when the record is saved successfully
         * @override
         */
        saveRecord: function () {
            var self = this;
            window.close();
            return this._super.apply(this, arguments).then(function () {
                messaging.toastMessage({
                    message: "Đã có lỗi xảy ra.",
                    type: "error"
                });
                return self.reload();
            });
        },
    };
    return ToasterMixin;

});





