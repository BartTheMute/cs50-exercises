document.getElementById("btn-lucky").addEventListener("click", function(){
    var form=document.getElementById('search-form');
    var input = document.createElement('input');
    input.setAttribute('name', "btnI");
    input.setAttribute('value', "I'm Feeling Lucky");
    input.setAttribute('type', "hidden");
    form.appendChild(input);
    form.submit();     
});