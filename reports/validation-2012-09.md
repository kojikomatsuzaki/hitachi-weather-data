# 2012年9月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2012/09.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 153 | 567 | `source_blank`: 567 |
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
| `temperature` | `temperature.xls` | `183a5638b69eafcc7d004ab71e8b2db9b583503f7bd8403f44230e0c4fc92ccb` | verified |
| `humidity` | `humidity.xls` | `2f2f40202539bedaac5804b9c20d9d2a3907a4526c7b3cbd30632e64ad7c6a02` | verified |
| `precipitation` | `precipitation.xls` | `aa46179f181e617d599a07b4723783d96b65e795850e769288833f005dfaae74` | verified |
| `pressure` | `pressure.xls` | `cacb87270e54b696262cdc3d4c6225d30ccc8610fbd9e3b8d0fd89f777d7a330` | verified |
| `solar_radiation` | `solar_radiation.xls` | `548e5e7b87f8536e14bd3198ebc6cffce1318cab023932e95eeeec416fa0f71d` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `21aaac9a9f64c86be572dfc60f25ec9dda199509fab78a28a34e82edeb320365` | verified |
| `wind_speed` | `wind_speed.xls` | `47da21b3775243d0bb67bb943816df5c6e0194efecb85832649b147fd61f12bd` | verified |
| `wind_direction` | `wind_direction.xls` | `92fef294156aacaeffec2153c7fac915d7dcea18350b431a9643bd2a84bb70fa` | verified |
| `dew_point_temperature` | `dew_point.xls` | `62936cf16b274e21cb7e5b8e017846879c4db1ef3118ad3c727033074f99ed2a` | verified |
| `weather_code` | `weather.xls` | `8121d4d03fbf15414eb3e9a4a6463324be58eac7d0572747622e8b5fc4db2430` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2012-09-01 1時 | 24.2 | 91.4 | 1009.2 | 1016.1 | 1.3 | WNW | 22.7 | — |
| 2012-09-01 12時 | 25.8 | 84.6 | 1010.2 | 1017.1 | 6.0 | NE | 23.0 | 70 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
