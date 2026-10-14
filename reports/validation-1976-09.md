# 1976年9月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1976/09.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 120 | 120 | 0 | — |
| `relative_humidity_percent` | 120 | 120 | 0 | — |
| `precipitation_mm` | 720 | 233 | 487 | `source_blank`: 487 |
| `station_pressure_hpa` | 120 | 120 | 0 | — |
| `sea_level_pressure_hpa` | 120 | 120 | 0 | — |
| `global_solar_radiation_mj_m2` | 720 | 0 | 720 | `source_file_unavailable`: 720 |
| `sunshine_duration_h` | 510 | 0 | 510 | `source_blank`: 510 |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 709 | 11 | `source_dash`: 11 |
| `dew_point_temperature_c` | 720 | 0 | 720 | `source_file_unavailable`: 720 |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1976.xls` | `e8b2b2b75d8c288b302a2590666c6fc5c7548fea8940496a022e4ac8033da013` | verified |
| `humidity` | `humi1976.xls` | `c94e0d992e90478d7916a584b91edadbe87096029dbe05b885d120e16facaeca` | verified |
| `precipitation` | `prec1976.xls` | `f253b804eedbfa3f474a48a616b4e998f515a391117b01bce661447ee614dd01` | verified |
| `pressure` | `pres1976.xls` | `1834d2fa5630b03713cad95f4659a29f6efe18d50d2d807b8204ac71a0c573f7` | verified |
| `sunshine_duration` | `sunL1976.xls` | `74c36f72fa9df996d85ef9567c0c046e1413cc33cbf63afc05c097dc8a105636` | verified |
| `wind_speed` | `wv1976.xls` | `4e12aa44db445f150bc5cb5ce6d5bf2a63a2882104598dc7ee6f6d44555436d5` | verified |
| `wind_direction` | `wd1976.xls` | `6926118f947db991cc97aec76fcb61408458e7eb7d64de7cac2f695619b8a4ca` | verified |
| `weather_code` | `weat1976.xls` | `cfd2bb1bbd7982352cb676c582b9d87b8e8ff24e9721f07e8c2caeac84f1679f` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1976-09-01 1時 | None | None | None | None | 1.5 | WNW | None | — |
| 1976-09-01 12時 | None | None | None | None | 1.8 | S | None | 1 |

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
