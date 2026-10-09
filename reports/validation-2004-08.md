# 2004年8月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2004/08.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 117 | 627 | `source_blank`: 627 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 743 | 1 | `source_dash`: 1 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `0aef2d330881e36e093f673d5442eacda7f8f677f4a88aa417ff9a997b4dd7f2` | verified |
| `humidity` | `humidity.xls` | `9c52b79fc0f0f1568e68db85f5865d4b20c4c06e9047b993a06d2fcc1a5be696` | verified |
| `precipitation` | `precipitation.xls` | `5803e7d24cb7fdac694810c66502f5284828f1b79b9f0fb59ec7f239ada7d7bf` | verified |
| `pressure` | `pressure.xls` | `1f3901a42a97e2f378403e5a6f2b7d83a5c9e1370be65e4d697671434c225abc` | verified |
| `solar_radiation` | `solar_radiation.xls` | `f1af598fe4c78f08a7e2f786c135c790be69e6887865bd079892d34d1f191742` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `6c7a6fec0ab36e86127cb19700fa0eaa948afc04545a40f114a4d4acf523c1c0` | verified |
| `wind_speed` | `wind_speed.xls` | `652fcca61e5d72efecb1f0924bd949ec30d1a08054d4e48322177c760b1336b1` | verified |
| `wind_direction` | `wind_direction.xls` | `79433a8af9e80a04ba2a708c7c721b5a87d5ac1aa333084f1eebc83aecfb0a8e` | verified |
| `dew_point_temperature` | `dew_point.xls` | `88e68870b9204c9ec411b9e1d79aa426ebd30e3a6bd18400623d351264c1002c` | verified |
| `weather_code` | `weather.xls` | `f26d6adc42f979c12dda8c77a5bd7f3737df57b60e8a56339be0a7884ece5347` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2004-08-01 1時 | 24.6 | 88.5 | 1006.9 | 1013.8 | 3.8 | SW | 22.6 | — |
| 2004-08-01 12時 | 29.0 | 69.2 | 1007.0 | 1013.8 | 2.9 | S | 22.8 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
