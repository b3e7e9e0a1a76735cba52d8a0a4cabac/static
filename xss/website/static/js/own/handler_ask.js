function reset() {
    let inputText = document.getElementById('inputText').value;
    let output = document.getElementById('output');

    $.ajax({
        type : 'GET',
        url: "/ask?text=" + inputText,
        success: function(data){
            $('body').html(data);
        }
    });
}

document.getElementById('reset').addEventListener("click", reset);