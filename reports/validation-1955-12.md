# 1955年12月データ検証報告

## 検証結果

- 判定：合格（原資料に明記された注記がある場合は未解釈事項として併記）
- YAML：`data/hitachi-city-hall/1955/12.yaml`
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
| `sunshine_duration_h` | 527 | 231 | 296 | `source_blank`: 296 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 649 | 95 | `source_dash`: 95 |
| `weather_code` | 31 | 31 | 0 | — |

## 独立照合

- 読取用XLSXの原セルと、時刻別観測値・日別集計値の計3,348項目を独立照合：一致。
- 降水量の時刻欄744セル：すべて原資料の空欄。日別集計は別に保持。
- 対照元のZIP・内部XLSはSHA-256照合済み。

## 原資料の同一性

原ZIPと内部ExcelのSHA-256をマニフェスト値と照合した。

| 要素 | ZIP | 内部ファイル | ZIP SHA-256 | XLS SHA-256 | 判定 |
|---|---|---|---|---|---|
| temperature | `temperature.zip` | `temp1955.xls` | `7dc3c5078eb87370eb55911c15bdd8124b8f35927cefa120772a380258087292` | `f358f49b392d997963f5c151bff29873e85f723ddec285d19b74da986abbd923` | verified |
| humidity | `humidity.zip` | `humi1955.xls` | `5e18b17b46d494d920901513c89f5d9cf9f75ba07c24d03607eeb3db6f4a65b4` | `d735a243606325f56b47f3dacca39fa6b30b63dc8d0e154b3d7d8c19db1179b3` | verified |
| precipitation | `precipitation.zip` | `prec1955.xls` | `716c1ef34a34d0308d5352674b4bac94e20d2d770ffc11b83e971745828ea6d5` | `b55130e561454fa74627bcff1660aa6028b2b9ce98137a19b807a736ce9f6f30` | verified |
| pressure | `pressure.zip` | `pres1955.xls` | `36b2f96654092b8d794401208fb849d856772debdc9195be87a44aea2ba8632c` | `cd5e93d8c7e10940eeccc464cefcfc5f542fc6c83e1c055d58a7fd04804272f8` | verified |
| sunshine_duration | `sunshine_duration.zip` | `sunL1955.xls` | `19b99d40c215cf344c3ff35f3c8ba5cd7695f98c93b6295ce291740a7605ed08` | `a3a0648e165704c7b095721831f28fd7d110416cab7f1f13f25cd6a649590a31` | verified |
| wind_speed | `wind_speed.zip` | `wv1955.xls` | `616710658b0cd8ef4887fc5a7e7d94a8f818e3a8675f05a4639a8829a736aa21` | `dbb8d356600e9f25508365ec32a9b74291a5a6b7325bdca19f007986fa566551` | verified |
| wind_direction | `wind_direction.zip` | `wd1955.xls` | `44d89d7328636f56afcc7f78ebea68797faedf9ec415b3098b1340a49bdf3e5d` | `7621a82c5ed1dc8a143f8b6a7859b6d57881f7224b1457da445b605a7ced776f` | verified |
| weather_code | `weather_code.zip` | `weat1955.xls` | `b3d1d73ad8d066eebea448eeae55ac3ffc9ee1a8b2ae6632eab294a69417846c` | `efa26822945d5ead24b8c2f094407242bae470ebae9eabec5df82d0544946b37` | verified |
| global_solar_radiation | `global_solar_radiation.zip` | `sunF1955.xls (not present)` | `f33cb9004daadeef887ac162eca59cfc6e87e263a3194289535fff7472d852c0` | `not_applicable` | archive_verified_member_absent |
| dew_point_temperature | `dew_point_temperature.zip` | `dewp1955.xls (not present)` | `bf6957b65adafff5e0e612e58b374822ae0597730bc2678236d6460a20caf201` | `not_applicable` | archive_verified_member_absent |

## レイアウト上の注意

- 海面気圧の見出し時刻：3, 9, 15, 21時。
- 風向は1〜24時、風速は6・9・14・22時の見出しを独立して照合した。
- 数値0、空欄、ハイフン等は原資料上の状態を分けて保持した。
- LibreOfficeで読取用XLSXへ変換して解析。原ZIP・原XLSは変更していない。
