var step;
var forms = document.querySelectorAll("form");
var allinp = 0;
var p;

function taisyou(){
  p = new Progress(0);
  for(var i = forms.length;i--;){
    var inp = forms[i].querySelectorAll("input[name='username'], input[name='password'], select");
    allinp += inp.length; //プログレスバーの進捗の対象を数える
    for(var j = inp.length;j--;){
      inp[j].setAttribute("onChange","koushin(this)");
    }
  }
  step = 100/allinp;//プログレスバーが一度の進捗で進む％
}

function koushin($this){//入力内容が更新されるたびにプログレスバーの進捗の状態を再計算する
  var elem = $this;
  if($this.value){
    var text = $this.value;
    elem.className = 'up';//入力内容がnullではない場合にクラス名を変更
  }else{
    elem.className = '';
  }
  var nowUp = document.getElementsByClassName('up');//変更したクラス名の数を計算
  var status = allinp - (allinp - nowUp.length);
  p = status*step;
  new Progress(p);//バーに反映させるファンクションを呼び出す
}


var Progress = (function () {
  function Progress (p) {
      this.bar = document.querySelectorAll('#prog-bar > .progress-bar')[0];
      this.p = p;
      this.update();
    };
    Progress.prototype.update = function () {
      this.bar.style.width = this.p + '%';
    };
    return Progress;
}());
