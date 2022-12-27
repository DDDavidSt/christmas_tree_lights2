function edit_check_uname(name_inp) {
	if (name_inp.value.length < 3){
		document.getElementById('edit_name_succ').innerHTML = '';
		document.getElementById("edit_name_error").innerHTML = 'Name must be at least 3 characters long';
		document.getElementById('edit_prof').setAttribute('disabled', true);
	}else{
		document.getElementById('edit_prof').removeAttribute('disabled');
		document.getElementById("edit_name_error").innerHTML = ''; 
		document.getElementById('edit_name_succ').innerHTML = "Valid";	}
}

function edit_check_newpswd(pswd_inp) {
	if (pswd_inp.value.length < 6){
		document.getElementById("edit_newpswd_succ").innerHTML = '';
		document.getElementById('edit_prof').setAttribute('disabled', true);
		document.getElementById("edit_newpswd_error").innerHTML = 'Password must be at least 6 characters long';
	}else{
		document.getElementById('edit_prof').removeAttribute('disabled');
		document.getElementById("edit_newpswd_error").innerHTML = ''; 
		document.getElementById('edit_newpswd_succ').innerHTML = "Valid";	
	}
}
function edit_check_newpswd_agn(pswd_agn_inp) {
	if (pswd_agn_inp.value != document.getElementById('nw_pswd').value){
		document.getElementById('edit_prof').setAttribute('disabled', true);
		document.getElementById('edit_newpswdagn_succ').innerHTML = '';
		document.getElementById("edit_newpswdagn_error").innerHTML = 'Password do not match';
	}else{
		document.getElementById('edit_prof').removeAttribute('disabled');

		document.getElementById("edit_newpswdagn_error").innerHTML = ''; 
		document.getElementById('edit_newpswdagn_succ').innerHTML = "Passwords match";}
}

function close_form(){
	var form_now = document.getElementById("form_div");
	var new_div = document.createElement("div");
	new_div.id = "form";
	new_div.innerHTML = `
	<div class="col-12 d-sm-flex text-left">
		<img id="prof_img" src="${(document.getElementById("prof_img").src)}" width=100px height=100px class="self-align-center">
		<div class="pl-4 pt-3">
			<h3 style="padding:0.2em 0.5em; margin: 0 0.5em" > Username:</h3>
			<h2 style="padding: 0em 0.5em; margin: 0 0.5em;">
				<span style='color:#a8dadc' id="usrname">${(document.getElementById('sess_name').innerHTML)}</span>
				<div class="alert alert-danger ml-sm-3" id="edit_name_error"></div>
				<div class="alert alert-success ml-sm-3" id="edit_name_succ"></div>
			</h2>
		
			<h3 style="padding: 0.2em 0.5em; margin: 0 0.5em;" > Admin rights:</h3><h4 style=' padding: 0em 0.5em; margin: 0.2em 1.5em;'> <em>${ (sess_admin) != 'None' ? 'all admin rights' : 'no admin rights'}</em></h4>
			<div id="chng_pswd" class="pr-3 pl-0">
			</div>
		</div>	
	</div>
	
	<div class="col-12 pt-3 d-flex">
		<button class="btn btn-lg btn-outline-light" id="edit_prof" onclick="edit_profile(this);">Edit profile </button>
		<div id="cls" class="pl-3">
		</div>
	</div>
	`;
	form_div.parentNode.replaceChild(new_div, form_div);
};
function edit_profile(btn) {

	// changing current Edit button
	btn.removeAttribute('onclick');
	btn.type = "submit";
	btn.innerHTML = "Edit!";
	btn.style.backgroundColor = '#457b9d';
	
	//changing the div into a form
	var form = document.createElement('form');
	var div_form = document.getElementById('form');
	form.innerHTML = div_form.innerHTML;
	form.method = "POST";
	form.id = "form_div";
	form.enctype = "multipart/form-data";
	form.action = "/chng_account";
	div_form.parentNode.replaceChild(form, div_form);	
	

	usr_name = document.getElementById('sess_name').innerHTML;

	var dv_uname = document.getElementById('usrname')
	var nw_uname = document.createElement("div")
	nw_uname.classList.add('d-sm-flex');
	nw_uname.innerHTML = `
	<div class="d-flex justify-content-center">
		<label for="usr_name"></label>
	<input name='usr_name' id='usrname' value='${usr_name}' class="form-control align-self-center ml-sm-3 my-auto" style="background: transparent; color: #a8dadc;" onkeyup="edit_check_uname(this)"></input>
	</div>
	
`;
	dv_uname.parentNode.replaceChild(nw_uname, dv_uname);

	document.getElementById('chng_pswd').innerHTML = ` 
		<button type="button" class="btn btn-lg btn-outline-light" onclick="change_pswd(this);"> Change password </button>`;

	//creating a close button
	document.getElementById("cls").innerHTML = `
		<button type="button" class="btn btn-lg btn-outline-light" onclick="close_form();" style="background-color:#e63946"> Close</button>
	`;
}

function change_pswd(btn) {
	
	var nw_inpts = document.getElementById('chng_pswd').innerHTML = `<div class="d-flex justify-content-center pb-2" style="padding:0.2em 0.5em; margin: 0 0.5em">

	<label for="old_pswd"></label>
	<input class="form-control align-self-center ml-sm-3 my-0" id="old_pswd" name="old_pswd" type="password" placeholder="Old password"></input>
</div>
<div class="d-flex justify-content-center pb-2" style="padding:0.2em 0.5em; margin: 0.3em 0.5em">
	<label for="new_pswd"></label>
	<input class="form-control align-self-center ml-sm-3 my-0" id="nw_pswd" name="new_pswd" type="password" placeholder="New password" onkeyup="edit_check_newpswd(this)"></input>
</div>
<div class="alert alert-danger ed_psw"  id="edit_newpswd_error"></div>
<div class="alert alert-success ed_psw mb-md-1" id="edit_newpswd_succ"  ></div>

<div class="d-flex justify-content-center pb-2" style="padding:0.2em 0.5em; margin: 0.3em 0.5em">
	<label for="new_pswd_agn"></label>
	<input class="form-control align-self-center ml-sm-3 my-0" id="nw_pswd_agn" name="new_pswd_agn" type="password" placeholder="New password again" onkeyup="edit_check_newpswd_agn(this)"></input>
</div>
<div class="alert alert-danger ed_psw mt-md-1"   id="edit_newpswdagn_error"></div>
<div class="alert alert-success ed_psw" id="edit_newpswdagn_succ"></div>
`;


}

