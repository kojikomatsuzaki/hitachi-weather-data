# 2000年4月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2000/04.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 153 | 567 | `source_blank`: 567 |
| `station_pressure_hpa` | 720 | 720 | 0 | — |
| `sea_level_pressure_hpa` | 720 | 720 | 0 | — |
| `global_solar_radiation_mj_m2` | 510 | 510 | 0 | — |
| `sunshine_duration_h` | 510 | 510 | 0 | — |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 720 | 0 | — |
| `dew_point_temperature_c` | 720 | 720 | 0 | — |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `693e2d507f0980a2b4a2d9a59a9b45f6402ef7971e624a9c52262203a417c32c` | verified |
| `humidity` | `humidity.xls` | `4c3e8924ff0b98afbd6b1777d1114ab664a5006cf562deb65d0ebf19130e175a` | verified |
| `precipitation` | `precipitation.xls` | `f160b7f4960c7643a22132265cbb3f41963537a191781b1f78daa44c90ae21ac` | verified |
| `pressure` | `pressure.xls` | `defefeb4ec929fc7d6e77dacfb222266e99168688b563e49def55f9deaf8df63` | verified |
| `solar_radiation` | `solar_radiation.xls` | `2edfefe35f8e72eda7f58b70334703aa8401d5815800ecb4be2e0d9c81f26e20` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `a338538cc3779d955790cd812bfe6259933b4278e2bf18ff7357882a0bb1cef3` | verified |
| `wind_speed` | `wind_speed.xls` | `5415cec686420caed36bf13e3621a4f7baf08a35c3de0d6fa5a17014685d4cd7` | verified |
| `wind_direction` | `wind_direction.xls` | `993583fe42afa01c08f28a2dadca0b187bbcc2e237eed1d4218c30cf1d60c3b9` | verified |
| `dew_point_temperature` | `dew_point.xls` | `3a2e4e22f9023c2473b60688677eda37755746262bf6b602aefc7955b3e8372d` | verified |
| `weather_code` | `weather.xls` | `b83460f4494f5538eb91b47af5dd5947aabaecea98cf046e3e47fda35e4035ab` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2000-04-01 1時 | 8.9 | 82.3 | 996.7 | 1004.0 | 2.4 | WNW | 6.1 | — |
| 2000-04-01 12時 | 14.1 | 24.7 | 1004.0 | 1011.2 | 4.5 | NNW | -5.8 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。

## 2000年問題に関する確認

- 日付は2000年として明示的に構成し、1900年への誤認がないことを確認した。
