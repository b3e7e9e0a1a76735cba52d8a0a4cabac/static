function sendTicket() {
    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;
    let subject = document.getElementById('subject').value;
    let text = document.getElementById('textarea').value;

    if (name == '' || email == '') { document.getElementById('output-text-contact').innerHTML = 'Заполните поле с именем и почтой'; return; }

    $.ajax({
        type : 'POST',
        url: "/api/ticket",
        contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
        data: { name: name, email: email, subject: subject, text: text },
        success: function(data){
            document.getElementById('output-text-contact').innerHTML = "Отправка...";
            setTimeout(() => { document.getElementById('output-text-contact').innerHTML = data; }, 1500);
        }
    });
}

function getTicket() {
    let id = document.getElementById('ticket-input').value;
    $.ajax({
        type : 'GET',
        url: "/api/ticket?id=" + id,
        success: function(data){
            document.getElementById('output-text-ticket').innerHTML = "Пожалуйста, подождите, запрос обрабатывается";
            setTimeout(() => { document.getElementById('output-text-ticket').innerHTML = data; }, 3000);

        }
    });
}

document.getElementById('btn-send').addEventListener("click", sendTicket);
document.getElementById('btn-ticket').addEventListener("click", getTicket);