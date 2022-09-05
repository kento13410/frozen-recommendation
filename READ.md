

CREATE TABLE foodnames(id integer primary key, 食品名 text, カロリー real, タンパク質 real, 脂質 real, 炭水化物 real, 値段 integer, 画像 text, url text);

INSERT INTO foodnames values(10, "5種野菜とひじきの豆腐ハンバーグ", 41, 2.29, 1.8, 3.9, 250,"https://www.maruha-nichiro.co.jp/products/photo/4902165373813_1.png","https://www.maruha-nichiro.co.jp/products/product?j=4902165373813");

ALTER TABLE foodnames ADD COlUMN お気に入り integer;
お気に入り integer