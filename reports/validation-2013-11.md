# 2013年11月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2013/11.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 66 | 654 | `source_blank`: 654 |
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
| `temperature` | `temperature.xls` | `6d704c888298bc7eeb08883b4d57048c601a1a877a8e4e0790f0d1f6124f598a` | verified |
| `humidity` | `humidity.xls` | `f8602a378d42b4b4db6c91a894d6b0c26647e4121e136ce57097ababcff16c4e` | verified |
| `precipitation` | `precipitation.xls` | `a30e5f348a73e3b42338360f703efde2f70e0445f74a94992405144e21087a23` | verified |
| `pressure` | `pressure.xls` | `26e3d5ab6c06163bcc749370d8909793eba7039eaa69f4c6b4cd01409d15b0f3` | verified |
| `solar_radiation` | `solar_radiation.xls` | `52294a1ef268178cc48c22567513fd1ca60b521ed16dd3216ed12b15664eafb5` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `6e60daba0eeb6e62edcffafb9115a82c3babbf19aecc7ae6336847fdddcf88ad` | verified |
| `wind_speed` | `wind_speed.xls` | `b18f315d164c22f6d9d9a0c0a45efff0e7602981c0933e9d052cf0d3e0ca494a` | verified |
| `wind_direction` | `wind_direction.xls` | `6879ac51264820f246eb50b68db048dfaae63f985cd009902009acfdf4180992` | verified |
| `dew_point_temperature` | `dew_point.xls` | `4aa67d6cb65764d35c5cf1e04114f69caa9a7851710d2c6a51d8c65ab845f053` | verified |
| `weather_code` | `weather.xls` | `555ffdb59e03faf6e770820241e01f5b2b1d80c529317d1437c1d0b79464206d` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2013-11-01 1時 | 14.4 | 59.0 | 1017.0 | 1024.3 | 2.7 | NW | 6.5 | — |
| 2013-11-01 12時 | 19.4 | 50.9 | 1018.3 | 1025.3 | 2.4 | E | 9.0 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
