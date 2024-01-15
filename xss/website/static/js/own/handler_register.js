function register() {
    let inputFirstName = document.getElementById('inputFirstName').value;
    let inputLastName = document.getElementById('inputLastName').value;
    let inputEmail = document.getElementById('inputEmail').value;
    let inputPassword = document.getElementById('inputPassword').value;
    let inputPasswordConfirm = document.getElementById('inputPasswordConfirm').value;

    if (inputEmail == '' || (inputPassword != inputPasswordConfirm)) { alert('Проверьте корректность введенных вами данных!'); return; }

    $.ajax({
        type : 'POST',
        url: "/register",
        contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
        data: { inputFirstName: inputFirstName, inputLastName: inputLastName, inputEmail: inputEmail, inputPassword: inputPassword },
        success: function(data){
            if (data == '1') {
                if (confirm("Вы успешно зарегистрировались. Перейти на страницу для входа?")) { window.location.href = '/login'; }
            }
            else if (data == '2') alert('Пользователь с таким email уже существует!');
            else alert('Произошла ошибка на стороне сервера, повторите позже');
        }
    });
}

document.getElementById('register').addEventListener("click", register);