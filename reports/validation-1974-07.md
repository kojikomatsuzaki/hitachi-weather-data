# 1974年7月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1974/07.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 124 | 124 | 0 | — |
| `relative_humidity_percent` | 124 | 124 | 0 | — |
| `precipitation_mm` | 744 | 258 | 486 | `source_blank`: 486 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `sunshine_duration_h` | 527 | 112 | 415 | `source_blank`: 415 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 711 | 33 | `source_dash`: 33 |
| `dew_point_temperature_c` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1974.xls` | `7fe0ca3429ac83093431e80e5e388ed027ecf23c80f918a2b1a5f00a80f7e3c2` | verified |
| `humidity` | `humi1974.xls` | `aaf386a948266426279957d2a02812ea0d64b786c14ad932ac3b4764126eaa97` | verified |
| `precipitation` | `prec1974.xls` | `5346c0770e4808a40bf806015529fa7755fc1ff236c28a4b38a8c4158b4bf427` | verified |
| `pressure` | `pres1974.xls` | `8ba9bbf261832b9f4b2febfb06e1307dc34236f8d8db37bc1f66bb41b98662e4` | verified |
| `sunshine_duration` | `sunL1974.xls` | `a4a8c8128b56a9c6fbb0ac96642c9e0d6ee715bc2aa726e2dc0827a8051eda0f` | verified |
| `wind_speed` | `wv1974.xls` | `c5584faf2b256afe5ae39505843afe35b8477fc9c906fbb1366128be3ff68c15` | verified |
| `wind_direction` | `wd1974.xls` | `0f87047cfe940454b19daf7b94090fafdfdd0b6b6431dc3a1d03ceb5b81d8db7` | verified |
| `weather_code` | `weat1974.xls` | `08f04a2c0c2f3c76a5cdd89634f1197935cbeb390e59cce5363e11f0285e4e31` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1974-07-01 1時 | None | None | None | None | 0.3 | NW | None | — |
| 1974-07-01 12時 | None | None | None | None | 0.5 | E | None | 60 |

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
