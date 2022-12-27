var loadFile = function(event, num_id){
	var output = document.getElementById("song_img"+num_id);
	let allowed_ext = ['jpg', 'png','jpeg'];
	if(allowed_ext.includes(event.target.files[0].name.split('.').at(-1))){
		document.getElementById("error_song_img").innerHTML = "";
	}else{
		document.getElementById("error_song_img").innerHTML = `The extension <strong>.${(event.target.files[0].name.split('.').at(-1))}</strong> is invalid. Valid extensions are .png, .jpg, .jpeg`;
	}
	if (output.height > output.width){
		output.style.width = output.height + "px";
	}else{
		output.style.height = output.width+"px";
	}
	output.src = URL.createObjectURL(event.target.files[0]);
	output.onload = function() {
		URL.revokeObjectURL(output.src);
	};
	};

function edit(btn, song_num) {
	btn.firstElementChild.src = btn.firstElementChild.src.includes('edit.png') ? '../static/tick.png' : '../static/edit.png';
	btn.type = "submit";
	btn.removeAttribute("onclick");
	//change the div with id form to an actual form

	var current_div = document.getElementById("form"+song_num);
	var change_form = document.createElement("form");
	change_form.method = "POST";
	change_form.action = "/edit";
	change_form.enctype = "multipart/form-data";
	change_form.innerHTML = current_div.innerHTML;
	current_div.parentNode.replaceChild(change_form, current_div);

	// change img to a button where a new picture can be uploaded
	var current_img = document.getElementById("song_img"+song_num);
	var changable_img = document.createElement("div");
	//changable.setAttribute("onclick", "change_val(this);");
	changable_img.innerHTML = 
		`<input name="id" value="${song_num}" type="hidden">
	<div class="col-12 d-flex" style="position:absolute;">
		<div class="image-upload mx-auto">
			<label for="song_btn${song_num}">
		<img id="song_img${song_num}" class="exp-img mx-auto d-block" src="../static/song_imgs/${song_num}.jpg">
			</label>
			<input accept="image/*" type="file" id="song_btn${song_num}" onchange="loadFile(event,${song_num})" name="song_img">
		</div>

	</div>
	
` ;
	current_img.parentNode.replaceChild(changable_img, current_img);

	
	// change song_name <p> to input div
	var current_name = document.getElementById("song_name"+song_num);
	var changable_name = document.createElement("div");
	//changable.setAttribute("onclick", "change_val(this);");
	changable_name.style = "font-size: 1.5em; margin-bottom: 0";
	changable_name.innerHTML = 
	`<div  class="col-md-7 col-sm-11 mx-auto error">
		<span id="error_song_img" ></span>
	</div>

	<div class="col-md-7 col-sm-11 px-0 mt-2 input-group mx-auto">
		<div class="input-group-prepend">
			<span class="input-group-text" id="inputGroup-sizing-sm">Song Name</span>
		</div>
		<input type="text" class="form-control m-0" aria-label="Small" aria-describedby="inputGroup-sizing-sm" value="${(current_name.innerHTML.trim().slice(current_name.innerHTML.trim().indexOf(">")+1, -4).trim())}" name="song_name" onkeyup="check_song_name(this)">
	</div>
	<div class="col-md-7 col-sm-11 mx-auto px-2 mb-2 text-left error">
		<span id="error_song_name" ></span>
	</div>
		` ;
	current_name.parentNode.replaceChild(changable_name, current_name);
	
	//change author <p> to input div
	

	var current_author = document.getElementById("song_author"+song_num);
	var changable_author = document.createElement("div");
	//changable.setAttribute("onclick", "change_val(this);");
	changable_author.style = "font-size: 1.5em; margin-bottom: 0";
	changable_author.innerHTML = 
	`<div class="col-md-7 col-sm-11 px-0 input-group mx-auto mt-2">
		<div class="input-group-prepend">
			<span class="input-group-text" id="inputGroup-sizing-sm">Song Author</span>
		</div>
		<input type="text" class="form-control m-0" aria-label="Small" aria-describedby="inputGroup-sizing-sm" value="${(current_author.innerHTML.trim().slice(current_author.innerHTML.trim().indexOf(">")+1, -7).trim())}" name="song_author" onkeyup="check_song_author(this)">
	</div>
	<div class="col-md-7 col-sm-11 mx-auto px-2 mb-2 text-left error">
		<span id="error_song_author"  ></span>
	</div>
` ;
	current_author.parentNode.replaceChild(changable_author, current_author);

	//change the duration div into a file form that can be used to replace the mp3 song or a txt sequence
	

	var current_file_div = document.getElementById("song_files"+song_num);
	var changable_file_div = document.createElement("div");
	changable_file_div.classList.add("col-12");
	changable_file_div.classList.add("text-center");
	//changable.setAttribute("onclick", "change_val(this);");
	changable_file_div.innerHTML = 
`<div class="row">
	<div class="col-md-7 col-sm-11 mx-auto mb-0 px-0 mt-2">
		<div class="mb-3">
			<label for="mp3" class="form-label">New MP3 song file</label>
			<input class="form-control" type="file" id="mp3" name="mp3_song" onchange="mp3_valid(this)">
		</div>
	</div>
	<div class="col-md-7 col-sm-11 mx-auto px-2 mb-2 text-left error">
		<span id="error_mp3"  ></span>
	</div>

</div>
<div class="row">
	<div class="col-md-7 col-sm-11 px-0  mx-auto">
		<div class="mb-3">
			<label for="formFile" class="form-label">New TXT song sequence</label>
			<input class="form-control" type="file" id="formFile" name="txt_sequence" onchange="txt_valid(this)">
		</div>
	</div>
	<div  class="col-md-7 col-sm-11 mx-auto px-0 text-left error">
		<span id="error_txt"  ></span>
	</div>

</div>` ;
	current_file_div.parentNode.replaceChild(changable_file_div, current_file_div);
}


