# 2002年2月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2002/02.yaml`
- 日数：28
- 時間観測レコード数：672
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 672 | 672 | 0 | — |
| `relative_humidity_percent` | 672 | 672 | 0 | — |
| `precipitation_mm` | 672 | 76 | 596 | `source_blank`: 596 |
| `station_pressure_hpa` | 672 | 672 | 0 | — |
| `sea_level_pressure_hpa` | 672 | 672 | 0 | — |
| `global_solar_radiation_mj_m2` | 476 | 476 | 0 | — |
| `sunshine_duration_h` | 476 | 476 | 0 | — |
| `wind_speed_m_s` | 672 | 672 | 0 | — |
| `wind_direction` | 672 | 670 | 2 | `source_dash`: 2 |
| `dew_point_temperature_c` | 672 | 672 | 0 | — |
| `weather_code` | 28 | 28 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `dc32e5dfbed922347962742581e3bb2aa5488c8f3288bb82ec569e6b4aa63c25` | verified |
| `humidity` | `humidity.xls` | `7b6f770f16cd171b1b9432a7100f5d4c070f3bfb3b30697d22ca65e3effaf4b1` | verified |
| `precipitation` | `precipitation.xls` | `b9bc1422a32642d8a03315032ad6e205823e4e063d32aa15aaab7e22a87a98a2` | verified |
| `pressure` | `pressure.xls` | `41b067437f286af732a54a6d7f090f738faba8fbdcea24b47253c4cfe31281fd` | verified |
| `solar_radiation` | `solar_radiation.xls` | `e7edfc4432e5a83eb9c9646b1d7d402aa8a0ff8b167f2939a375caf13051ec7e` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `fa3165a8e421c7e625afa1fdd8ab5c4e05c65fa7cf27bbd32658822f1212ce31` | verified |
| `wind_speed` | `wind_speed.xls` | `0500a7bffbbedcb18377948a06cb1fc4e8cec744cd56eb61f6dc1d5bdc7e2c36` | verified |
| `wind_direction` | `wind_direction.xls` | `53b9a50f0f0395a19116be7c503d1e4da4042dcf2f16517fe6ce06dab3e09fbc` | verified |
| `dew_point_temperature` | `dew_point.xls` | `e626c5a3bcf7109e02e436c0fc037059c781d14dfa5d17356315e5472c5ba6e7` | verified |
| `weather_code` | `weather.xls` | `9528f782777847d1bfd5043ecca95bc5faa2a470c594a50b0a26abd95953f236` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2002-02-01 1時 | 0.2 | 57.2 | 1015.2 | 1022.8 | 0.7 | WNW | -7.3 | — |
| 2002-02-01 12時 | 7.8 | 34.0 | 1015.6 | 1023.0 | 3.4 | SE | -7.1 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
