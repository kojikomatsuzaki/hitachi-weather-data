# 2007年12月データ検証報告

## 検証結果

- 判定：合格（未知の原表記は推測せず保持）
- 生成ファイル：`data/hitachi-city-hall/2007/12.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 740 | 4 | `unrecognized_source_value`: 4 |
| `precipitation_mm` | 744 | 106 | 638 | `source_blank`: 638 |
| `station_pressure_hpa` | 744 | 740 | 4 | `unrecognized_source_value`: 4 |
| `sea_level_pressure_hpa` | 744 | 740 | 4 | `unrecognized_source_value`: 4 |
| `global_solar_radiation_mj_m2` | 527 | 523 | 4 | `unrecognized_source_value`: 4 |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 740 | 4 | `unrecognized_source_value`: 4 |
| `wind_direction` | 744 | 740 | 4 | `unrecognized_source_value`: 4 |
| `dew_point_temperature_c` | 744 | 740 | 4 | `unrecognized_source_value`: 4 |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `5dae0dacb9a5cd2bd4624850a60c7bd47f8e22596bf8b1bea31e982e4d401859` | verified |
| `humidity` | `humidity.xls` | `a5ed85aad9a6c4978a446e9e9206f6c88d41b81f32fd2d53263fdf4663b9bae1` | verified |
| `precipitation` | `precipitation.xls` | `b3bd083b01bf599fcd50a33450bb7556271d8222f0c89fca971b26e6de2c097e` | verified |
| `pressure` | `pressure.xls` | `ba40f4407173920d70f70d54e2f3fbbd8b12eb4488b4b21b6208c8d8876655cc` | verified |
| `solar_radiation` | `solar_radiation.xls` | `b8315077ebdca084f16ac1cb9579cfca38891c675a23ce712838b3db0bfeed27` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `5bb6c98519f72661dcc4a0c10ce4d21b19f183907a402bd166197d892c5f8d32` | verified |
| `wind_speed` | `wind_speed.xls` | `9bdea751ca0a95a986dbebf71a2e1c04424087fc549fb5ef293cdd625557fc27` | verified |
| `wind_direction` | `wind_direction.xls` | `6ccf39e8dbbafa87927ff131edf1d1fde17cbebf7a8be35c6cb03ae97efce1b2` | verified |
| `dew_point_temperature` | `dew_point.xls` | `fac1c00a70f831800cf9ca17cd4b44040c9430dc6f0f23d38f8202b888a80c26` | verified |
| `weather_code` | `weather.xls` | `d0669c15faf7f9e318da3d545b3fd819f82072589f485ffbb477343155d4fc95` | verified |

## 解釈を保留した原表記

次のセルは正常値へ推測変換せず、`raw_values`と`unrecognized_source_value`へ保持した。

| 観測要素 | 日 | 時 | 原表記 |
|---|---:|---:|---|
| `relative_humidity_percent` | 1 | 5 | `****` |
| `relative_humidity_percent` | 1 | 6 | `****` |
| `relative_humidity_percent` | 1 | 7 | `****` |
| `relative_humidity_percent` | 1 | 8 | `****` |
| `station_pressure_hpa` | 1 | 5 | `****` |
| `station_pressure_hpa` | 1 | 6 | `****` |
| `station_pressure_hpa` | 1 | 7 | `****` |
| `station_pressure_hpa` | 1 | 8 | `****` |
| `sea_level_pressure_hpa` | 1 | 5 | `****` |
| `sea_level_pressure_hpa` | 1 | 6 | `****` |
| `sea_level_pressure_hpa` | 1 | 7 | `****` |
| `sea_level_pressure_hpa` | 1 | 8 | `****` |
| `global_solar_radiation_mj_m2` | 1 | 5 | `****` |
| `global_solar_radiation_mj_m2` | 1 | 6 | `****` |
| `global_solar_radiation_mj_m2` | 1 | 7 | `****` |
| `global_solar_radiation_mj_m2` | 1 | 8 | `****` |
| `wind_speed_m_s` | 1 | 5 | `****` |
| `wind_speed_m_s` | 1 | 6 | `****` |
| `wind_speed_m_s` | 1 | 7 | `****` |
| `wind_speed_m_s` | 1 | 8 | `****` |
| `wind_direction` | 1 | 5 | `****` |
| `wind_direction` | 1 | 6 | `****` |
| `wind_direction` | 1 | 7 | `****` |
| `wind_direction` | 1 | 8 | `****` |
| `dew_point_temperature_c` | 1 | 5 | `****` |
| `dew_point_temperature_c` | 1 | 6 | `****` |
| `dew_point_temperature_c` | 1 | 7 | `****` |
| `dew_point_temperature_c` | 1 | 8 | `****` |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2007-12-01 1時 | 9.3 | 78.1 | 1011.1 | 1018.4 | 1.6 | WNW | 5.7 | — |
| 2007-12-01 12時 | 14.1 | 66.0 | 1008.2 | 1015.4 | 1.6 | ESE | 7.9 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
