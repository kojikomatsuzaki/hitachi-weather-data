# 2011年6月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2011/06.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 152 | 568 | `source_blank`: 568 |
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
| `temperature` | `temperature.xls` | `323d4e14a5f9a5f378f00f6a093aec59b9c5cd6aebf9238dce0ae7bd4e7acff9` | verified |
| `humidity` | `humidity.xls` | `b1a1064daeb82ffffbeb77655e8b4e4325fd978c0f9de3ac36120ebbc6e76b48` | verified |
| `precipitation` | `precipitation.xls` | `a2353837dad8b3f670c11e1f93d2451c597486f6e2830b50607b133a2fdc5594` | verified |
| `pressure` | `pressure.xls` | `264a128e9e29ef0cee10c48dec20b6403f7f6b4e926d4a126c8e073de8c0f438` | verified |
| `solar_radiation` | `solar_radiation.xls` | `e8e1eab45b314c368aaf359aa8a74dac8301c1cbad0238c946d3bd9560e26e95` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `f158a36c5e167b2d94e15cfcdcbfb9bb219b0e820572f16ba624fa5798802a67` | verified |
| `wind_speed` | `wind_speed.xls` | `5adc874651efdb8a36f639fea3272a540840aa56626104b76313f274b8c4b639` | verified |
| `wind_direction` | `wind_direction.xls` | `99c0d76d6381697752b6a240799947edc6c42f2861cc9ecc5542fcae431997be` | verified |
| `dew_point_temperature` | `dew_point.xls` | `dba883170065f409fc66487db2e7409e7f154afc4662950253a155b055f51e55` | verified |
| `weather_code` | `weather.xls` | `e8f09779ba5b867ac90b1a2378b35915c5b1b77a0b3b97e827dd53080161a16f` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2011-06-01 1時 | 10.3 | 76.8 | 1011.2 | 1018.5 | 2.5 | N | 6.4 | — |
| 2011-06-01 12時 | 12.7 | 72.1 | 1013.2 | 1020.5 | 1.8 | ESE | 7.8 | 3 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
