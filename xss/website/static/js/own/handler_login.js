function login() {
    let inputEmail = document.getElementById('inputEmail').value;
    let inputPassword = document.getElementById('inputPassword').value;

    $.ajax({
        type : 'POST',
        url: "/login",
        contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
        data: { inputEmail: inputEmail, inputPassword: inputPassword },
        success: function(data){
            if (data == '1') {
                window.location.href = '/';
            }
            else alert('Неверный логин или пароль!');
        }
    });
}

document.getElementById('login').addEventListener("click", login);