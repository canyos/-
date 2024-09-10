function item(name,src,ex,price) {
    this.name=name;
    this.src=src;
    this.ex=ex;
    this.price = price;
}//제품의 정보를 저장할 구조체

var tops=[];
var bottoms=[];
var shoesList=[];
var outers=[];
var items=[tops,bottoms,shoesList,outers];

var list = ["top","bottom","shoes","outer"]
function init(){//제품정보를 읽어 배열에 넣어주는 함수
    for(var j=0;j<4;j++){
        for(var i=1;i<=3;i++){
            items[j].push(new item(list[j]+i.toString(),"./img/"+list[j]+i.toString()+".jpg",list[j]+i.toString(),i));
        }
    }
}

function display(i){ //project.html에 제품을 표시해주는 함수
    for(var j=0;j<items[i].length;j++){

        document.write("<div class = 'item'>");
        document.write("<a href ="+items[i][j].name+".html>");
        document.write("<img class = 'itemImg' src="+items[i][j].src+">");
        document.write("<p>"+items[i][j].name+"</p>");
        document.write("</a>");
        document.write("</div>");

    }
}

var selected=[];
function makeTable(){ //장바구니에서 담은 아이템들을 table로 표시
    let keys  = Object.keys(localStorage);
    for(let key of keys){
        for(var j=0;j<items.length;j++){
            for(var i=0;i<items[j].length;i++){
                if(items[j][i].name == key){
                    selected.push(items[j][i]);
                }
            }
        }
    }
    for(var i=0;i<selected.length;i++){
        document.write("<tr>");
        document.write("<td><input type = 'checkbox' name = 'basket' id="+selected[i].name+"check></input></td>");
        document.write("<td><img width = 100px height= 100px src="+selected[i].src+">"+selected[i].name+"</td>");
        document.write("<td><input id="+selected[i].name+" type = 'number'></td>");
        document.write("</tr>");
    }
}
var count =0;
var price =0;
function cal(){ //장바구니에서 선택한 제품 가격을 계산 및 출력
    price=0;
    for(var i=0;i<selected.length;i++){
        if(document.getElementById(selected[i].name+"check").checked){
            if(document.getElementById(selected[i].name).value<0){ //음수입력에러핸들링
                alert("음수를 입력하지마세요.");
                break;
            }
            price+=selected[i].price*document.getElementById(selected[i].name).value;
            count++;
        }
            
    }
    document.getElementById("price").innerHTML = price;
}
function order(){//상품없이 주문했을때 에러핸들링
    if(document.getElementById("price").innerHTML==""||document.getElementById("price").innerHTML==0)
        alert("주문을 확인해주세요");
    else{
        alert("주문되었습니다");
        localStorage.clear();
    }
    
}

function select(){ //상세페이지에서 제품을 선택하였을때 저장하는 함수
    alert("장바구니에 담았습니다!");
    init();
    var name = document.getElementById('itemName').innerHTML;

    for(var j=0;j<items.length;j++){
        for(var i=0;i<items[j].length;i++){
            if(items[j][i].name == name){
                localStorage.setItem(items[j][i].name,items[j][i].name);
            }
        }
    }
}