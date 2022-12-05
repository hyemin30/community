//프로필


function save_order1() {
    let name = $('#name').val()
    let blog = $('#blog').val()
    let lang = $('#lang').val()

    $.ajax({
        type: 'POST',
        url: '/profile',
        data: {name_give: name, blog_give: blog, lang_give: lang},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}


//포스트

function posting2() {
    let post = $('#post2').val()

    $.ajax({
        type: 'POST',
        url: '/post',
        data: {post_give: post},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

//리스트

$(document).ready(function () {
    // show_postlist3();
});

function show_postlist3() {
    $.ajax({
        type: "GET",
        url: "/post",
        data: {},
        success: function (response) {
            let rows = response['post']
            for (let i = 0; i < rows.length; i++) {
                let post = rows[i]['post']
                let num = rows[i]['num']
                let done = rows[i]['done']

                let temp_html = ``
                if (done == 0) {
                    temp_html = `<li>
                                            <h2>${post}</h2>
                                            <button onclick="done_bucket3(${num})" type="button" class="btn btn-outline-primary">읽음!</button>
                                        </li>`
                } else {
                    temp_html = `<li>
                                        <h2 class="done">${post}</h2>
                                        </li>`
                }
                $('#post-list3').append(temp_html)
            }
        }
    });
}

function done_bucket3(num) {
    $.ajax({
        type: "POST",
        url: "/post/done",
        data: {num_give: num},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}
