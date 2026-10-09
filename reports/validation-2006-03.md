# 2006年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2006/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 113 | 631 | `source_blank`: 631 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 741 | 3 | `source_dash`: 3 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `f3d314404af492e1c1a77e33dbf3a58f2d3b909bea7ba2e5ba749d943a4f15db` | verified |
| `humidity` | `humidity.xls` | `dfe465bfe1973829bce629c20af04c875c3a4d499b3ccb68f0af9c9458442f75` | verified |
| `precipitation` | `precipitation.xls` | `3f3ffc8b2b8962cfaeed386460812309432b22cbce9a3b1b3aef27c798281e27` | verified |
| `pressure` | `pressure.xls` | `fb6d15c0656955a9e7d1884c93cda95b3ad9bc2c202d8124365f10999e8a5b6b` | verified |
| `solar_radiation` | `solar_radiation.xls` | `80ee37dc94d575782a6f022b743454a379092de8238300501a8f23ea108e9606` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `8275a756f7ddad03afde712a898aaa484c7b43ead9490d9841ec09f4e30d94a1` | verified |
| `wind_speed` | `wind_speed.xls` | `d0c0f726ca25d26dcca89ac40807a40c3e46d1fde3d55a442db0ef5916a6b972` | verified |
| `wind_direction` | `wind_direction.xls` | `b186c31684b39abf50bfc10f3971b2499d79b7a64d1f6e26b7647e970c1354e3` | verified |
| `dew_point_temperature` | `dew_point.xls` | `7c2d80fa88f7a860337b32da5a352158c428a2e5d87b2653897f8f5f259bd007` | verified |
| `weather_code` | `weather.xls` | `82a1c252e28789e9f45a822c1faf1b27dbb89ece6993d08daa5534beabe80a5c` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2006-03-01 1時 | 4.8 | 72.3 | 1017.0 | 1024.5 | 1.6 | N | 0.2 | — |
| 2006-03-01 12時 | 8.2 | 95.2 | 1002.0 | 1009.3 | 4.7 | NNE | 7.5 | 3 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
