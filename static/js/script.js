
setInterval(untilChristmas, 1000);
function untilChristmas(){
	let now = new Date();
	let year = now.getFullYear();
	let christmas = new Date(year, 11, 24);

	let until_chr = christmas - now;
	if( until_chr < 0 ){
		document.getElementById("until_chr").innerHTML = "Hey! <br> It's Christmas time!";
	}else{
		const days = Math.floor(until_chr / (24*60*60*1000));
		const daysuntil_chr = until_chr % (24*60*60*1000);
		const hours = Math.floor(daysuntil_chr / (60*60*1000));
		const hoursuntil_chr = until_chr % (60*60*1000);
		const minutes = Math.floor(hoursuntil_chr / (60*1000));
		const minutesuntil_chr = until_chr % (60*1000);
		const sec = Math.floor(minutesuntil_chr / 1000);
		
		let day = "day";
		let hour = "hour";
		let minute = "minute";
		let secs = "second";
		
		if(days > 1){
			day += "s";
		}
		if(hours > 1){
			hour += "s";
		}
		if(minutes > 1){
			minute += "s";
		}if(sec > 1){
			secs += "s";
		}
		document.getElementById("until_chr").innerHTML = `It's only ${days} ${day}, ${hours} ${hour}, ${minutes} ${minute}  and ${sec} ${secs} until Christmas!`;	
	}
}
