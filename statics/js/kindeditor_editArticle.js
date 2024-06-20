        var theKindEditor = null;
        function initKindEditor() {
            theKindEditor = KindEditor.create('#articleContent', {
                width: '50%',
                height: '300px',
                resizeType: 0,

                uploadJson:'/uploadFiles.html',

                items: [
                    'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', '|', 'emoticons', 'image', 'link'
                ],afterBlur: function () {
                    $('#articleContent').val(theKindEditor.html())
                }
            })
        }
        $(document).ready(function () {
            initKindEditor();
            theKindEditor.html($('#articleContent').val())

        })