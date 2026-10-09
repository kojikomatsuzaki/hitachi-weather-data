# 2009年12月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2009/12.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 76 | 668 | `source_blank`: 668 |
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
| `temperature` | `temperature.xls` | `218b15e06d29b6d3f2770c9d05524200ad0d9adaf3b1b45b335f9b4fda285b85` | verified |
| `humidity` | `humidity.xls` | `bb81bf217dd99f89932be57ea0cc004dea0ba9da9978e1e6794d86706d4560f4` | verified |
| `precipitation` | `precipitation.xls` | `b0a6374153f7a3bda17217e77db4e48858ff8de99d3c5cba9a3a142e804fd5fe` | verified |
| `pressure` | `pressure.xls` | `2f0c646d4de67b49d25605f131cd533e72a2878e59ca2af96f129680ec4658b7` | verified |
| `solar_radiation` | `solar_radiation.xls` | `90e8537d1cd77cfa6a1f3ad7f397baf410454022b2835dbb981d6acbc313aca9` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `6eea4d6aa5c2057b2686170b62faa8767d1a3e9c29c48630384e2c94ebdaef96` | verified |
| `wind_speed` | `wind_speed.xls` | `0e444f7f1d1b0c4f282d8c237b30234f97b640958b5363efd82e515d961154e7` | verified |
| `wind_direction` | `wind_direction.xls` | `97cf63ae3b029af2949e8a02cdd649d771df58cc9f2b59787044c0e0f75f058c` | verified |
| `dew_point_temperature` | `dew_point.xls` | `efb79e744c4d34329146fe026b383012c5f3a78b3722b383650ea78b2664648f` | verified |
| `weather_code` | `weather.xls` | `8ca571415f2ce47926a1a3af4cdea9c1ab95b2a173f2dfc0e70c3da78afc1af5` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2009-12-01 1時 | 8.9 | 66.0 | 1012.5 | 1019.8852513028531 | 2.1 | NNW | 2.9 | — |
| 2009-12-01 12時 | 12.7 | 41.6 | 1013.4 | 1020.6932686482944 | 4.7 | ENE | 0.0 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
