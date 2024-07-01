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
    $('select[name=solutionChoices]').change(function (event) {
        if(true == $(this).parent().children('input').prop('checked')) {
            $.ajax({
                url:'/backend/getSolutionAlternatedContent',
                type: 'get',
                data: {'solutionAlternatedId': $('select[name=solutionChoices] option:selected').attr('value')},
                success: function (arg) {
                    console.log(arg)

                }
            })
        }
    })
})