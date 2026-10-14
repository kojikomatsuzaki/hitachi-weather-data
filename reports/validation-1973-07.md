# 1973年7月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1973/07.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 124 | 124 | 0 | — |
| `relative_humidity_percent` | 124 | 124 | 0 | — |
| `precipitation_mm` | 744 | 34 | 710 | `source_blank`: 710 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `sunshine_duration_h` | 527 | 266 | 261 | `source_blank`: 261 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 711 | 33 | `source_dash`: 33 |
| `dew_point_temperature_c` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1973.xls` | `fef26fe387e7fc17ef2bf321caf0edbdb6d387e91722e6c4e9bafd3fcf4bfa6e` | verified |
| `humidity` | `humi1973.xls` | `a2508dfe4ff1447df28316dc660700a2c625961d1ee79c3bcf5b754dbad21aa1` | verified |
| `precipitation` | `prec1973.xls` | `45d7372c93783aad4c9ef603233fe84e0a1756b22b6c6c3e8df59648b36ee054` | verified |
| `pressure` | `pres1973.xls` | `08d13ad383f350a8cacf4a7a705d3712121fd5099cfb70419b037c127cf19705` | verified |
| `sunshine_duration` | `sunL1973.xls` | `16c297b652bbce31fb5477f70730ab8503010b9cc4d2563724c58f570f5f959b` | verified |
| `wind_speed` | `wv1973.xls` | `bf3443635ae19fb5459b80c156d45c5f89e248aec064dea873bffdfb80789079` | verified |
| `wind_direction` | `wd1973.xls` | `1bb777ca2185add69333a9794b0f386ad62439aa6c8797498cb4f88a2a29a1aa` | verified |
| `weather_code` | `weat1973.xls` | `bacf7ec8c312b2d9f6830637427fe422a281cd5d4e61d3b6cb5453e2adf3fa74` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1973-07-01 1時 | None | None | None | None | 0.3 | NNE | None | — |
| 1973-07-01 9時 | 20.4 | 85.0 | 1008.0 | 1015.0 | 2.2 | SSW | None | 3 |

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
