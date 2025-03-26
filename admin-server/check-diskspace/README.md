# check-diskspace
このレポジトリは研究室内のサーバー管理で，各サーバーのdisk spaceを調べて容量が少ない場合に警告を与えるためのテキストを生成するソースコードです．<br>
## 環境構築
```
cd check_disk_space
pip install -r requirements.txt
```
## 使用方法
以下のコマンドを実行することでdisk spaceの調査を行い，警告を与えるためのテキストを生成します．
```
cd check_disk_space
bash run_check.sh
```
セキュリティの問題で，`server_ips`と`username`と`password`は各自で入力して使用してください．<br>
このコマンドの実行により，`./check_log/{実行日時}`のファイルが作成され，その中に，`check_log_{実行日時}_warnings.txt`と`check_log_{実行日時}.log`が保存されます．<br>
`check_log_{実行日時}_warnings.txt`が実際に使用率の警告閾値(default=85%)を超えるサーバーのipアドレスとディレクトリ名が一覧で保存されます．<br>
`check_log_{実行日時}.log`には，各サーバーのdfコマンドの結果が保存されます．<br>

## 警告の与え方の例
生成された`check_log_{実行日時}_warnings.txt`の中身をコピーしてサーバー管理の連絡チャンネルなどに共有するなどして，サーバー利用者に周知することができます．
![check_disk_space](https://github.com/user-attachments/assets/3d685e47-d527-455f-ba29-b397c1dc4bac)
