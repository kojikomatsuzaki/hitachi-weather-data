# 2022年11月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2022/11.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 124 | 596 | `source_blank`: 596 |
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
| `temperature` | `temperature.xls` | `4b3e0ac97cb00171b01f51816b10487c17297ff0c8021ba792d24a0070508280` | verified |
| `humidity` | `humidity.xls` | `fb0499bd6bc2a679dc4ee06667acce545c645a36034ab51a697a2f687624da4a` | verified |
| `precipitation` | `precipitation.xls` | `54cc08feb9bc5e01cb7feb6d96031b4cb0e90bb942735fe910011231319bfa8e` | verified |
| `pressure` | `pressure.xls` | `a31237aa8a008d8983464510abd2aa0f548c7e7810250eae976b60dab086c926` | verified |
| `solar_radiation` | `solar_radiation.xls` | `8237b397096398242e42be6a7f631c25124cdfe1a872f69e9d0ab39d91170e30` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `59ffdc85c54c24f1f1f25ff2f88132d575ec092eb30c0d44d0966bcaebf89036` | verified |
| `wind_speed` | `wind_speed.xls` | `9c87911a7ca2422297c42e57ee1ca69779be1ecdb8730fe0c7e409540c9ed496` | verified |
| `wind_direction` | `wind_direction.xls` | `e539723faecb165e3ffbb133049d8b0fc3b1071001f0fa9e45bc892925d17eba` | verified |
| `dew_point_temperature` | `dew_point.xls` | `5d81ec9f3683bcbf61367db3b61d946d9b021c5ad3aec922d9e3c84fe4bc507b` | verified |
| `weather_code` | `weather.xls` | `376a9a649407148a87deb2f05dc662a045e084ab4a4fd841c39290ba5cc012a5` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2022-11-01 1時 | 13.5 | 69.8 | 1019.6 | 1026.3 | 3.7 | NNW | 8.1 | — |
| 2022-11-01 12時 | 17.4 | 73.7 | 1015.9 | 1022.4 | 4.0 | NE | 12.7 | 3 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
