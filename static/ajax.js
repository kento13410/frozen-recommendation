const tabs = document.querySelectorAll(".tabs li a");
const contents = document.querySelectorAll(".contents li");

// この意味が分からん
console.log(tabs);
console.log(contents);

for (let i = 0; i < tabs.length; i++) {
// タブの0個めをクリックしたらコンテンツの0個めが追加される
	tabs[i].addEventListener("click", function(e) {
		// 起こるイベントを削除できる
		e.preventDefault();

		for (let j = 0; j < tabs.length; j++) {
			// タブをクリックしたら全て消す
			tabs[j].classList.remove("active");
		}
		for (let j = 0; j < contents.length; j++) {
			// タブをクリックしたら全て消す
			contents[j].classList.remove("active");
		}

		// thisは今イベントが起こっているものを指す
		this.classList.add("active");
		contents[i].classList.add("active");
	});
}