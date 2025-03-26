import os
from datetime import datetime

import paramiko
from tqdm import tqdm

# サーバーのIPアドレスのリスト
server_ips = ["000.000.000.000", 
              "000.000.000.100", 
              ]

username = "username"
password = "password"


# 確認するディレクトリのリスト
check_dir_name_list = ["/", "/data1", "/data2", "/data3", "/data4", "/data5", "/data6", "/raid", "/mnt", "/home"]

# 使用率の警告閾値
warning_threshold_ratio = 85

# 実行日時のフォーマット
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
save_dir = f"check_log/{current_time}"
os.makedirs(save_dir, exist_ok=True)

log_filename = os.path.join(save_dir, f"check_log_{current_time}.log")
warning_filename = os.path.join(save_dir, f"check_log_{current_time}_warnings.txt")

# 警告をまとめるリスト
warnings = []
warnings.append(f"ip: [dir_name] (Use%)")

# 全df出力をまとめるリスト
all_df_outputs = []

for ip in tqdm(server_ips, desc="Connecting to servers"):
    try:
        # SSHクライアントを初期化
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # SSH接続を確立
        client.connect(ip, username=username, password=password)

        # dfコマンドを実行してディスク情報を取得
        stdin, stdout, stderr = client.exec_command("df")
        df_output = stdout.read().decode()

        # サーバーごとのdf出力をまとめる
        all_df_outputs.append(f"Server: {ip}\n{df_output}\n{'-'*40}\n")

        # 各行を解析して、対象ディレクトリの使用率をチェック
        for line in df_output.splitlines():
            parts = line.split()
            if len(parts) < 6:
                continue

            # マウントポイントがチェック対象ディレクトリリストに含まれるかを確認
            dir_name = parts[5]  # マウントポイント
            if dir_name in check_dir_name_list:
                # 使用率を抽出し、パーセントを除去して数値に変換
                used_percent = int(parts[4].replace('%', ''))

                # 使用率が閾値を超えていれば、警告リストに追加
                if used_percent > warning_threshold_ratio:
                    warnings.append(f"{ip}: [{dir_name}] ({used_percent}%)")

        # SSH接続を終了
        client.close()

    except Exception as e:
        print(f"Error connecting to {ip}: {e}")
        all_df_outputs.append(f"Error connecting to {ip}: {e}\n{'-'*40}\n")
    
    finally:
        # 常に接続をクローズ
        client.close()

# df出力をファイルに保存
with open(log_filename, "w") as log_file:
    log_file.writelines(all_df_outputs)

# 警告リストをファイルに保存
if warnings:
    with open(warning_filename, "w") as warning_file:
        warning_file.write("\n".join(warnings))
else:
    with open(warning_filename, "w") as warning_file:
        warning_file.write("すべてのディレクトリが警告閾値以下です。")

print(f"全df出力は {log_filename} に保存されました。")
print(f"警告は {warning_filename} に保存されました。")
