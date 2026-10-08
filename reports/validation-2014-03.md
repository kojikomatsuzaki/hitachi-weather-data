# 2014年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2014/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 143 | 601 | `source_blank`: 601 |
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
| `temperature` | `temperature.xls` | `63409d3c3d328404badd7ecf9cc4c95da5aa4721f5a76e23320f404a6caa841b` | verified |
| `humidity` | `humidity.xls` | `3af408bb37ede59f570d5e424b6d54541c407cb3a7c2054f5946873add657c76` | verified |
| `precipitation` | `precipitation.xls` | `e4d50ecc186cf63aa5a4ff7b876108dcc245d6bcfa71ceffc2e9064443274413` | verified |
| `pressure` | `pressure.xls` | `fb65a5232abfd77a68ee916f42600b305943bcfa4fc21056dc72eb151dae763c` | verified |
| `solar_radiation` | `solar_radiation.xls` | `fcd451954f7881f8a15dc1761a292a0d4fb09b437ab6296bbcae1da3bf624ba2` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `49932c6907cbc10918bada29b23fa28c998b932a260a12108e1180dd7a5e4d3f` | verified |
| `wind_speed` | `wind_speed.xls` | `44459b9d6eaf0a856fb70860ee48be69ba498efaa76360cfacf79b1557afa2f3` | verified |
| `wind_direction` | `wind_direction.xls` | `4ef47f923f568958ec01621eaeefdba7bcc5afa002f3a5da7b77401eba698b86` | verified |
| `dew_point_temperature` | `dew_point.xls` | `1dbe53f8bc685bab6e22861b24e7b76b78bddf77de38cfff9704cd70ba989643` | verified |
| `weather_code` | `weather.xls` | `eff74169afd4c30a8ad07bd7cef8c18637d5fd85164e1526fee4e302e3873871` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2014-03-01 1時 | 7.1 | 75.7 | 1014.6 | 1022.0 | 2.8 | NNE | 3.1 | — |
| 2014-03-01 12時 | 5.1 | 82.1 | 1012.6 | 1020.0 | 4.6 | NNE | 2.3 | 60 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
