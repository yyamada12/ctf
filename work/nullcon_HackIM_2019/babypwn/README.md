# ポイント

- 負数の入力でスタックにオーバーフローできる
- canaryが有効だが、 `scanf()` に対しては `"+"` を入力することでメモリのデータはそのままになる性質を利用する
- pwntoolでpltやgotが取得できない
  - got は `readelf -r challenge` で読む
  - pltは `objdump -d -M intel -j .plt.got --no challenge` で読む
    普通は `-j .plt` なところが `-j .plt.got` であるからpwntoolで取得できないのかな？
- スタックに書き込む値は `int` で4バイトずつなため、１つのアドレスを書き込むために2回に分ける必要がある



# 補足



1回目: puts(puts_got) してmainに戻る

| contents         | addr     | payload      |
| ---------------- | -------- | ------------ |
| buf              | rbp-0x60 | "+" x2       |
| ...              |          | … "+" x18    |
| "y"              | rbp-0x10 | "+" x2       |
| stack canary     | rbp-0x8  | "+" x2       |
| original rbp     | rbp      | "+" x2       |
| リターンアドレス | rbp+0x8  | pop rdi; ret |
|                  | rbp+0x10 | puts_got     |
|                  | rbp+0x18 | plt_got      |
|                  | rbp+0x20 | main         |



2回目: 取得したlibcのアドレスでone_gadgetに飛ばす