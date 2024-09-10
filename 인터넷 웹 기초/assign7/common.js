function idAndPass(id,pass){
    this.id = id;
    this.pass = pass;
}
var List = [new idAndPass("kim","123"), new idAndPass("lee","456"), new idAndPass("park","789")];

function getLogin() {
    var isin=0;
    var inputID = document.getElementById("id").value;
    var inputPass = document.getElementById("password").value;
    for(var i=0;i<3;i++){
        if(inputID==List[i].id){
            if(inputPass==List[i].pass){
                isin=1;
                alert("Hello! 201924548 이풍헌!");
                location.replace('welcome.html');
                return;
            }else{
                isin=1;
                alert("wrong password!");
                return;
            }
        }
    }
    alert("check your id again!");
}

