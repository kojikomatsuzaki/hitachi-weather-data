# 1986年5月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1986/05.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 149 | 595 | `source_blank`: 595 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 465 | 62 | `source_blank`: 62 |
| `sunshine_duration_h` | 527 | 300 | 227 | `source_blank`: 227 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 716 | 28 | `source_dash`: 28 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1986.xls` | `5e039eb5846d286e0be65e5d1d5581e3fdea99a8383f220f20030e3b8a23a02b` | verified |
| `humidity` | `humi1986.xls` | `3ba87e36c34266bb1d5de987508c1c991353c85e5467c0de3f98aa749a3722e4` | verified |
| `precipitation` | `prec1986.xls` | `b7d9be7d16a487fb917c80103296c19419378dea3e778b419304bb8677866b7f` | verified |
| `pressure` | `pres1986.xls` | `f03da4c60d0b9b5b134a92529bd934a8ae1b8cf4e1e28b149b6b815049e7db26` | verified |
| `solar_radiation` | `sunF1986.xls` | `f3e1f15f77b9d2b06e4316e2f4a7eba573406753dc733db64c8f77dc9e5d7b1d` | verified |
| `sunshine_duration` | `sunL1986.xls` | `f42e6e0d52bcefdcb9697572a3c33be6eaf8bfeb7e0b08a0f41d616ba0831c30` | verified |
| `wind_speed` | `wv1986.xls` | `4c2f2a5a8a636fd94715826e135fd55e3726bf0841003e92e7b80fee4c87db9e` | verified |
| `wind_direction` | `wd1986.xls` | `7c3aeb8ce131d9038dd317729f986cab8657777d4d1469d05f5e6761aafffc2c` | verified |
| `dew_point_temperature` | `dewp1986.xls` | `8688d25ce046c8805c3a51087015ef32ccf18c55ada154ed48d0e7a6594b4453` | verified |
| `weather_code` | `weat1986.xls` | `7b3ac609e991a50ada56c2b5305204755406b53ba104fb6a9fc784825aafd01b` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1986-05-01 1時 | None | None | None | None | 3.3 | WSW | None | — |
| 1986-05-01 12時 | 16.3 | 62.4 | None | None | 2.0 | SE | 9.1 | 0 |

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
