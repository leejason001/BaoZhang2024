        var theKindEditor = null;
        function initKindEditor() {
            theKindEditor = KindEditor.create('#commentToTheArticle', {
                width: '50%',
                height: '300px',
                resizeType: 0,
                items: [
                    'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', '|', 'emoticons', 'image', 'link'
                ]
            })
        }
        function submitCommentToTheArticle(articleId, content, commentContainer) {
                 $.ajax({
                    url:'/readerCommentTheArticle/',
                    type: 'post',
                    data: {'article_id': articleId, 'content':content, 'parentComment': commentContainer.attr('me')},
                    dataType: 'json',
                    success: function (arg) {
                         var commentDom = '<div class="levelOffset">' + arg.username + '</div><div class="theComment levelOffset" article=' + articleId + ' me=' + arg.comment_id + '>' + content + '<div class="replayOnComment rightLocation"><button class="replayButton">回复</button></div><div class="replayArea"><textarea></textarea><div class="leftLocation"><button class="replaySubmit">提交</button></div></div>'
                        if (commentContainer.attr('me')) {
                            commentContainer = commentContainer.children('.replayArea')
                            commentContainer.after(commentDom)
                        } else {
                            commentContainer.prepend(commentDom)
                        }

                    }
                })
        }
        const ATTITUDE_FAVOR  = 0
        const ATTITUDE_OPPOSE = 1
        const ON_ATTITUDE  = 1;
        const OFF_ATTITUDE = -1;

        function doAttitude(direction, attitude, button) {
            datas = window.location.pathname.split('/')
            var articleId_Rex = new RegExp(/\d+/g)
            //console.log(articleId_Rex.exec(datas[2])[0])
            $.ajax({
                url:"/userAttitleTheArticle/",
                type: 'post',
                data:{"surfix":datas[1], "articleId":articleId_Rex.exec(datas[2])[0],"direction":direction, "attitude":attitude},
                success:function (arg) {
                    if ("success" == arg) {
                        if(ON_ATTITUDE == direction && ATTITUDE_FAVOR == attitude) {
                            button.addClass("theUserAttitude")
                            console.log("点赞成功")
                        } else if (OFF_ATTITUDE == direction && ATTITUDE_FAVOR == attitude) {
                            button.removeClass("theUserAttitude")
                            console.log("去赞成功")
                        } else if (ON_ATTITUDE == direction && ATTITUDE_OPPOSE == attitude) {
                            button.addClass("theUserAttitude")
                            console.log("踩成功")
                        } else {
                            button.removeClass("theUserAttitude")
                            console.log("去踩成功")
                        }
                    } else if("failed" == arg) {
                        console.log("操作数据库失败")
                    }
                },
                error:function () {
                    console.log("发送Ajax请求失败")
                }
            })
        }
        $(document).ready(function () {
            csrftokenInAjax()
            $("#favorButton").click(function () {
                var direction = ON_ATTITUDE
                if ($(this).hasClass("theUserAttitude")) {
                    direction = OFF_ATTITUDE
                }
                doAttitude(direction, ATTITUDE_FAVOR, $(this))
            })
           $("#opposeButton").click(function () {
                var direction = ON_ATTITUDE
                if ($(this).hasClass("theUserAttitude")) {
                    direction = OFF_ATTITUDE
                }
                doAttitude(direction, ATTITUDE_OPPOSE, $(this))
            })
           $(".replayButton").on('click', function(){
               console.log($(this))
           })
           initKindEditor();
            $("#submitCommentOfTheArticle").on('click', function() {
                submitCommentToTheArticle($('#commentsTrees').attr('article'), theKindEditor.html(), $('#commentsTrees'))
            })
            $("#commentsTrees").on('click', '.replaySubmit',function() {
                submitCommentToTheArticle($(this).parents('.theComment').attr('article'), $(this).parent().siblings('textarea').val(), $(this).parents('.theComment'))
            })
        })
