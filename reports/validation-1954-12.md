# 1954年12月データ検証報告

## 検証結果

- 判定：合格（原資料に明記された注記がある場合は未解釈事項として併記）
- YAML：`data/hitachi-city-hall/1954/12.yaml`
- 日数：31
- 時刻レコード数：744
- YAML再読込：生成直前のデータ構造と一致
- 各月の観測時刻見出し：要素別に照合

## 抽出セル数

| 要素 | セル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 124 | 124 | 0 | — |
| `relative_humidity_percent` | 124 | 124 | 0 | — |
| `precipitation_mm` | 744 | 0 | 744 | `source_blank`: 744 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 0 | 124 | `source_blank`: 124 |
| `sunshine_duration_h` | 527 | 204 | 323 | `source_blank`: 323 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 696 | 48 | `source_dash`: 48 |
| `weather_code` | 31 | 31 | 0 | — |

## 独立照合

- 読取用XLSXの原セルと、時刻別観測値・日別集計値の計3,348項目を独立照合：一致。
- 降水量の時刻欄744セル：すべて原資料の空欄。日別集計は別に保持。
- 対照元のZIP・内部XLSはSHA-256照合済み。

## 原資料の同一性

原ZIPと内部ExcelのSHA-256をマニフェスト値と照合した。

| 要素 | ZIP | 内部ファイル | ZIP SHA-256 | XLS SHA-256 | 判定 |
|---|---|---|---|---|---|
| temperature | `temperature.zip` | `temp1954.xls` | `7dc3c5078eb87370eb55911c15bdd8124b8f35927cefa120772a380258087292` | `c6324d4275ac29a33e9cb3a5f430fce55eff48ccb60904712dbb8c06bc13bba3` | verified |
| humidity | `humidity.zip` | `humi1954.xls` | `5e18b17b46d494d920901513c89f5d9cf9f75ba07c24d03607eeb3db6f4a65b4` | `6772f76e8d892156e49238a0b09fa89df538f9b114fa96f75e8296c7ff1fabaf` | verified |
| precipitation | `precipitation.zip` | `prec1954.xls` | `716c1ef34a34d0308d5352674b4bac94e20d2d770ffc11b83e971745828ea6d5` | `93ff7ebcdc55ba651b2b387de0e4dfafb35b9e2b25b333cefb978edc5aca4039` | verified |
| pressure | `pressure.zip` | `pres1954.xls` | `36b2f96654092b8d794401208fb849d856772debdc9195be87a44aea2ba8632c` | `c738a37297385f3a573d6bd12ce99fdbb99312786f3c7288e961ecf08e261aa2` | verified |
| sunshine_duration | `sunshine_duration.zip` | `sunL1954.xls` | `19b99d40c215cf344c3ff35f3c8ba5cd7695f98c93b6295ce291740a7605ed08` | `7f0aa47a06d0cdab29d6765dc8646688fcd3ddad18343098eca4b471d4947117` | verified |
| wind_speed | `wind_speed.zip` | `wv1954.xls` | `616710658b0cd8ef4887fc5a7e7d94a8f818e3a8675f05a4639a8829a736aa21` | `fa22361c86ceeb0e98b1a4223c423ef32b2042767e0b24d55f52ff2e77fa0646` | verified |
| wind_direction | `wind_direction.zip` | `wd1954.xls` | `44d89d7328636f56afcc7f78ebea68797faedf9ec415b3098b1340a49bdf3e5d` | `0fade84feed0bb9e23a5bbf6d59ba17c5eed4b0a12ed2bfba51f64f5a993fa26` | verified |
| weather_code | `weather_code.zip` | `weat1954.xls` | `b3d1d73ad8d066eebea448eeae55ac3ffc9ee1a8b2ae6632eab294a69417846c` | `a0594cbe11bd01d231270a858fe2adfee8ce2cae2ffc5b7fae94b88722983486` | verified |
| global_solar_radiation | `global_solar_radiation.zip` | `sunF1954.xls (not present)` | `f33cb9004daadeef887ac162eca59cfc6e87e263a3194289535fff7472d852c0` | `not_applicable` | archive_verified_member_absent |
| dew_point_temperature | `dew_point_temperature.zip` | `dewp1954.xls (not present)` | `bf6957b65adafff5e0e612e58b374822ae0597730bc2678236d6460a20caf201` | `not_applicable` | archive_verified_member_absent |

## レイアウト上の注意

- 海面気圧の見出し時刻：3, 9, 15, 21時。
- 風向は1〜24時、風速は6・9・14・22時の見出しを独立して照合した。
- 数値0、空欄、ハイフン等は原資料上の状態を分けて保持した。
- LibreOfficeで読取用XLSXへ変換して解析。原ZIP・原XLSは変更していない。
