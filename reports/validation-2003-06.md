# 2003年6月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2003/06.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 156 | 564 | `source_blank`: 564 |
| `station_pressure_hpa` | 720 | 720 | 0 | — |
| `sea_level_pressure_hpa` | 720 | 720 | 0 | — |
| `global_solar_radiation_mj_m2` | 510 | 510 | 0 | — |
| `sunshine_duration_h` | 510 | 510 | 0 | — |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 718 | 2 | `source_dash`: 2 |
| `dew_point_temperature_c` | 720 | 720 | 0 | — |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `007bebbea11fac447f0cb5befc51094a6abccbf6042a5d419a7dc8a160db30b9` | verified |
| `humidity` | `humidity.xls` | `007fab21848d5c3cbeec1f3555df1ccd3ee874b23f4a990016cfb3b6d5c5b0cc` | verified |
| `precipitation` | `precipitation.xls` | `c380c8a7ce3642d340fc59d6c8d6b9faa5cab8c8cc83cc7a27c310d9e9075992` | verified |
| `pressure` | `pressure.xls` | `e03dbf80d357ab192fadcf9d299cc6fd52459b6856d30202051aca079fbe2c4e` | verified |
| `solar_radiation` | `solar_radiation.xls` | `79191b805f9a0f8239c34cb231f7c67e288e4248202e00d8279e6d500014bbe8` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `23e52e9b0b06f70d7e5f8f5222c49c8017cc91e5f93dd48b132a268be1093ca7` | verified |
| `wind_speed` | `wind_speed.xls` | `72641f78df422b939f0c82e86925007c62e64b968aabbc23be5acb91c6e04746` | verified |
| `wind_direction` | `wind_direction.xls` | `13657161c3152d9392a50d9bf743bb2e41dca954f86e3f3d4109a9a1112a7dc4` | verified |
| `dew_point_temperature` | `dew_point.xls` | `635cd9fa04e90df522486acf47cab25d8250703a8720b4b73172a1620688bdd8` | verified |
| `weather_code` | `weather.xls` | `134d65cfc373cf712695a21ebc07751ced010ce906679f2ccafbf3f9682d08ff` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2003-06-01 1時 | 19.4 | 95.8 | 991.5 | 998.4 | 3.0 | SSW | 18.7 | — |
| 2003-06-01 12時 | 22.2 | 89.1 | 987.3 | 994.1 | 0.6 | W | 20.2 | 60 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
