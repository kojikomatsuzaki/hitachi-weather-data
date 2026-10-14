# 1982年8月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1982/08.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 136 | 608 | `source_blank`: 608 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 449 | 78 | `source_blank`: 78 |
| `sunshine_duration_h` | 527 | 237 | 290 | `source_blank`: 290 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 712 | 32 | `source_dash`: 32 |
| `dew_point_temperature_c` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1982.xls` | `6eaaa06ffcfea12ab640dbf6496337c8ec8b4a381d9cbae001193604eed61b04` | verified |
| `humidity` | `humi1982.xls` | `58f9bc91b3ae95f08c784329516211b4e5b97e914d6d0e9f45445e57e48635b9` | verified |
| `precipitation` | `prec1982.xls` | `fd9b1aa2f6457da65a620b176ab1a68673b4b6ccb4297d5f88ae24afa7d8d7fb` | verified |
| `pressure` | `pres1982.xls` | `59d957dfedb8b8c4d10d1d9bd527be681cca70424924ea7d0f1949fa8e1f5961` | verified |
| `solar_radiation` | `sunF1982.xls` | `f97d2eba3c0c1d2f84f6799e69f97bd4bb9e748e4d9e60fff0942238834de5eb` | verified |
| `sunshine_duration` | `sunL1982.xls` | `41f5f9ddace12874bf9548b649b6c1106d4c460ad3830b6d32dcd9c1b8777f87` | verified |
| `wind_speed` | `wv1982.xls` | `b88624b0236715a55988cf29225a587570cd12afcf11dfc4b74b2103c2223f89` | verified |
| `wind_direction` | `wd1982.xls` | `b7fd48b14eaf0c2fd0f38a63141707f8632b67b77eef699d5bd891aef15daef0` | verified |
| `weather_code` | `weat1982.xls` | `01ebd100070a35bb8b825488d3f9fe7a4bd03870f25cad71b8db8c1e028d7e0a` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1982-08-01 1時 | None | None | None | None | 2.8 | NE | None | — |
| 1982-08-01 12時 | 22.0 | 95.0 | None | None | 4.8 | NE | None | 3 |

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
