# 2025年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2025/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 187 | 557 | `source_blank`: 557 |
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
| `temperature` | `temperature.xls` | `ddbadcf26a6a5ac819a25ede99d7b6aa5fb4e1bb5a9d0fb23d0e30ad58ae40ce` | verified |
| `humidity` | `humidity.xls` | `fc3f8ffbd22c203f7efb74c1b99f15769b7f165a60124b19db751ccc7e58c41c` | verified |
| `precipitation` | `precipitation.xls` | `7b7a7b2f864ebd6f7620ba7656e1728d1be22cea3ba12edd9eebed7288b35d14` | verified |
| `pressure` | `pressure.xls` | `28fc3884717408e27626740510ef8a4ec7dbe4d9b2834059264c350c3196d3d8` | verified |
| `solar_radiation` | `solar_radiation.xls` | `a3c27890d3c4705ac532ebbad3e97df07f4939bb85257dc5c0fe3f228a926491` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `5cf5102ce6d6ea770d6c0d650d86544af399142191868ac73596c622dc1511ab` | verified |
| `wind_speed` | `wind_speed.xls` | `04e3bc9ad4d9c8849ee8a62522eb962349a5422f073e6470cf85eca2c226e33a` | verified |
| `wind_direction` | `wind_direction.xls` | `d6afa0c4ed8731814626a17e7549ca8a944c4093ac4532d228019a393aff0c6c` | verified |
| `dew_point_temperature` | `dew_point.xls` | `23378c0b97920e84fdfd7b12f30549157c6ad16477543ab014976e85569cc510` | verified |
| `weather_code` | `weather.xls` | `791b0ace2ba867e0048f58161831c2948337c87e383daf6481ae8219ae16556c` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2025-03-01 1時 | 7.1 | 53.5 | 1013.1 | 1019.9 | 1.2 | NW | -1.6 | — |
| 2025-03-01 12時 | 16.0 | 53.3 | 1013.4 | 1020.0 | 4.5 | SSE | 6.5 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。
