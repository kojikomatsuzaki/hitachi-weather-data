# 1992年11月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1992/11.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 240 | 240 | 0 | — |
| `relative_humidity_percent` | 240 | 240 | 0 | — |
| `precipitation_mm` | 720 | 107 | 613 | `source_blank`: 613 |
| `station_pressure_hpa` | 120 | 120 | 0 | — |
| `sea_level_pressure_hpa` | 120 | 120 | 0 | — |
| `global_solar_radiation_mj_m2` | 510 | 331 | 179 | `source_blank`: 179 |
| `sunshine_duration_h` | 510 | 197 | 313 | `source_blank`: 313 |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 714 | 6 | `source_dash`: 6 |
| `dew_point_temperature_c` | 240 | 240 | 0 | — |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1992.xls` | `09af14d393ac01f494980b29a502b885c229919634c5f457cad819744d3e7186` | verified |
| `humidity` | `humi1992.xls` | `af8f64d94aaf962b94b1e37042c2ddb12bbd94e38b608d44b08124e0cbb619c1` | verified |
| `precipitation` | `prec1992.xls` | `3acc042be9a83e0b456cf6e18e38966485906bb08ae925bbd1d92d83f7e59693` | verified |
| `pressure` | `pres1992.xls` | `a6856b6f90d72de576cfe4ec9bea0c69eee11eee926c1aa3e3fc76faad8015ce` | verified |
| `solar_radiation` | `sunF1992.xls` | `45de40eef16dc3b0baf055eb1b9a29deb5827984e2e4847a82aa435971e2a570` | verified |
| `sunshine_duration` | `sunL1992.xls` | `32769faa4cb3c25fdcd424027c31b204ec17f8a33eaeffe5979612322a6d4174` | verified |
| `wind_speed` | `wv1992.xls` | `9be46539f9fb2ad2784d2932bfa27e33d6c62aa796e28bb3d30b0514d0704289` | verified |
| `wind_direction` | `wd1992.xls` | `ef8b18d1e1ce82a6f686b3b99ee43b86e37b76fbd004d0de3122e3429b6c11c5` | verified |
| `dew_point_temperature` | `dewp1992.xls` | `1bacdb364ab233ac2532044e2041ae4d9d4c9335bb63839462271f6099fc1d20` | verified |
| `weather_code` | `weat1992.xls` | `9ac02db1859bba704b37ed61cdb1f90d5aecee9ee4acf3fca2469e2552bb9a28` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1992-11-01 1時 | None | None | None | None | 1.0 | NW | None | — |
| 1992-11-01 12時 | 16.4 | 62.0 | None | None | 4.0 | ESE | 9.2 | 1 |

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
