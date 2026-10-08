# 2019年1月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2019/01.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 26 | 718 | `source_blank`: 718 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 742 | 2 | `source_dash`: 2 |
| `wind_direction` | 744 | 742 | 2 | `source_dash`: 2 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `7d9f20a5cdf9a39bbfd6f10f2c573f10b26f39068fba0508fcf00c1688c23a56` | verified |
| `humidity` | `humidity.xls` | `23119670d2ea8a55a2d38bfbe3e2c0a2df69b0b84a88c73d45a93e7620fc1f0a` | verified |
| `precipitation` | `precipitation.xls` | `2f70dab4c1b23537d71540afa14e8eb275a023bd77d3fd0a1f6d4682e8cf853d` | verified |
| `pressure` | `pressure.xls` | `d6d2b2439ce736fa05c29c0511b1990fd4f1fb205e247cca6e59d23246db5ea4` | verified |
| `solar_radiation` | `solar_radiation.xls` | `90b2246feac518f9961bd6275ef83efab8a3260c35b47f4e47d32492f8420055` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `15cbaa7451febdf3651239e1d01b68470648b8c96f564d21b13edd2b4653fe85` | verified |
| `wind_speed` | `wind_speed.xls` | `6f8318168784082ce58a42b5a0bd7fc4953f18f48d3b78ae47c17270f11242db` | verified |
| `wind_direction` | `wind_direction.xls` | `121d4d7835e9531d55fbdd292395e48297c91b3f04d6c58b8bf9e188031fd462` | verified |
| `dew_point_temperature` | `dew_point.xls` | `3e5e59091bbc76044057013345022ab9bbaaa55fcd1923536d2cf7b3966fe16d` | verified |
| `weather_code` | `weather.xls` | `aa60fb6c443e2a5665aea3d394fa980582401720002ce45435f187f76591b8d7` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2019-01-01 1時 | 1.2 | 53.0 | 1019.5 | 1026.5 | 2.3 | WNW | -7.2 | — |
| 2019-01-01 12時 | 8.6 | 31.3 | 1015.7 | 1022.5 | 4.3 | SSW | -7.3 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
