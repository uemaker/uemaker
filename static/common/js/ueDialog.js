;(function ($) {
    $.ueDialog = function () {
        var defaults = {
            id: "modal",//弹窗id
            title: "dialog",//弹窗标题
            footer: true,
            type: 'default',
            showCancel: true,
            backdrop: false,//是否显示遮障，和原生bootstrap 模态框一样
            keyboard: true,//是否开启esc键退出，和原生bootstrap 模态框一样
            remote: "",//加载远程url，和原生bootstrap 模态框一样
            openEvent: null,//弹窗打开后回调函数
            closeEvent: null,//弹窗关闭后回调函数
            okEvent: null//单击确定按钮回调函数
        };
        //动态创建窗口
        var _createDialog = {
            init: function (opts) {
                var _self = this;
                var d = _self._html(opts);
                $("body").append(d);
                var modal = $("#" + opts.id);
                //初始化窗口
                modal.modal({
                    backdrop: opts.backdrop,
                    keyboard: opts.keyboard
                });
                if(opts.remote){
                    $(".modal-body").load(opts.remote);
                }

                modal
                //显示窗口
                .modal('show')
                //隐藏窗口后删除窗口html
                .on('hidden.bs.modal', function () {
                    modal.remove();
                    $(".modal-backdrop").remove();
                    if (opts.closeEvent) {
                        opts.closeEvent();
                    }
                })
                //窗口显示后
                .on('shown.bs.modal', function () {
                    if (opts.openEvent) {
                        opts.openEvent();
                    }
                });
                //绑定按钮事件
                $(".ok").click(function () {
                    if (opts.okEvent) {
                        opts.okEvent();
                    }
                    modal.modal('hide');
                });

                return modal;
            },
            _html: function (o) {
                var model_cls = model_label_cls = model_dialog_cls = '';
                if(o.type == 'small'){
                    model_cls = 'bs-example-modal-sm';
                    model_label_cls = 'mySmallModalLabel';
                    model_dialog_cls = 'modal-sm';
                }else if(o.type == 'large'){
                    model_cls = 'bs-example-modal-lg';
                    model_label_cls = 'myLargeModalLabel';
                    model_dialog_cls = 'modal-lg';
                }
                modalHtml = '<div id="' + o.id + '" class="modal fade '+ model_cls +'" tabindex="-1" role="dialog" aria-labelledby="'+ model_label_cls +'">';
                modalHtml += '<div class="modal-dialog '+ model_dialog_cls +'" role="document"><div class="modal-content">';
                if(o.title){
                    modalHtml += '<div class="modal-header"><button type="button" class="close" data-dismiss="modal" ><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>' +
                    '<h4 id="myModalLabel" class="modal-title">' + o.title + '</h4></div>';
                }
                modalHtml += '<div class="modal-body" ><p>' + o.content + '</p></div>';
                if(o.footer){
                    modalHtml += '<div class="modal-footer">';
                        if(o.showCancel){
                            modalHtml += '<button class="btn" data-dismiss="modal" aria-hidden="true">取消</button>';
                        }
                    modalHtml += '<button class="btn btn-primary ok">确定</button></div>';
                }
                modalHtml += '</div></div></div>';
                return modalHtml;
            }
        };
        return {
            success: function (msg, callback) {
                var opt = $.extend({}, defaults, {
                    id: 'success_modal',
                    type: 'small',
                    title: '',
                    footer: false,
                    content: msg,
                    backdrop: true,
                    keyboard: false,
                    closeEvent: callback
                });
                $(".modal").remove();
                var modal = _createDialog.init(opt);
                setTimeout(function () {
                    modal.modal('hide');
                }, 2000)
            },
            error: function (msg) {
                var opt = $.extend({}, defaults, {
                    id: 'error_modal',
                    type: 'small',
                    title: '',
                    footer: false,
                    content: msg,
                    backdrop: true,
                    keyboard: false
                });
                $(".modal").remove();
                var modal = _createDialog.init(opt);
                setTimeout(function () {
                    modal.modal('hide');
                }, 2000)
            },
            alert: function (msg) {
                var opt = $.extend({}, defaults, {
                    id: 'alert_modal',
                    type: 'small',
                    title: '',
                    footer: true,
                    content: msg,
                    backdrop: true,
                    keyboard: false,
                    showCancel: false,
                });
                $(".modal").remove();
                _createDialog.init(opt);
            },
            confirm: function (msg, callback) {
                 var opt = $.extend({}, defaults, {
                    id: 'confirm_modal',
                    type: 'small',
                    title: '',
                    footer: true,
                    content: msg,
                    backdrop: true,
                    keyboard: false,
                    okEvent: callback
                });
                $(".modal").remove();
                _createDialog.init(opt);
            },
            loadpage: function (url, opt) {
                var opt = $.extend({}, defaults, {
                    id: 'page_modal',
                    remote: url
                }, opt);
                $(".modal").remove();
                _createDialog.init(opt);
            }
        };

    }
})(jQuery);