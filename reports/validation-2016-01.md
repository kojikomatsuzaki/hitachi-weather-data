# 2016年1月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2016/01.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 79 | 665 | `source_blank`: 665 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 743 | 1 | `source_blank`: 1 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `53e3996b6902c79aca5cbb46e88631d84f288c81588bb8714507630401e0c3e7` | verified |
| `humidity` | `humidity.xls` | `555c241d61a663834041713f72d5d2765cd28fba8362d800f3fd9b2a45fe4723` | verified |
| `precipitation` | `precipitation.xls` | `4e43779acdfc9943498d33343947f9df4eaa04ab676fa97db41c4d900bbe41fd` | verified |
| `pressure` | `pressure.xls` | `7ad699be639cce9c228e1b651af76eabfde5cee25a41b6cba654ab7ea96bb4ec` | verified |
| `solar_radiation` | `solar_radiation.xls` | `9ec4c52fa8e080bb6f22bde350be091abe9e0af1623704e49cff4f0ae2e267ad` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `657c105496e4e88cf724739ef3c3877fbc785c8848b066a68d279bf57ba92fad` | verified |
| `wind_speed` | `wind_speed.xls` | `ab9fd0592be294eefb65948078844e8ed0845134b3564ecf2023bee6728ad93d` | verified |
| `wind_direction` | `wind_direction.xls` | `d54fff8ad0fb815ed18ed2b61605b3799c65e237967ce8fd941eb238344064d1` | verified |
| `dew_point_temperature` | `dew_point.xls` | `daad30c474916bb400777b909c7cb5a9d66e0fdfe6d2a18b66c0202f5610e2bf` | verified |
| `weather_code` | `weather.xls` | `16b3c6a5f5fadfa0584e9b677482bc7d597b0640617abe1e2494e54258bae544` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2016-01-01 1時 | 4.9 | 60.0 | 1014.3 | 1021.8 | 2.2 | NNW | -2.2 | — |
| 2016-01-01 12時 | 10.4 | 30.1 | 1017.4 | 1024.7 | 2.3 | WNW | -6.4 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
