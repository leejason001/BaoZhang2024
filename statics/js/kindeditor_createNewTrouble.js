        var theKindEditor = null;
        function initKindEditor() {
            theKindEditor = KindEditor.create('#detail', {
                width: '50%',
                height: '300px',
                resizeType: 0,

                uploadJson:'/uploadFiles.html',

                items: [
                    'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', '|', 'emoticons', 'image', 'link'
                ],afterBlur: function () {
                    $('#detail').val(theKindEditor.html())
                }
            })
        }
        $(document).ready(function () {
            initKindEditor();

        })