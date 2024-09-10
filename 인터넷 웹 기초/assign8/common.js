function order() {
    var sum = 0;
    alert("주문해 주셔서 감사합니다!");
    sum+=document.getElementById("jajang").value*5000;
    sum+=document.getElementById("bob").value*6000;
    sum+=document.getElementById("tang").value*10000;
    sum+=document.getElementById("gun").value*5000;

    var addr = document.getElementById("address").value;

    var date = new Date();
    var str = "";
    str+=date.getFullYear();
    str+=". "+(date.getMonth()+1);
    str+=". "+date.getDate()+".";
    document.getElementById("date").innerHTML = str;

    str="";
    if(date.getHours()>12){
        str+="오후 "+(date.getHours()-12);
    }else{
        str+="오전 "+date.getHours();
    }
    str+=":"+date.getMinutes()+":"+date.getSeconds();
    document.getElementById("time").innerHTML=str;

    document.getElementById("destination").innerHTML=addr;
    document.getElementById("price").innerHTML=sum+"원";
    document.getElementById("totalJajang").innerHTML = "자장면 : " + document.getElementById("jajang").value+"개";
    document.getElementById("totalBob").innerHTML = "자장면 : " + document.getElementById("bob").value+"개";
    document.getElementById("totalTang").innerHTML = "자장면 : " + document.getElementById("tang").value+"개";
    document.getElementById("totalGun").innerHTML = "자장면 : " + document.getElementById("gun").value+"개";
}
