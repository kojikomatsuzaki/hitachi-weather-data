# 1993年12月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1993/12.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 94 | 650 | `source_blank`: 649, `source_whitespace`: 1 |
| `station_pressure_hpa` | 248 | 248 | 0 | — |
| `sea_level_pressure_hpa` | 248 | 248 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 341 | 186 | `source_blank`: 186 |
| `sunshine_duration_h` | 527 | 188 | 339 | `source_blank`: 339 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 738 | 6 | `source_dash`: 6 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1993.xls` | `910c23f66e99d74982b50a1d8e04f276163cbd9af97d26822eef8bfefbe817d7` | verified |
| `humidity` | `humi1993.xls` | `3848aca165fdc7303db847004635e14908530e26fb46e4594f380bebf38afd95` | verified |
| `precipitation` | `prec1993.xls` | `f6cb76216bced217379acad685dc96dd3dd7f62d862c02a720d6a7e31057c960` | verified |
| `pressure` | `pres1993.xls` | `14c886ba62f9b3fd324de685065247de0de9b5ac92ca1c4d2e0b5748399a4897` | verified |
| `solar_radiation` | `sunF1993.xls` | `be5e471093479a13d43fd4e5e08b9957e4371ac5c42480fbc52460bf360e1c33` | verified |
| `sunshine_duration` | `sunL1993.xls` | `70298426f5c274518ee533a3362ceb4b5977268c60f26f50182d889996062045` | verified |
| `wind_speed` | `wv1993.xls` | `67117312065c5908aa7707fc04756f122643acc9a549b5ec935b0ee4dab1a1d9` | verified |
| `wind_direction` | `wd1993.xls` | `09942d3388f66e91386c2638c97af1732a6371ca17f99f9c3daa3ca6b7268158` | verified |
| `dew_point_temperature` | `dewp1993.xls` | `7536c1549210f90685c7b925ffc83b7a727be7942324410085c988899e7702da` | verified |
| `weather_code` | `weat1993.xls` | `ae30a7ec9fd74cb7fa0e56b5f68e85bfb158a8651ed5dda24e64b9a6e66ceb19` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1993-12-01 1時 | None | None | None | None | 1.7 | WNW | None | — |
| 1993-12-01 12時 | 15.7 | 72.0 | 1003.3 | 1010.5 | 6.5 | W | 10.6 | 3 |

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
