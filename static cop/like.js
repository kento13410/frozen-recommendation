// HTMLノード変数の生成
window.addEventListener("load",()=>{
    checkbox1 = document.getElementById("checkbox1");
    heart1 = document.getElementById("heart1");
    checkbox2 = document.getElementById("checkbox2");
    heart2 = document.getElementById("heart2");

})
// いいねイベント
checkbox1.addEventListener("click",()=>{
    if (heart1.style.color ==='red'){
        heart1.style.color = 'aliceblue';
    }
    else{
        heart1.style.color = 'red';
    }
});

checkbox2.addEventListener("click",()=>{
    if (heart2.style.color ==='red'){
        heart2.style.color = 'aliceblue';
    }
    else{
        heart2.style.color = 'red';
    }
    });
