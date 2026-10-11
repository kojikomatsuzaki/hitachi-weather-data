# 1996年10月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1996/10.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 139 | 605 | `source_blank`: 605 |
| `station_pressure_hpa` | 248 | 248 | 0 | — |
| `sea_level_pressure_hpa` | 248 | 248 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 380 | 147 | `source_blank`: 147 |
| `sunshine_duration_h` | 527 | 245 | 282 | `source_blank`: 282 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 734 | 10 | `source_dash`: 10 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1996.xls` | `93a9aa3fb96c4c3b397ed7bdce703b8479bc199bac2ff214e3afdf904ae629c9` | verified |
| `humidity` | `humi1996.xls` | `23eea2f7464285b90013df140e82f788352ed0133e972016f4b32dcb53bdf188` | verified |
| `precipitation` | `prec1996.xls` | `4ccfa930add37ef45e7cae213345b187ba55a02fc080bbe93eec67f3ddfbd5c5` | verified |
| `pressure` | `pres1996.xls` | `2789fd58082d9b6a3f9c887f1129d344fa7a5ca8dcc58cfdb87946d06c0ad20e` | verified |
| `solar_radiation` | `sunF1996.xls` | `b1628e94abd5b1fe753f626f5a9b8396f0efbd800577432ea1f46743ebeead49` | verified |
| `sunshine_duration` | `sunL1996.xls` | `e558a42845d8fafcd57ba4295294226f18c69c1d3538a70da513baaad682cc2b` | verified |
| `wind_speed` | `wv1996.xls` | `ccf1d1219cde9aa1f80df120ae4b333581bc2a89b3c67f733497c1559a38478a` | verified |
| `wind_direction` | `wd1996.xls` | `4d8270624d121cefab6803c181632b673a6a32813dd13c2438f9a1ceb57814e9` | verified |
| `dew_point_temperature` | `dewp1996.xls` | `9099f64ac07646c73aff78f9c2907edacff0728e4ef35bae3dea48d5ed1afe02` | verified |
| `weather_code` | `weat1996.xls` | `cf42acba7fa52365ac5fc1eebfe32396019cd6215f0820688e14d4c7d3284b5b` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1996-10-01 1時 | None | None | None | None | 1.3 | NNE | None | — |
| 1996-10-01 12時 | 19.2 | 76.0 | 1002.6 | 1009.5 | 3.2 | NE | 14.8 | 3 |

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
