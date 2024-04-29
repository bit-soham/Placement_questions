document.addEventListener('DOMContentLoaded', function(){
    document.getElementById('menu-icon').addEventListener('click', function() {
        this.classList.toggle('open');
        sidebar = document.querySelector('.side-bar');
        sidebar.classList.toggle('open');
    });
});


function displayFileName() {
    var input = document.querySelector(".Cform_logo");
    var fileNameDisplay = document.getElementById('file-label');
    
    if (input.files && input.files[0]){
        //var reader = new FileReader();
        //reader.onload = function(e){
            //    document.querySelector(".custom-file-input label").textContent = e.target.result;
            //}
            //reader.readAsDataURL(input.files[0]);
            
            fileNameDisplay.textContent = input.files[0].name;
            fileNameDisplay.style.opacity = 1;
        }
        else{
            fileNameDisplay.textContent = "Click here to Choose File";
            fileNameDisplay.style.opacity = 0.5;
        }
        // Add event listener for when a file is selected
    }
    
    
    function displayImageName(){
        var input = document.querySelector(".Qform_image");
        var fileNameDisplay = document.getElementById('file-label');
        
        if (input.files && input.files[0]){
            //var reader = new FileReader();
        //reader.onload = function(e){
            //    document.querySelector(".custom-file-input label").textContent = e.target.result;
            //}
            //reader.readAsDataURL(input.files[0]);
            
        fileNameDisplay.textContent = input.files[0].name;
        fileNameDisplay.style.opacity = 1;
    }
    else{
        fileNameDisplay.textContent = "Click here to Choose File";
        fileNameDisplay.style.opacity = 0.5;
    }
    // Add event listener for when a file is selected
}
