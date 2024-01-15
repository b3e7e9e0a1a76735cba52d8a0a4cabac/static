
function getOrder() {
    let id = document.getElementById('order-input').value;
    $.ajax({
        type : 'GET',
        url: "/api/orders?id=" + id,
        //contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
        //data: { payload: value },
        success: function(data){
            document.getElementById('output-text').innerHTML = "Пожалуйста, подождите, запрос обрабатывается";
            setTimeout(() => { document.getElementById('output-text').innerHTML = data; }, 3000);
            //console.log(data);
        }
    });
}

document.getElementById('btn-search').addEventListener("click", getOrder);




