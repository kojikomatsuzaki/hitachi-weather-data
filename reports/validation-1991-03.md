# 1991年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1991/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 174 | 570 | `source_blank`: 570 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 396 | 131 | `source_blank`: 131 |
| `sunshine_duration_h` | 527 | 184 | 343 | `source_blank`: 343 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 704 | 40 | `source_dash`: 40 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1991.xls` | `24d3f0f039efa953ea527b7963ef3d7bef51107325c9aad50cd60714da084cb8` | verified |
| `humidity` | `humi1991.xls` | `45f8ee3f32e1f1786da85d49ea378e496159c82d0a27cecaec3441948626613b` | verified |
| `precipitation` | `prec1991.xls` | `90c72eb50cbe3bc67355e0f4114082020f9668181c91ed5171ec4dff8353bca4` | verified |
| `pressure` | `pres1991.xls` | `19745640625cc527d1656f2237998dae80acae1323343653cb1cf864dc2fbb93` | verified |
| `solar_radiation` | `sunF1991.xls` | `16cb7a2ce811487fe4585a4c47f854b34fc10a6cc3c70ac24586265b71a88fec` | verified |
| `sunshine_duration` | `sunL1991.xls` | `5bd27f4ead1af59b2603206bbb68149f6a623f9671711cca6acea2d777399518` | verified |
| `wind_speed` | `wv1991.xls` | `420cd9e9d4110a8be7e14158d4667ef5d668f49a58bc242110cbf9970baa0dee` | verified |
| `wind_direction` | `wd1991.xls` | `47bf7f4523527de690bd50672155de2251b2d6ea8428e5fd98bf58c2db5ce22a` | verified |
| `dew_point_temperature` | `dewp1991.xls` | `920b7071d5c9e6ec9a3cc8874539d3f4da5b1ac9c0d038e05abaf807174e4504` | verified |
| `weather_code` | `weat1991.xls` | `4f5d4b0bb28624f1bb053306a59cc28824c519d98a2178f9789dae71894a1354` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1991-03-01 1時 | None | None | None | None | 2.0 | NE | None | — |
| 1991-03-01 12時 | 6.0 | 39.9 | None | None | 1.2 | SE | -6.6 | 3 |

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
