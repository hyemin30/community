

// 회원가입
function check_sign(){
    let emailVal = $('#input-email').val();
    let pwVal = $('#input-pw').val();
    let nicknameVal = $('#input-nickname').val();
    let langVal = $('#input-lang').val();
    let blogVal = $('#input-blog').val();
    
    $.ajax({
        type: "POST",
        url: "/sign",
        data: {email_give: emailVal, pw_give: pwVal, nick_give: nicknameVal, lang_give: langVal, blog_give: blogVal},
        success: function(response){
        console.log(response);
        }
    })
}


// 로그인
function check_login(){
    let loginEmailVal = $('#login-email').val();
    let loginPwVal = $('#login-pw').val();
    $.ajax({
        type: "POST",
        url: "/login",
        data: {loginEmail_give: loginEmailVal, loginPw_give: loginPwVal},
        success: function(response){
        console.log(response);
        }
    })
}


//프로필
    $(document).ready(function () {
    show_profile();
    });

    function show_profile(){
    $.ajax({
        type: 'GET',
        url: '/profile',
        data: {},
        success: function (response) {
            let rows = response['profile']
            for (let i = 0; i < rows.length; i++){
                let nickname = rows[i]['name']
                let language = rows[i]['lang']
                let blog = rows[i]['blog_url']

                let temp_html =`
                                <tr>
                                    <td>${nickname}</td>
                                    <td>${language}</td>
                                    <td>${blog}</td>
                                </tr>
                `
                $('#profile_list').append(temp_html)
            }
        }
    });
}


function save_posting() {
    let post = $('#post').val()

    $.ajax({
        type: 'POST',
        url: '/posting',
        data: {content_give: post},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

//리스트

$(document).ready(function () {
    show_postlist();
});

function show_postlist() {
    $.ajax({
        type: "GET",
        url: "/postings",
        data: {},
        success: function (response) {
            let rows = response['readings']

            for (let i = 0; i < rows.length; i++) {
                let content = rows[i]['content']
                let num = rows[i]['num']
                let read = rows[i]['read']

                let temp_html = ``
                if (done == 0) {
                    temp_html = `<li>
                                   <h2>${post}</h2>
                                   <button onclick="done_posting(${num})" type="button" class="btn btn-outline-primary">읽음!</button>
                                 </li>`
                } else {
                    temp_html = `<li>
                                        <h2 class="done">${post}</h2>
                                        </li>`
                }
                $('#posting-list').append(temp_html)
            }

        }
    });
}

// function done_posting(num) {
//     $.ajax({
//         type: "POST",
//         url: "/post/done",
//         data: {num_give: num},
//         success: function (response) {
//             alert(response["msg"])
//             window.location.reload()
//         }
//     });
// }
