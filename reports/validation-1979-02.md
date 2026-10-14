# 1979年2月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1979/02.yaml`
- 日数：28
- 時間観測レコード数：672
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 224 | 224 | 0 | — |
| `relative_humidity_percent` | 224 | 224 | 0 | — |
| `precipitation_mm` | 672 | 120 | 552 | `source_blank`: 552 |
| `station_pressure_hpa` | 112 | 112 | 0 | — |
| `sea_level_pressure_hpa` | 112 | 112 | 0 | — |
| `global_solar_radiation_mj_m2` | 672 | 0 | 672 | `source_file_unavailable`: 672 |
| `sunshine_duration_h` | 476 | 207 | 269 | `source_blank`: 269 |
| `wind_speed_m_s` | 672 | 672 | 0 | — |
| `wind_direction` | 672 | 664 | 8 | `source_dash`: 8 |
| `dew_point_temperature_c` | 672 | 0 | 672 | `source_file_unavailable`: 672 |
| `weather_code` | 28 | 28 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1979.xls` | `1146af5df075e85d011c25b1240381b1b050f8978d62ec45c0b56b21abe80b57` | verified |
| `humidity` | `humi1979.xls` | `3feff690b07134f081e439eb3ecddede6210592d870d62559f0a0c3db27a60c1` | verified |
| `precipitation` | `prec1979.xls` | `89455d1d9deee892812cb066957a4e84ca7669a368932a9347ab24e0c9e36b04` | verified |
| `pressure` | `pres1979.xls` | `e764cdf573e5ab0b8dc8bc5bd7e0b011464912ae3ab1676706696acbb4ff65c1` | verified |
| `sunshine_duration` | `sunL1979.xls` | `cbd2820dfac233276bb9042890b2061041303686c3657d49f69c425a7b77629b` | verified |
| `wind_speed` | `wv1979.xls` | `35bc8126e103649234b52574ddc59d651a722fb6ce61643771e53a4de003e557` | verified |
| `wind_direction` | `wd1979.xls` | `63a2d58752a35744ebfa836f9c453ff0a3fae946e2d5860f93d419c6a90e1d61` | verified |
| `weather_code` | `weat1979.xls` | `6f9f8499bd03098c15c13028b879206e8c5b7b6a336be1d770831ad85d564977` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1979-02-01 1時 | None | None | None | None | 1.2 | NNE | None | — |
| 1979-02-01 12時 | 13.9 | 84.0 | None | None | 3.3 | WSW | None | 3 |

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
