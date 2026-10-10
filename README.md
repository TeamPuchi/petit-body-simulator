# Petit Body Simulator

ぷちの体（M5Stack CoreS3、`m5_petit_cloud` ファーム）の画面と、タップ・なぞる・長押しの動きをブラウザで試すもの。
実機を持っていない人が、設定モード・クイックパネル・「ぷちに おねがい」・設定ページ（スマホ側）の流れを確認するために。

- 公開ページ: https://teampuchi.github.io/petit-body-simulator/
- もとのファーム: https://github.com/TeamPuchi/m5-petit-firmware （`firmware/m5_petit_cloud/`）

## できること

- 起動 → 長押し → 設定モード（QR）→ スマホの設定ページ（メイン／ぷちのコア設定）→ 保存して再起動／保存せずに戻る
- いつもの顔: タップで見る、横になぞるとハート、連打でまばたき
- 下端から上へ: おと・ひかり・ながもち → いま だれ → ぷちに おねがい → 顔（一周）。上端から下へ: おねがいへ直行
- クラウドからの cmd（look / blink / icon / color / sleep / wake / snapshot / sensors / volume / brightness / people）と、センサーの出来事
- 体がクラウドへ送る event のログ

数値（しきい値・座標・時間）はファームのコードから写しています。設定ページの HTML は `build.py` がファームの `provisioning.cpp` から取り出して埋め込みます。

## 更新のしかた

```
python3 build.py <m5-petit-firmware>/firmware/m5_petit_cloud [sleep.jpg]
```

`template.html` が本体、`index.html` が生成物（GitHub Pages が配るもの）。ファームを直したら build し直してコミットします。

## 実機との違い

- 字体は Google Fonts の丸ゴシックで代用（実機は lgfxJapanGothic 12 / 24 / 40）
- 音は鳴りません
- QR の中身は見本。実機では機体ごとの SoftAP の名前が入ります
