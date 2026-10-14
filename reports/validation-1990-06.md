# 1990年6月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1990/06.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 240 | 240 | 0 | — |
| `relative_humidity_percent` | 240 | 240 | 0 | — |
| `precipitation_mm` | 720 | 188 | 532 | `source_blank`: 532 |
| `station_pressure_hpa` | 120 | 120 | 0 | — |
| `sea_level_pressure_hpa` | 120 | 120 | 0 | — |
| `global_solar_radiation_mj_m2` | 510 | 450 | 60 | `source_blank`: 60 |
| `sunshine_duration_h` | 510 | 131 | 379 | `source_blank`: 379 |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 682 | 38 | `source_dash`: 38 |
| `dew_point_temperature_c` | 240 | 240 | 0 | — |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1990.xls` | `58790d3e5f15fac361b5b1b90fcedfeb2721ae055d04b4f4da6cf25385803ea1` | verified |
| `humidity` | `humi1990.xls` | `7f710bf77e0f3b272912c0aec4f07dbe4546c01705d3d983e2f1f48fb9f0b688` | verified |
| `precipitation` | `prec1990.xls` | `9cd93ef5c81bc046af6d422c5cf9d3a951ca7565990072a8487625c0f48c5f91` | verified |
| `pressure` | `pres1990.xls` | `97f1965ae37f9c9ebd4097d127190573ef25062f0c480379120df8f532f34f02` | verified |
| `solar_radiation` | `sunF1990.xls` | `0d5dc77d5664560c0804e8fd3093e14ea15cd5545bacfc8dd869688661f6ea22` | verified |
| `sunshine_duration` | `sunL1990.xls` | `34d99a5e4a999aac4e4dc24cd1da70dad86718b754c3bb2deb0e649794704977` | verified |
| `wind_speed` | `wv1990.xls` | `2bbe74092e40af9fc48f95da9370f16c9bc0bf53db3cb1f94b53ab3c666c31be` | verified |
| `wind_direction` | `wd1990.xls` | `24b642639e34d746fb4ae39ae97c3da8285c66f5273ff2a34cb326d3ef9ad52c` | verified |
| `dew_point_temperature` | `dewp1990.xls` | `317faca493eba7816fc582496a60946a0ed395e05b9e74170d83842a02218311` | verified |
| `weather_code` | `weat1990.xls` | `fe24b2be9ef83860462df8753712ff2c564e941d4747a6116dc1f1d3f0fd497f` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1990-06-01 1時 | None | None | None | None | 1.0 | SW | None | — |
| 1990-06-01 12時 | 24.7 | 47.8 | None | None | 6.5 | SW | 12.9 | 2 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値は時間観測値と混在させず、`daily_summaries`へ収録した。

## 原ZIPの整合性確認

| 要素 | ZIP | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.zip` | `7dc3c5078eb87370eb55911c15bdd8124b8f35927cefa120772a380258087292` | verified |
| `humidity` | `humidity.zip` | `5e18b17b46d494d920901513c89f5d9cf9f75ba07c24d03607eeb3db6f4a65b4` | verified |
| `precipitation` | `precipitation.zip` | `716c1ef34a34d0308d5352674b4bac94e20d2d770ffc11b83e971745828ea6d5` | verified |
| `pressure` | `pressure.zip` | `36b2f96654092b8d794401208fb849d856772debdc9195be87a44aea2ba8632c` | verified |
| `solar_radiation` | `global_solar_radiation.zip` | `f33cb9004daadeef887ac162eca59cfc6e87e263a3194289535fff7472d852c0` | verified |
| `sunshine_duration` | `sunshine_duration.zip` | `19b99d40c215cf344c3ff35f3c8ba5cd7695f98c93b6295ce291740a7605ed08` | verified |
| `wind_speed` | `wind_speed.zip` | `616710658b0cd8ef4887fc5a7e7d94a8f818e3a8675f05a4639a8829a736aa21` | verified |
| `wind_direction` | `wind_direction.zip` | `44d89d7328636f56afcc7f78ebea68797faedf9ec415b3098b1340a49bdf3e5d` | verified |
| `dew_point_temperature` | `dew_point_temperature.zip` | `bf6957b65adafff5e0e612e58b374822ae0597730bc2678236d6460a20caf201` | verified |
| `weather_code` | `weather_code.zip` | `b3d1d73ad8d066eebea448eeae55ac3ffc9ee1a8b2ae6632eab294a69417846c` | verified |

## 読取方式

- 原Excelは変更していない。
- 古いBIFFレコードとの互換性確保のため、LibreOffice Calcで一時XLSXを生成して読み取った。
- 正本生成に使用した原Excelは、ZIP内部ファイルのSHA-256で識別できる。
