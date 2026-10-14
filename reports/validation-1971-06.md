# 1971年6月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1971/06.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 120 | 120 | 0 | — |
| `relative_humidity_percent` | 120 | 120 | 0 | — |
| `precipitation_mm` | 720 | 202 | 518 | `source_blank`: 518 |
| `station_pressure_hpa` | 120 | 120 | 0 | — |
| `sea_level_pressure_hpa` | 120 | 120 | 0 | — |
| `global_solar_radiation_mj_m2` | 720 | 0 | 720 | `source_file_unavailable`: 720 |
| `sunshine_duration_h` | 510 | 165 | 345 | `source_blank`: 345 |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 684 | 36 | `source_dash`: 36 |
| `dew_point_temperature_c` | 720 | 0 | 720 | `source_file_unavailable`: 720 |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1971.xls` | `e6c70b5bb0ac723724ad1689855556d5ec9d281bc9b05d002527ec40db3e6105` | verified |
| `humidity` | `humi1971.xls` | `4001a7e0bea4e522ebf707dde6906739425a35e5a75ff0e4c2dc0d3299b5aa5b` | verified |
| `precipitation` | `prec1971.xls` | `1cf345b26893fa30d2e4e5d5f944b3334468809669639b8106120faa5061aba9` | verified |
| `pressure` | `pres1971.xls` | `51ff9dc9dad789eaf70b30076c2dd46987e9e075e4714911c8cdc6aedb184125` | verified |
| `sunshine_duration` | `sunL1971.xls` | `b624c41be8eb2f8b771e0ee90d27103c1de68e6ca7ca0e59191da3a5a74fbb74` | verified |
| `wind_speed` | `wv1971.xls` | `5f2ae9d80652733edfa395676d4d490f63bd39f51ef50e6520932a29df09253c` | verified |
| `wind_direction` | `wd1971.xls` | `29f7e9305f01b512e96a22dde90c3a4f40e4520f91bc31126b536a9c07037df1` | verified |
| `weather_code` | `weat1971.xls` | `c12d1b0d5e96c9dde24e03cf45f66f5dcbc919e68efdc49bbb1e97d66dfe049d` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1971-06-01 1時 | None | None | None | None | 2.7 | NW | None | — |
| 1971-06-01 9時 | 18.2 | 71.0 | 1004.1 | 1011.1 | 2.2 | NE | None | 3 |

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
