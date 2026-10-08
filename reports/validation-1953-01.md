# 1953年1月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1953/01.yaml`
- 日数：31
- 時刻レコード数：558
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ZIPのSHA-256：8ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 124 | 124 | 0 | — |
| `relative_humidity_percent` | 124 | 124 | 0 | — |
| `precipitation_mm` | 744 | 0 | 744 | `source_blank`: 744 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 0 | 124 | `source_blank`: 124 |
| `sunshine_duration_h` | 527 | 245 | 282 | `source_blank`: 282 |
| `wind_speed_m_s` | 124 | 124 | 0 | — |
| `wind_direction` | 124 | 86 | 38 | `source_dash`: 38 |
| `weather_code` | 31 | 31 | 0 | — |

## 原ZIPの整合性確認

| 要素 | ZIP | 内部ファイル | SHA-256 | 判定 |
|---|---|---|---|---|
| `temperature` | `temperature.zip` | `temp1953.xls` | `7dc3c5078eb87370eb55911c15bdd8124b8f35927cefa120772a380258087292` | verified |
| `humidity` | `humidity.zip` | `humi1953.xls` | `5e18b17b46d494d920901513c89f5d9cf9f75ba07c24d03607eeb3db6f4a65b4` | verified |
| `precipitation` | `precipitation.zip` | `prec1953.xls` | `716c1ef34a34d0308d5352674b4bac94e20d2d770ffc11b83e971745828ea6d5` | verified |
| `pressure` | `pressure.zip` | `pres1953.xls` | `36b2f96654092b8d794401208fb849d856772debdc9195be87a44aea2ba8632c` | verified |
| `sunshine_duration` | `sunshine_duration.zip` | `sunL1953.xls` | `19b99d40c215cf344c3ff35f3c8ba5cd7695f98c93b6295ce291740a7605ed08` | verified |
| `wind_speed` | `wind_speed.zip` | `wv1953.xls` | `616710658b0cd8ef4887fc5a7e7d94a8f818e3a8675f05a4639a8829a736aa21` | verified |
| `wind_direction` | `wind_direction.zip` | `wd1953.xls` | `44d89d7328636f56afcc7f78ebea68797faedf9ec415b3098b1340a49bdf3e5d` | verified |
| `weather_code` | `weather_code.zip` | `weat1953.xls` | `b3d1d73ad8d066eebea448eeae55ac3ffc9ee1a8b2ae6632eab294a69417846c` | verified |

## 代表値の確認

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 風速 | 風向 | 天気 |
|---|---:|---:|---:|---:|---|---|
| 1953-01-01 6時 | 5.7 | 75.0 | 1007.9 | 4.8 | NW | — |
| 1953-01-01 9時 | 9.0 | 57.0 | 1004.4 | 5.4 | SW | 0 |

## 年代による構造差

- 気温、湿度、現地気圧、風速、風向は6時・9時・14時・22時の記録である。
- 天気は9時の記録であり、2000年以降の12時とは異なる。
- 降水量表は1時から24時の欄を持つが、1953年1月の時刻別セルはすべて空欄で、日合計のみ値がある。
- 露点温度と全天日射量は1953年の公開資料に収録されていない。
- 海面気圧の表は存在するが、1953年1月の時刻別セルはすべて空欄である。

## 現段階での保留事項

- 空欄は0と断定せず、`null`と`source_blank`で保存した。
- 月別集計値と階級別日数は、別工程で採録する。
