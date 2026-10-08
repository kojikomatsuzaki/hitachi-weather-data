# 2019年9月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2019/09.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 138 | 582 | `source_blank`: 582 |
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
| 2019-09-01 1時 | 23.5 | 77.3 | 1007.9 | 1014.3 | 0.7 | NNW | 19.3 | — |
| 2019-09-01 12時 | 28.3 | 55.6 | 1011.0 | 1017.3 | 1.0 | SSE | 18.6 | 3 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
