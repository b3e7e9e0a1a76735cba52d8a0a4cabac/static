function login() {
    let inputEmail = document.getElementById('inputEmail').value;
    let inputPassword = document.getElementById('inputPassword').value;

    $.ajax({
        type : 'POST',
        url: "/login",
        contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
        data: { inputEmail: inputEmail, inputPassword: inputPassword },
        success: function(data){
            $('body').html(data);
        }
    });
}

document.getElementById('login').addEventListener("click", login);