# 1980年3月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1980/03.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 102 | 642 | `source_blank`: 642 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `sunshine_duration_h` | 527 | 261 | 266 | `source_blank`: 266 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 682 | 62 | `source_dash`: 62 |
| `dew_point_temperature_c` | 744 | 0 | 744 | `source_file_unavailable`: 744 |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1980.xls` | `86853516630da3c00623ec5ddaf8ae6164d3f5a413bbfc78f76f8461437af647` | verified |
| `humidity` | `humi1980.xls` | `1c1567065c78c1bd7d83f24fe60427cdf0c7484fa5c709f37080fe043dbf23ab` | verified |
| `precipitation` | `prec1980.xls` | `99c62c33a1ceeacb3687b00478629b201c91dba4c57b232aeb9cf2acf844f5d6` | verified |
| `pressure` | `pres1980.xls` | `dcfebca69b18435a9478df37a0a78174c42827a013754c677d18cece820da592` | verified |
| `sunshine_duration` | `sunL1980.xls` | `fd0cf6bb6cbe0e3b13c4ea840c44b7e5cc9d39317f4548bdab9ac2171862fdaa` | verified |
| `wind_speed` | `wv1980.xls` | `28b53267dacdf126450846119fae4f7c633ca348d53a6b00617267f57bb652d8` | verified |
| `wind_direction` | `wd1980.xls` | `27c18082e3b7a82ec4f6fc37e867b16ec86aaec92c8cd7b5072697b37a4c46b9` | verified |
| `weather_code` | `weat1980.xls` | `ea9316c21ca95b5eba9a4b0361e683bcc231cdabdc3f61265382711cbf6e7197` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1980-03-01 1時 | None | None | None | None | 1.2 | SW | None | — |
| 1980-03-01 12時 | 10.2 | 83.0 | None | None | 4.7 | WSW | None | 60 |

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
