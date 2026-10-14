# 1981年8月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1981/08.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 100 | 644 | `source_blank`: 644 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 459 | 68 | `source_blank`: 68 |
| `sunshine_duration_h` | 527 | 288 | 239 | `source_blank`: 239 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 670 | 74 | `source_dash`: 74 |
| `dew_point_temperature_c` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1981.xls` | `a1f67309ce153b9a227e47c3153d2e9a1068524dffa762e429039365894aef8a` | verified |
| `humidity` | `humi1981.xls` | `98f1cce7ddfb14046524b8b1034c13004ba732d297ada312554d8cdfc5c13cea` | verified |
| `precipitation` | `prec1981.xls` | `e04c7d21d2d27c42e7e6244b32064af65c23700cc7d70195eceb9859536c66c8` | verified |
| `pressure` | `pres1981.xls` | `8863399f44d5a3494d4d6e720bf8c0647518dbbf27c3b517095feeeea853e5b3` | verified |
| `solar_radiation` | `sunF1981.xls` | `9994ddf9d69c27df462314db49849ef80c3908fa17a09b8b05b75b567f5ba95e` | verified |
| `sunshine_duration` | `sunL1981.xls` | `381925f811b3b6de0e18efee64b8813667e01e84965752bee30f991b47272beb` | verified |
| `wind_speed` | `wv1981.xls` | `baeb15f538f280bffc63477020a8d14408b83318fa02732b721e54351777970b` | verified |
| `wind_direction` | `wd1981.xls` | `17c75920e09b7cf1f8662b0a4f1e53f7c3b3dd41a537cf54359964eb1da2b067` | verified |
| `weather_code` | `weat1981.xls` | `245539176ad895d66d7b9cf9042fc92a7d2a3e455cc39fc595f70c3e0f36e543` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1981-08-01 1時 | None | None | None | None | 2.5 | WSW | None | — |
| 1981-08-01 12時 | 27.6 | 76.0 | None | None | 4.2 | SW | None | 1 |

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
