# 2020年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2020/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 151 | 593 | `source_blank`: 593 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 744 | 0 | — |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `fb917b6327cbb71349e38a9663e64fb43f506cff53333d823f3e9a5fb4a4593d` | verified |
| `humidity` | `humidity.xls` | `50c1030bbb17b99185680933cde3765e1112ecfc833c5e40a00b7ea0f0f65fbe` | verified |
| `precipitation` | `precipitation.xls` | `17585f19db32b583aaed1928558bede1271ea4aa854fc37e10efc89cfa031a47` | verified |
| `pressure` | `pressure.xls` | `28c0f441ac354f8cac99198af1b0dba2965a55df815407ec84cc68e0a1d715f0` | verified |
| `solar_radiation` | `solar_radiation.xls` | `676a67ade32e5d6269c8cce55aa4bc1527ce129879cc23534ea41fee832e3b78` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `a048fac387cf5bb811cac0d6276c58af8e241bccec85fb11f7d5811f69e956ea` | verified |
| `wind_speed` | `wind_speed.xls` | `b5af6f4754104be06ae07a33f33a006f1e66c94f267f7e266962c6b415fb46f7` | verified |
| `wind_direction` | `wind_direction.xls` | `934c94415c99ed4d10e46d75b4263d23a7596d684de55e3e8197e55c59aa0827` | verified |
| `dew_point_temperature` | `dew_point.xls` | `f43f0cec21dc738ab15990ac2987bae56f584bc1d3f1d02c1739c0b1b01fe1dd` | verified |
| `weather_code` | `weather.xls` | `33c950f7fa8df9c1c0ebd495727166313c52550f2cf2236a3bb44a76daf6f3f1` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2020-03-01 1時 | 6.7 | 82.8 | 1008.5 | 1015.3 | 0.7 | NW | 4.0 | — |
| 2020-03-01 12時 | 13.2 | 55.1 | 1008.6 | 1015.2 | 2.1 | SE | 4.4 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
