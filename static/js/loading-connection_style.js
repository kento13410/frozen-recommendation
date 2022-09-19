function loaded() {
    // loading画面を消す(activeを消す)
    document.getElementById("loading").classList.remove("active");
}

// 画面に対して読み込んだ後のイベントを追加する…
window.addEventListener("load", function() {
    // ローディング画面の実行時間を設定(0.5s)
    setTimeout(loaded, 2000)
})

// 最大でも5秒後に消える
setTimeout(loaded, 5000)
