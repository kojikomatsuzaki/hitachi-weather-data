# 1999年10月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1999/10.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 153 | 591 | `source_blank`: 591 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 743 | 1 | `source_dash`: 1 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1999.xls` | `54043407b19de346c3b746c2e79f649242409096fbd85f7f55b7490165a41ee8` | verified |
| `humidity` | `humi1999.xls` | `baabd38389888e4fe5f0d00ff28cfe88f6c233ced90089cb47c089e7c4233468` | verified |
| `precipitation` | `prec1999.xls` | `538489bd6a862805529bd707443f7f8ec7ac3073000ef80d02fa34db2a0a372b` | verified |
| `pressure` | `pres1999.xls` | `c6c143bb91641b175261f4b93245e4401d91de8234d879674c0c29e96d0e6323` | verified |
| `solar_radiation` | `sunF1999.xls` | `107e351fe209262e0a918728e9cc0993813325731d9337bf317dcad82a104169` | verified |
| `sunshine_duration` | `sunL1999.xls` | `a0697e671044f929e105db34a8b3edb913daa0b2987a6119b10bfd36820bb44d` | verified |
| `wind_speed` | `wv1999.xls` | `90ffc409c1aad8d3ec49f09e80e81903e79668d449850465143d3bcb67b182fc` | verified |
| `wind_direction` | `wd1999.xls` | `b91ae591d0d9a89ccfa84a9f33bd353237544dcae76e8fbf11bb42518b8a94bf` | verified |
| `dew_point_temperature` | `dewp1999.xls` | `df9d7ea0a88eb46372ebb6c5981289ee3a6c6b1971012de7927ecf7da9ee67f5` | verified |
| `weather_code` | `weat1999.xls` | `260082981d858eb39bdcfa2addf0e9ba5bb4ea19bf5f65a736292e68e3e604c0` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1999-10-01 1時 | 20.5 | 82.7 | 1010.3 | 1017.4 | 2.3 | N | 17.5 | — |
| 1999-10-01 12時 | 24.1 | 67.8 | 1014.6 | 1021.5 | 4.2 | NNE | 17.8 | 3 |

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
