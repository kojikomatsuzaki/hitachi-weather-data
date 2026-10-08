# 2023年1月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2023/01.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 96 | 648 | `source_blank`: 648 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 743 | 1 | `source_missing`: 1 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `3582aea2029f6c2a4008cbf9e870961f309709ac878790dfcfdc4a263810d44a` | verified |
| `humidity` | `humidity.xls` | `494ad809400a928fa2b1c4d86427ea4de207d5987feb1af85d442623e5d1c778` | verified |
| `precipitation` | `precipitation.xls` | `edaf4aa2b1c2067c0836716f9ed8b3b6143349d2dcd822ea41aa7b89aabd34e2` | verified |
| `pressure` | `pressure.xls` | `683242d296f28155994cb9f80a0f62aea5ac0f3975c039fd2cd60570eb8e7e7e` | verified |
| `solar_radiation` | `solar_radiation.xls` | `a0e91fcf9357c3514ca52b4760b7d5e123c7d120c9f8db2cf82f387ba317d7b4` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `e734c3cdeb618cb75d33e9b155b0d69b2f91e07bc844b3ef51705327d1b1ff33` | verified |
| `wind_speed` | `wind_speed.xls` | `eaaf5ad2c4b2ad801ea11e2815836137e14ed9917567be199f0b7494fdaf35dd` | verified |
| `wind_direction` | `wind_direction.xls` | `d777db6baae7f21f2317681697b7d86c66651fe690b1b6d5f372111b56c6e390` | verified |
| `dew_point_temperature` | `dew_point.xls` | `3f8956cec6d3adc12416d10d1cac6eeedb13435631746e14153aca17e7349ab2` | verified |
| `weather_code` | `weather.xls` | `f9ec6223423d4edffe046e04564ddc534890a15d184b89438b6d05877575d85a` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2023-01-01 1時 | 3.0 | 69.7 | 1013.9 | 1020.8 | 0.1 | CALM | -1.9 | — |
| 2023-01-01 12時 | 11.2 | 35.5 | 1010.6 | 1017.3 | 5.4 | WSW | -3.4 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
