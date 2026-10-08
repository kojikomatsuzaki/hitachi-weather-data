# 2021年8月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2021/08.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 243 | 501 | `source_blank`: 501 |
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
| `temperature` | `temperature.xls` | `074d44d5db4495a3255e069f0bb97dd09f7a13173b6a40fdeafdff0c4d4e46fd` | verified |
| `humidity` | `humidity.xls` | `10546f0c620bf6ae38a76ac28005341865734b316862541a4c17e8b400b7b2b9` | verified |
| `precipitation` | `precipitation.xls` | `2c9f03bc97fcb21684897196c656ab98ac8684b9b7770a3def6809e2ae5ceb86` | verified |
| `pressure` | `pressure.xls` | `81e2c47011d8f86ee873731051353a641b8a5cdb502213c98ab99f7c4956c3b8` | verified |
| `solar_radiation` | `solar_radiation.xls` | `57e62c369e8ed87038af738adb5275a21844b7906f09722ede4fcb67f5ff5397` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `49043cab4ffdfc1a1077f662b7d1e6071c475e3b8ebc16a5fca070c8a714606b` | verified |
| `wind_speed` | `wind_speed.xls` | `5a5d2c6bc6616e4a7a0a2175326349a068fd3674e4128df52ce00e0a555a0a06` | verified |
| `wind_direction` | `wind_direction.xls` | `a30a620ee7f811695f0041022c28d06421e46f375aeac6cb49c4495465aead05` | verified |
| `dew_point_temperature` | `dew_point.xls` | `06fdf6a251cd7f2bc822bd10eb972bbf3bb463e0c52b751d97459e45210a764e` | verified |
| `weather_code` | `weather.xls` | `d900fa39a02323c346410287a0b039cf19f9ce634a19ed246065d4be3ddb95dc` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2021-08-01 1時 | 24.4 | 89.8 | 995.9 | 1002.2 | 0.6 | W | 22.6 | — |
| 2021-08-01 12時 | 29.0 | 76.6 | 996.5 | 1002.7 | 4.7 | S | 24.5 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
