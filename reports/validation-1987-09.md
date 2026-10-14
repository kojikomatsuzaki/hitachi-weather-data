# 1987年9月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1987/09.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 240 | 240 | 0 | — |
| `relative_humidity_percent` | 240 | 240 | 0 | — |
| `precipitation_mm` | 720 | 189 | 531 | `source_blank`: 531 |
| `station_pressure_hpa` | 120 | 120 | 0 | — |
| `sea_level_pressure_hpa` | 120 | 120 | 0 | — |
| `global_solar_radiation_mj_m2` | 510 | 394 | 116 | `source_blank`: 113, `source_missing`: 3 |
| `sunshine_duration_h` | 510 | 162 | 348 | `source_blank`: 348 |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 672 | 48 | `source_dash`: 48 |
| `dew_point_temperature_c` | 240 | 240 | 0 | — |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1987.xls` | `a10c93b0309c8cd0468ed411a79d0557bb0957a47926f4fcbec5cc6e528ea16e` | verified |
| `humidity` | `humi1987.xls` | `6e0182b5c70c050ceaf6df7f8e0a2ebc1f0e2c7b022d6708c13afd648c5242f6` | verified |
| `precipitation` | `prec1987.xls` | `e411907dd80cfce696d13e5210b1f70d70e8add4d47aa0937eee298154bb30a5` | verified |
| `pressure` | `pres1987.xls` | `a12b4f9da25b8d2cfba1b63a5557379ba76d19cff102ab3062bce27fb81802da` | verified |
| `solar_radiation` | `sunF1987.xls` | `4226009a5139ce09ddb2ea84aec540772f0da7d98377703755459c06a0679d31` | verified |
| `sunshine_duration` | `sunL1987.xls` | `57dc5a2ed91af11f96c901e75733409627de8dd0222d824bdd3494ff1f577ca2` | verified |
| `wind_speed` | `wv1987.xls` | `ab9458d2a6a3e4077b928a597fbc5271ae99b6554a3b569deb5c99c42cfc208c` | verified |
| `wind_direction` | `wd1987.xls` | `254290e0cac59454c85c15c7bc4cfc901e18dbe848c3be690708f73cbbba4abd` | verified |
| `dew_point_temperature` | `dewp1987.xls` | `8af3af11db3385a93ae26c2c5d197591de18739c9a407ec07871ec755ea87341` | verified |
| `weather_code` | `weat1987.xls` | `856f409d73f1df9ca4282b41e328f72267b0254ebaa89e426dd266ff05b214ea` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1987-09-01 1時 | None | None | None | None | 6.0 | WSW | None | — |
| 1987-09-01 12時 | 29.0 | 60.9 | None | None | 2.8 | ENE | 20.7 | 0 |

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
