function change(secs, song){
	document.getElementById('song_duration').style.width = String(Math.round((secs/song[0]['song_duration_secs'])*100)) + '%';
	//for the playlist page - just thought that adding a new call could be more inefficient than just checking it it exists
	try {
		document.getElementById('currsong_name_bar').innerHTML = song[0]['song_name'];
		document.getElementById('currsong_img_bar').src = "static/" + song[0]['song_img_path'];
		document.getElementById('active_song_duration').style.width = String(Math.round((secs/song[0]['song_duration_secs'])*100)) + '%';
		document.getElementById('curr_time_song').innerHTML = `${Math.floor(secs/60)}:${secs%60 > 9 ? secs%60 : '0' + String(secs%60)}`;
		// console.log(song[0]['id']);
		// console.log(document.getElementsByClassName('active'));
		var lactive = document.querySelectorAll('.active');
		// console.log(lactive);
		lactive.forEach(element => {
			console.log(element);
			if(element.nodeName == "BUTTON" && element != document.getElementById(String(song[0]['id']))){
				element.classList.remove("active");
				element.childNodes[2].classList.replace("author-active", "author");
				return;
			}

		});
		document.getElementById(String(song[0]['id'])).classList.add('active');
		document.getElementById(String(song[0]['id'])).childNodes[2].classList.replace("author","author-active");
		
	}
	catch(TypeError){
	}
}
function callme(){
	var networkPromise = fetch('/seconds-full_length')
		.then(response => response.json())
		.then(data => { 
			change(data['secs'], data['song']) });
	var timeOutPromise = new Promise(function(resolve, reject){ setTimeout( resolve, 1000, 'Timeout Done');
	});

	Promise.all(
	[networkPromise, timeOutPromise]).then(function(values) {
		callme();
	});
}
callme();


function change_vol_html(vol){
	document.getElementById('volume').value = vol;
}
function callme_vol(){
	var networkPromise = fetch('/volume')
		.then(response => response.json())
		.then(data => { 
			change_vol_html(data['vol']) });
	var timeOutPromise_vol = new Promise(function(resolve, reject){ setTimeout( resolve, 5000, 'Timeout Done');
	});

	Promise.all(
	[networkPromise, timeOutPromise_vol]).then(function(values) {
		callme_vol();
	});
}
callme_vol();

function change_vol(vol){
	$.ajax({
		url: '/set_vol',
		data: {'vol':vol},
		type: 'POST',
		    dataType: 'json',
		success: function(response){
		    console.log(response);
		},
		error: function(error){
		    console.log(error);
		}
	});
}


