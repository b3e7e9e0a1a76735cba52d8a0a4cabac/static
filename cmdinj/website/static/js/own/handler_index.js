function getHex() {
    let value = document.getElementById('digit').value;
    if (value == '') {  document.getElementById('output').innerHTML = 'Введите десятичное число'; return; }
    $.ajax({
        type : 'GET',
        url: "/api/hex?value=" + value,
        success: function(data){
            document.getElementById('output').innerHTML = "Пожалуйста, подождите, запрос обрабатывается";
            setTimeout(() => { document.getElementById('output').innerHTML = data; }, 3000);

        }
    });
}

document.getElementById('submitButton').addEventListener("click", getHex);