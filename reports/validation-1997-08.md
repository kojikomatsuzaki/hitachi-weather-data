# 1997年8月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1997/08.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 130 | 614 | `source_blank`: 614 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 734 | 10 | `source_dash`: 10 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1997.xls` | `cc676c8b85a839748e813139009301c8d66f0e597cd24d7c60f537ab27e4556e` | verified |
| `humidity` | `humi1997.xls` | `e734f8c2d47854d0e71c4706e211c547937154bf7d4b9f42165edd8aaf6ba5f8` | verified |
| `precipitation` | `prec1997.xls` | `902e6dc73ca6bd32ff5ee8de3877b57a9139bb41c8ebbd5d8eff5be4e3b91c79` | verified |
| `pressure` | `pres1997.xls` | `7cd0faf878a24ee87d04082bd1f221b21620ecd80c8dad2ec4a91885fa23760b` | verified |
| `solar_radiation` | `sunF1997.xls` | `cb5ec5afe63aa9a3d1eca1c3637efefacb7e87580977473947f63e9fa40e370f` | verified |
| `sunshine_duration` | `sunL1997.xls` | `b03b1c1d5d6b1264e2729a0f1561de8d5332c7516111918697ac1de088aa24b3` | verified |
| `wind_speed` | `wv1997.xls` | `a2a795d28672c7a7033eb798a08f057b1919e79b171f0baafff46500aee6d046` | verified |
| `wind_direction` | `wd1997.xls` | `1f8bb74d592341a467f9dd63f0b758e08f7370b7b84b5571ed40311c726ed8b0` | verified |
| `dew_point_temperature` | `dewp1997.xls` | `27891362aa8f6d3a970c5f59b5a3968ec11b8c87e0cb48e7354f8d079cb0dee1` | verified |
| `weather_code` | `weat1997.xls` | `dc9cbd3234e28a8774b797a773e91937de95d427073668b0a14313d20b66a405` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1997-08-01 1時 | 24.9 | 89.9 | 1004.8 | 1011.6 | 3.1 | SW | 23.1 | — |
| 1997-08-01 12時 | 30.8 | 65.5 | 1004.2 | 1010.9 | 2.9 | SSW | 23.6 | 0 |

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
