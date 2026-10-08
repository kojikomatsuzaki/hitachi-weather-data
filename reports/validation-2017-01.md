# 2017年1月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2017/01.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 49 | 695 | `source_blank`: 695 |
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
| `temperature` | `temperature.xls` | `88e53dad77efbb79b654ab198ef593bce2285ca5c4a13413de2cdf2fea693eff` | verified |
| `humidity` | `humidity.xls` | `59297b5b938fc4fe76cb7fa85f3ebf99264ed3464d38a0d76d69133f254339fb` | verified |
| `precipitation` | `precipitation.xls` | `fc1dea34d3696f93a857a475279a67b39bb0476c452238927ae58a7a10ea2221` | verified |
| `pressure` | `pressure.xls` | `f2b075a956176416fed7e34bd68bd96e98cd8ddd5b075a85f484757e0bf52aa3` | verified |
| `solar_radiation` | `solar_radiation.xls` | `171b56affb7ae04ce060eaf8511cce01ce6db765bdecb7c74d174b3d0a282ee5` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `75a4ef0c68c5c8e05f648fa7c9ac4897ee1eaf44bbe5fa5227af8e85a9866ead` | verified |
| `wind_speed` | `wind_speed.xls` | `36fb52cc2d3c413bb3aec097454bef4a7cba80a63dddab8f58e5a05e584ba8df` | verified |
| `wind_direction` | `wind_direction.xls` | `164e4dc50278fe8c6e26330966da7bf6e19a20cc12c78f365c2690c3651d13d1` | verified |
| `dew_point_temperature` | `dew_point.xls` | `5e0bb2718c88614af346bf798bc44b55030cba239e3396904ef5793ee79150f2` | verified |
| `weather_code` | `weather.xls` | `c3226273ca46012abe724c4c31bf25ab956d8ead6440adf1cc1d539bbd39461a` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2017-01-01 1時 | 4.8 | 56.2 | 1015.4 | 1022.9 | 1.6 | WNW | -3.2 | — |
| 2017-01-01 12時 | 12.0 | 45.1 | 1014.8 | 1022.0 | 2.1 | SSE | 0.5 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
