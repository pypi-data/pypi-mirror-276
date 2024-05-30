this.ckan.module('wysiwyg-summernote-init', function ($) {
    return {
        options: {
            editor: "summernote"
        },
        initialize: function () {
            $.proxyAll(this, /_/);

            htmx.on("htmx:afterSettle", this._initEditors);

            // on first init
            this._initEditors();
        },

        _initEditors: function (e) {
            let elements = document.querySelectorAll(`[wysiwyg-editor='${this.options.editor}']`);

            if (typeof e !== 'undefined') {
                if (e.target.getAttribute("wysiwyg-editor") === this.options.editor) {
                    this._initEditor(e.target);
                    return;
                }

                elements = e.target.querySelectorAll(`[wysiwyg-editor='${this.options.editor}']`);
            }

            for (let node of elements) {
                this._initEditor(node);
            }
        },

        /**
         * Initialize Summernote editor on an element
         *
         * @param {Node} element
         */
        _initEditor: function (element) {
            $(element).summernote({
                minHeight: 300,
                callbacks: {
                    onImageUpload: (file) => {
                        this.onImageUpload(file[0]);
                    },
                },
            });
        },
        onImageUpload: function (file) {
            let self = this;
            let data = new FormData();
            data.append("upload", file);

            $.ajax({
                data: data,
                type: "POST",
                url: ckan.url('/wysiwyg/upload_file'), //Your own back-end uploader
                cache: false,
                contentType: false,
                processData: false,
                success: function (response) {
                    if (response.error) {
                        return self.sandbox.publish("ap:notify", response.error.message, "error");
                    }

                    if (!response.url) {
                        return;
                    }

                    self.el.summernote('editor.insertImage', response.url);
                }
            });
        }
    };
});
