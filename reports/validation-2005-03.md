# 2005年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2005/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 119 | 625 | `source_blank`: 625 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 740 | 4 | `source_dash`: 4 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `69ffcad814abc0798076d2e38774af7e63b4b78210e791b62a4f721bc1a72874` | verified |
| `humidity` | `humidity.xls` | `c34545245f0186b9d3b734e85c56ba584839e99cffe97a96c3b69e2e762341b5` | verified |
| `precipitation` | `precipitation.xls` | `00b052916d7c782eab0917c533475cd1d04830c6f9ca4acf49c580eaf464b421` | verified |
| `pressure` | `pressure.xls` | `db19dde8122b7bd3a2c124dfbbf9d980bc8e92aadce6ef1846495eaf94b9f846` | verified |
| `solar_radiation` | `solar_radiation.xls` | `ffb010c48d8e63922920b5cfa9e90389746e45d36effa911882db414365d1b06` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `fd33d384b361ac4981022c964fa207bacf2c12bca0b60c2706d8abd2a381a487` | verified |
| `wind_speed` | `wind_speed.xls` | `596a70ea8a130b5b6a05ac0fe6b71d87fdcd8177b6841185e9f972df7c3228cb` | verified |
| `wind_direction` | `wind_direction.xls` | `c3e94839eeae41cf82620e2b0803f0d55b361591feb765bf019da862db1ed6e9` | verified |
| `dew_point_temperature` | `dew_point.xls` | `02ef42a47b8498f5fb52527cf2afec923c0b40efdac21fe615e68e1d0eb72bc8` | verified |
| `weather_code` | `weather.xls` | `1dc2b13e2324042e3bdf8c7ed86ec2efc3e9b411c9cfb6102c3e133ca1df40f3` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2005-03-01 1時 | 3.1 | 41.1 | 1009.6 | 1017.1 | 3.1 | NNW | -8.9 | — |
| 2005-03-01 12時 | 6.5 | 38.8 | 1011.4 | 1018.8 | 3.7 | SE | -6.5 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
