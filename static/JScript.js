


function validate_file(){
	var fileInput= document.getElementById('file');
 
	var filetype=fileInput.value;
 
	var allowedExtensions =/(\.doc|\.docx|\.pdf|\.txt)$/i;
	if(!allowedExtensions.exec(filetype) && filetype!=''){
		alert("Please, Choose file in given format");
		filetype='';
		document.getElementById('file').value=null;
		return false;
	}
	else
		return true;

 
} 