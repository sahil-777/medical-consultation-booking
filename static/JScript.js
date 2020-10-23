


function validate_file(){
	var fileInput= document.getElementById('file');
	//console.log(fileInput);
	//if(fileInput==null)
	//	return true;
	var filetype=fileInput.value;
	var allowedExtensions =/(\.doc|\.docx|\.pdf|\.txt)$/i;
	if(!allowedExtensions.exec(filetype)){
		alert("Please, Choose file in given format");
		filetype='';
		document.getElementById('file').value=null;
		return false;
	}
	//return true;
} 