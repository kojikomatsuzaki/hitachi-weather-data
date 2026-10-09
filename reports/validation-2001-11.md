# 2001年11月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2001/11.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 720 | 720 | 0 | — |
| `relative_humidity_percent` | 720 | 720 | 0 | — |
| `precipitation_mm` | 720 | 77 | 643 | `source_blank`: 643 |
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
| `temperature` | `temperature.xls` | `90e3ba3acdd3e20af05bd5773856525d4746c8d7e66a0b7dd110247fd3b997f0` | verified |
| `humidity` | `humidity.xls` | `faf03bd14f1660c3a9dd6ca07ac417eca5ef5ae6169c33d77448f737a6658818` | verified |
| `precipitation` | `precipitation.xls` | `b48b59e81733197e2d8c198f7771472606ba5793eaf9e19e779277d04d779148` | verified |
| `pressure` | `pressure.xls` | `6d5afd73818c99dd549cbbb2a07c5238b11ab7e129b27ed79faef5a29c075b3e` | verified |
| `solar_radiation` | `solar_radiation.xls` | `f1f5835cb3483c71d11346f58210f48979cd3b7aaadd7a3aef852e94c35a5ceb` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `1a6433e2438a126aae3e0602ff7f6186452a761d8a07ffa847000f5a52f6d991` | verified |
| `wind_speed` | `wind_speed.xls` | `925c29ff3e9c6bbd242361ae9a609d2a4db33ced8617a0dcc3609af15e2c8a58` | verified |
| `wind_direction` | `wind_direction.xls` | `a8f0aafd372bb165ea8a93739ec60222277d1571668216b84025fb93b0652cf5` | verified |
| `dew_point_temperature` | `dew_point.xls` | `85f7eb8ec5194fe1c8e962f8453a202061dbcbc6cc3fa45213a7a4dea629132e` | verified |
| `weather_code` | `weather.xls` | `fd8a438b2e0197358335c415c93a0e86bfdd58be2ef0dfc72b10d5474f493483` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2001-11-01 1時 | 11.7 | 86.7 | 1015.1 | 1022.4 | 1.1 | NW | 9.5 | — |
| 2001-11-01 12時 | 21.1 | 54.5 | 1013.1 | 1020.2 | 3.4 | SW | 11.6 | 1 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
