# 2015年2月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2015/02.yaml`
- 日数：28
- 時間観測レコード数：672
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 672 | 672 | 0 | — |
| `relative_humidity_percent` | 672 | 672 | 0 | — |
| `precipitation_mm` | 672 | 100 | 572 | `source_blank`: 572 |
| `station_pressure_hpa` | 672 | 672 | 0 | — |
| `sea_level_pressure_hpa` | 672 | 672 | 0 | — |
| `global_solar_radiation_mj_m2` | 476 | 476 | 0 | — |
| `sunshine_duration_h` | 476 | 476 | 0 | — |
| `wind_speed_m_s` | 672 | 672 | 0 | — |
| `wind_direction` | 672 | 672 | 0 | — |
| `dew_point_temperature_c` | 672 | 672 | 0 | — |
| `weather_code` | 28 | 28 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `fd8def09b325b90190edc7f3a9f4097fbc483586d6e3ee4e8dcf583e73e4625b` | verified |
| `humidity` | `humidity.xls` | `c6a36173857e82282923414b580fc38f5e864f396a69ad448a0216c388eb1902` | verified |
| `precipitation` | `precipitation.xls` | `9e7f710e7e315c3f9352fff25ed013d85b31dd2ba74ae390a11ad8196c470a70` | verified |
| `pressure` | `pressure.xls` | `1ed9bc4655cace5e8db4a5fe0f1242878625a73f4ceae02f1ff22f4e7633af45` | verified |
| `solar_radiation` | `solar_radiation.xls` | `f234ad04d5028471681bfea1fe64a7e543906ff84dbf61ef00e8e24b8048c98c` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `d4acc62a1de3f90fe4ca79774a4dcade1961afbc3951a9a4a210512258ae3623` | verified |
| `wind_speed` | `wind_speed.xls` | `486d45e5fb5cbdf7593fc7cf9fee43d75a95a63a858be7d0019cd5788c03d270` | verified |
| `wind_direction` | `wind_direction.xls` | `2fbad81d98978063f78fdb327f267becb912e1f0627aa05d7f667bba46cbe9b2` | verified |
| `dew_point_temperature` | `dew_point.xls` | `b38fccf8edd3d989e8c79162d1d9add770c4806aa624a507a196fdf02e3ab553` | verified |
| `weather_code` | `weather.xls` | `57b695c874408acc60f2b1b6ef4f4a5e442c9d4b2db8f441fddb03c8613ba0cf` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2015-02-01 1時 | 2.0 | 44.3 | 1007.9 | 1015.4 | 2.0 | SSW | -8.9 | — |
| 2015-02-01 12時 | 5.8 | 31.0 | 1012.1 | 1019.5 | 6.2 | WNW | -10.0 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
