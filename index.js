let choice =document.getElementById('choice');
let widget = document.querySelector('.widget');
let body = document.getElementById('body');
let content = document.getElementById('content');
let tables = document.getElementsByTagName('table')
let temp = 1;
widget.addEventListener('click',function(){
if(temp==1){
    choice.className = 'dark';
    temp=0;
    widget.style.border= '2px solid rgb(11, 243, 81)';
    body.style.backgroundColor= 'rgb(7, 7, 29)';
    body.style.color = 'white';
    content.className = 'shadow-sm p-3 mt-1 bg-dark rounded mx-auto'
    for (let i = 0; i < tables.length; i ++) {
        tables[i].className = 'table table-dark table-hover text-center align-middle'
    }
}else{
    choice.className = 'light';
    temp=1;
    widget.style.border= '2px solid black';
    body.style.backgroundColor= 'white';
    body.style.color = 'black';
    content.className = 'shadow-sm p-3 mt-1 bg-body rounded mx-auto'
    for (let i = 0; i < tables.length; i ++) {
        tables[i].className = 'table table-hover text-center align-middle'
    }
}
})