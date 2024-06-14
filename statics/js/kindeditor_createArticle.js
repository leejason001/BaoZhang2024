        var theKindEditor = null;
        function initKindEditor() {
            theKindEditor = KindEditor.create('#articleContent', {
                width: '50%',
                height: '300px',
                resizeType: 0,

                uploadJson:'/uploadFiles.html',

                items: [
                    'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', '|', 'emoticons', 'image', 'link'
                ]
            })
        }
        $(document).ready(function () {
            initKindEditor();
        })