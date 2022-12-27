//the check for song_img is in edit.js since there is already a function that handles the preview

function check_song_name(inp){
	inp.addEventListener("keyup", (song_n) => {
	
		let tmp = document.createElement("div");
		tmp.innerHTML = song_n.target.value
		strip_name = tmp.textContent || tmp.innerText || "";

		if (strip_name.length === 0){
			document.getElementById("error_song_name").innerHTML = "Invalid song name";}
		else{
			document.getElementById("error_song_name").innerHTML = "";
		}
	});
}
function check_song_author(inp){
	inp.addEventListener("keyup", (song_a) => {
	
		let tmp = document.createElement("div");
		tmp.innerHTML = song_a.target.value
		strip_auth = tmp.textContent || tmp.innerText || "";

		if (strip_auth.length === 0){
			document.getElementById("error_song_author").innerHTML = "Invalid song author";}
		else{
			document.getElementById("error_song_author").innerHTML = "";
		}
	});
}
function mp3_valid(finp){
	ext = finp.value.slice(-3,);
	if(ext === 'mp3'){
		document.getElementById("error_mp3").innerHTML = "";
	}else{
		document.getElementById("error_mp3").innerHTML = `Invalid song extension: ${ext} - only mp3 is supported`;
	}
}
function txt_valid(finp){
	ext = finp.value.slice(-3,);
	if(ext === 'txt'){
		document.getElementById("error_txt").innerHTML = "";
	}else{
		document.getElementById("error_txt").innerHTML = `Invalid song sequence extension: ${ext} - only txt is supported`;
	}
}
