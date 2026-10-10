# 1998年5月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1998/05.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 208 | 536 | `source_blank`: 536 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 742 | 2 | `source_dash`: 2 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1998.xls` | `aaf83e21aa340c371e55ca479db4f89c661c1e83a5b422fc30873870d34421d0` | verified |
| `humidity` | `humi1998.xls` | `d8a8317464958bdbc5751e06fa5c4d2b232b15f3ca035c2b3df3a1ebed602526` | verified |
| `precipitation` | `prec1998.xls` | `880c16afe1cec6aea6576fc1533438af3164ea08ee46b7db89473f6144261e31` | verified |
| `pressure` | `pres1998.xls` | `c67279f3e0398d4c0e4956818de17c3c31af05b82ab996859fb11c4dec23bd01` | verified |
| `solar_radiation` | `sunF1998.xls` | `1d7715ce0b4da1eec4a8595ff263ece193f2607ebf50759fbe8000e7f0c1ae42` | verified |
| `sunshine_duration` | `sunL1998.xls` | `1f84b55447cab663df2ef9c99a986d9c326ed97f26807462ac21638014b2e9ff` | verified |
| `wind_speed` | `wv1998.xls` | `738ca2a70f578d0934285ff0c9683f998fa6bc311924faa63d2610ce79a890fb` | verified |
| `wind_direction` | `wd1998.xls` | `84bc7ceb5b0eac8e443ebc62081f8d472273582aa4a576d6b1f328392f07d802` | verified |
| `dew_point_temperature` | `dewp1998.xls` | `cfa19d871f622a6e4531c9148612a409fb070851893ade5c0a1e4d3409243b94` | verified |
| `weather_code` | `weat1998.xls` | `5065b82039b8422eb4d1c7ec3e12375c62fd22db728cbed7f262f6b6c51785be` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1998-05-01 1時 | 12.3 | 79.5 | 1021.4 | 1028.7 | 2.8 | NNE | 8.8 | — |
| 1998-05-01 12時 | 16.7 | 60.2 | 1021.2 | 1028.4 | 1.3 | SSE | 8.9 | 3 |

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
