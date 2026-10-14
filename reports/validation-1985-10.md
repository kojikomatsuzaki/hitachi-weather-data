# 1985年10月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1985/10.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 114 | 630 | `source_blank`: 630 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 390 | 137 | `source_blank`: 137 |
| `sunshine_duration_h` | 527 | 244 | 283 | `source_blank`: 283 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 736 | 8 | `source_dash`: 8 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1985.xls` | `d4c482c5636f0ed1119248712e88437c112953dd0d84a986d6db82e3a1c0c77d` | verified |
| `humidity` | `humi1985.xls` | `babd430553694d60d9b380c741ad7d3f7ecdfda26c6a1bb5e0cc4f9bcc3f140b` | verified |
| `precipitation` | `prec1985.xls` | `56b12f99d2393531b81f1e083562863ffab3cab173758f559736c6d46c6055bb` | verified |
| `pressure` | `pres1985.xls` | `4c4930104d3b65bc542335364d6ef1f0024d719b193221785289b27e9fef229d` | verified |
| `solar_radiation` | `sunF1985.xls` | `f44323e2d25e5dead94c692655fa62e6a865f112fc203dd83bf08db6c34c659c` | verified |
| `sunshine_duration` | `sunL1985.xls` | `64d83753b9417d972933ec745c06351ea6dbce0818bd04a06fa5c3cfe93572ff` | verified |
| `wind_speed` | `wv1985.xls` | `f61478c35582004c6c50f0e515bf502c51f2b0134551d5eefa0a71647b71b9fc` | verified |
| `wind_direction` | `wd1985.xls` | `86b8bf8404506efee8e7af503663af65db4f112f73f0ddb282020999914fc772` | verified |
| `dew_point_temperature` | `dewp1985.xls` | `a41a50d7dd43a99898f169e20d607897e9a6f53785bce2209d725e6efcbd3b5a` | verified |
| `weather_code` | `weat1985.xls` | `b6f35adf6070626a1cfce8fb47b6cc568010c8fae5bd8e499b0491731cb76f70` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1985-10-01 1時 | None | None | None | None | 1.7 | WNW | None | — |
| 1985-10-01 12時 | 21.2 | 82.5 | None | None | 1.2 | S | 18.1 | 3 |

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
