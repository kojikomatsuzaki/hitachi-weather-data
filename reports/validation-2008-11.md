# 2008年11月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2008/11.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 95 | 625 | `source_blank`: 625 |
| `station_pressure_hpa` | 720 | 720 | 0 | — |
| `sea_level_pressure_hpa` | 720 | 720 | 0 | — |
| `global_solar_radiation_mj_m2` | 510 | 510 | 0 | — |
| `sunshine_duration_h` | 510 | 510 | 0 | — |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 719 | 1 | `source_dash`: 1 |
| `dew_point_temperature_c` | 720 | 720 | 0 | — |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `d191439051c1f159e92004cc9597a455ee753b3f6ac333cde67e497979152913` | verified |
| `humidity` | `humidity.xls` | `4487c61a9f51764b79496095238f79ee1380bc7e5e22c8d387e9070158eba77f` | verified |
| `precipitation` | `precipitation.xls` | `3fe65b0d2d35fd79c58b6687c4e6957d8ee9b84deea7ba7a8b855dea785a0858` | verified |
| `pressure` | `pressure.xls` | `1754f2884604599edd3ad7c3f04195110b7395961bd977aa26f7334a415b5729` | verified |
| `solar_radiation` | `solar_radiation.xls` | `c41c762052538ae5686aa7e2c95f21902f3943a619f5fb799c71ec451b091745` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `62612c8fa72a8f256b4fcd07628f0eae469c5e72761c9219ec888ac9fe4365de` | verified |
| `wind_speed` | `wind_speed.xls` | `d8fa3eaf799e802d7ddf4cc24110a0e5bec193aaca59f47c21b163ba4f7482f7` | verified |
| `wind_direction` | `wind_direction.xls` | `ed01c97a816248e28e332227d266112c6fc8af109c0c935f91f330b2c9abc83a` | verified |
| `dew_point_temperature` | `dew_point.xls` | `dac78fa59b9f4ef66ec839f8843a4a80395e4fa844d10c99f53b3c6a517daf82` | verified |
| `weather_code` | `weather.xls` | `4f93ee8c4ed798bd7c49c8fe089474add7575537527cef4ee1407d1f776a21b0` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2008-11-01 1時 | 14.3 | 62.6 | 1002.7 | 1009.9 | 4.1 | W | 7.2 | — |
| 2008-11-01 12時 | 18.1 | 42.7 | 1005.0 | 1012.0 | 4.8 | NW | 5.3 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
