# 2001年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2001/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 156 | 588 | `source_blank`: 588 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 738 | 6 | `source_dash`: 6 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

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
| 2001-03-01 1時 | 9.4 | 72.6 | 1003.4 | 1010.7 | 1.1 | NNE | 4.7 | — |
| 2001-03-01 12時 | 5.9 | 77.2 | 1002.2 | 1009.6 | 5.8 | NNE | 2.2 | 60 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 天気表記の形式

- 12時の天気は原資料の数値コードを採録した。
