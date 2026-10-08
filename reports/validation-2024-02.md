# 2024年2月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2024/02.yaml`
- 日数：29
- 時間観測レコード数：696
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 696 | 696 | 0 | — |
| `relative_humidity_percent` | 696 | 696 | 0 | — |
| `precipitation_mm` | 696 | 164 | 532 | `source_blank`: 532 |
| `station_pressure_hpa` | 696 | 696 | 0 | — |
| `sea_level_pressure_hpa` | 696 | 696 | 0 | — |
| `global_solar_radiation_mj_m2` | 493 | 493 | 0 | — |
| `sunshine_duration_h` | 493 | 493 | 0 | — |
| `wind_speed_m_s` | 696 | 696 | 0 | — |
| `wind_direction` | 696 | 696 | 0 | — |
| `dew_point_temperature_c` | 696 | 696 | 0 | — |
| `weather_code` | 29 | 29 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `ccbbbe156be0843226f6cdb0f64eb280ce596f672eabf1936954f76ff75e88ad` | verified |
| `humidity` | `humidity.xls` | `b8bd9df5408f891e72d23659364aa86fdc123596be0ab61e790c6f08d63c29d6` | verified |
| `precipitation` | `precipitation.xls` | `e50715d87e285aea30e9b80fab6e55e0ccd25b364c3e116d9026f4a87de9b2ec` | verified |
| `pressure` | `pressure.xls` | `10d694e5d199d623291b3a6e169963979967e7275bdfe62c717983c8f5278e5e` | verified |
| `solar_radiation` | `solar_radiation.xls` | `5739be6ca862ff0599aed38a8afdd6310caefe4e5ffacfbd01e7a3d26f243c53` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `e7231780e59e7742419f66d401c8a216bf47258d18433f43daa68d727e2d7472` | verified |
| `wind_speed` | `wind_speed.xls` | `384943085a051bc476564e3fd9c77e3822c84948405246b48038e1ddee33cfc3` | verified |
| `wind_direction` | `wind_direction.xls` | `055529b5b64ca80a4cc8cf4293b6f4e5afbae16ed857f80fdd6e8194d8485da7` | verified |
| `dew_point_temperature` | `dew_point.xls` | `b23fe418bf08dcaeb26953e3e4432405f15a2d9cf99723e2f2d6a1905ac80809` | verified |
| `weather_code` | `weather.xls` | `f22c337a04878eb5617d7ba3ff685e5625713f10122ec57a9a07d112bd2ec999` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2024-02-01 1時 | 7.0 | 72.9 | 1010.0 | 1016.8 | 1.3 | W | 2.5 | — |
| 2024-02-01 12時 | 15.8 | 34.4 | 1003.7 | 1010.2 | 6.4 | NW | 0.2 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
