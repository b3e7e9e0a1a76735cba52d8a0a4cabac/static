function search() {
    let keyword = document.getElementById('keyword').value;

    $.ajax({
        type : 'GET',
        url: "/search?q=" + keyword,
        success: function(data){
            $('body').html(data);
        }
    });
}

document.getElementById('search').addEventListener("click", search);