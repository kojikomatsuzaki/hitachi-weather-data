# 2010年7月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2010/07.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 155 | 589 | `source_blank`: 589 |
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
| `temperature` | `temperature.xls` | `9005181b1ed5d6aff8f2bcf25e56605a06fa0ef45a011866e439f9c0a7b37326` | verified |
| `humidity` | `humidity.xls` | `9fb7d9bef0cf0d26d77bd21679615ce5dd057f6ad3c858e56f2ef0b5cdd69255` | verified |
| `precipitation` | `precipitation.xls` | `60c0a450bfc3a0f9df2f08a6fb44250a890c4c61b3bcf9b76e6bd0659e9fd868` | verified |
| `pressure` | `pressure.xls` | `6d5fcc9ba84a7b176fb9f5a479366fba9ea14aadaaab89c224043c131c689cfd` | verified |
| `solar_radiation` | `solar_radiation.xls` | `8715bff6eaf739be5d5b69bac5eeb6e7598414201be4fb03d1d864725ec3c313` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `297d3987977537f9cc8dd919f68bbff0bd4e24fc6b728bd9e935f5ad5a090723` | verified |
| `wind_speed` | `wind_speed.xls` | `c9b1cd86f3904922cfe7f9a93d7d2c53cb2a2c0be6fa14a7104b44bc27c7d15a` | verified |
| `wind_direction` | `wind_direction.xls` | `dfd8a6046ba7c094f952e7dfd34a7b04a50cbf9b08b3ca68084fa9462816bebc` | verified |
| `dew_point_temperature` | `dew_point.xls` | `20a971f9d0f81d130bcd888623fe4eb56fc85aab349d7d54d1a136a2945990d1` | verified |
| `weather_code` | `weather.xls` | `fa95b47b4682a9e32269057b8477f81284e421ee84e5896f2f2d9cf522ab0d4d` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2010-07-01 1時 | 20.9 | 94.6 | 999.7 | 1006.6934770681739 | 1.9 | SW | 20.0 | — |
| 2010-07-01 12時 | 24.4 | 77.4 | 1000.3 | 1007.2151350537113 | 1.8 | SE | 20.2 | 3 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
