var swap_song = function(img){
    if (img.src.includes('heart_full.png')) {
        $.ajax({
            url: '/unlike_song',
            data: {'id':img.name},
            type: 'POST',
                dataType: 'json',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
        img.src = '../static/heart.png'
        document.getElementById("num_likes"+img.name).innerHTML = parseInt(document.getElementById("num_likes"+img.name).innerHTML) - 1;

    }else{
        $.ajax({
            url: '/like_song',
            data: {'id':img.name},
            type: 'POST',
                dataType: 'json',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
        img.src = '../static/heart_full.png';
        document.getElementById("num_likes"+img.name).innerHTML = parseInt(document.getElementById("num_likes"+img.name).innerHTML) + 1;

    };
}

var swap_sugg = function(img){
    if (img.src.includes('heart_full.png')) {
        $.ajax({
            url: '/unlike_sugg',
            data: {'id':img.name},
            type: 'POST',
                dataType: 'json',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
        img.src = '../static/heart.png'
        document.getElementById("num_likes"+img.name).innerHTML = parseInt(document.getElementById("num_likes"+img.name).innerHTML) - 1;
    }else{
        $.ajax({
            url: '/like_sugg',
            data: {'id':img.name},
            type: 'POST',
                dataType: 'json',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
        img.src = '../static/heart_full.png';
        document.getElementById("num_likes"+img.name).innerHTML = parseInt(document.getElementById("num_likes"+img.name).innerHTML) + 1;

    };
}
function log_in_err(){
    alert("Log in to like songs or suggestions");
}