var theKindEditor = null;
function initKindEditor() {
    theKindEditor = KindEditor.create('#solution', {
        width: '50%',
        height: '300px',
        resizeType: 0,

        uploadJson:'/uploadFiles.html',

        items: [
            'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', '|', 'emoticons', 'image', 'link'
        ],afterBlur: function () {
            $('#solution').val(theKindEditor.html())
        }
    })
}
$(document).ready(function() {
    initKindEditor();
})