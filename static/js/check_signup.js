function check_uname(name_inp) {
	if (name_inp.value.length < 3){
		document.getElementById('name_succ').innerHTML = '';
		document.getElementById("name_error").innerHTML = 'Name must be at least 3 characters long';
		document.getElementById('sgn_up_btn').setAttribute('disabled', true);
	}else{
		document.getElementById('sgn_up_btn').removeAttribute('disabled');
		document.getElementById("name_error").innerHTML = ''; 
		document.getElementById('name_succ').innerHTML = "Valid";	}
}

function check_pswd(pswd_inp) {
	if (pswd_inp.value.length < 6){
		document.getElementById("pswd_succ").innerHTML = '';
		document.getElementById('sgn_up_btn').setAttribute('disabled', true);
		document.getElementById("pswd_error").innerHTML = 'Password must be at least 6 characters long';
	}else{
		document.getElementById('sgn_up_btn').removeAttribute('disabled');
		document.getElementById("pswd_error").innerHTML = ''; 
		document.getElementById('pswd_succ').innerHTML = "Valid";	
	}
}
function check_pswd_agn(pswd_agn_inp) {
	if (pswd_agn_inp.value != document.getElementById('pswd').value){
		document.getElementById('sgn_up_btn').setAttribute('disabled', true);
		document.getElementById('pswd_agn_succ').innerHTML = '';
		document.getElementById("pswd_agn_error").innerHTML = 'Password do not match';
	}else{
		document.getElementById('sgn_up_btn').removeAttribute('disabled');

		document.getElementById("pswd_agn_error").innerHTML = ''; 
		document.getElementById('pswd_agn_succ').innerHTML = "Passwords match";}
}


