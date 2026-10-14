# 1984年10月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1984/10.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 134 | 610 | `source_blank`: 610 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 384 | 143 | `source_blank`: 137, `source_missing`: 6 |
| `sunshine_duration_h` | 527 | 204 | 323 | `source_blank`: 323 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 742 | 2 | `source_dash`: 2 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1984.xls` | `14a9328d91cd088475a4879a682ef33fcace3b2b817937cc094e719664175b46` | verified |
| `humidity` | `humi1984.xls` | `ab74c9b83141619d69fb2c14b0c43c4b3845dc0e4ec2df03b94980486e81e847` | verified |
| `precipitation` | `prec1984.xls` | `0ed6cb77280b041c057a0465e030a55f012c83c0405c247d5ca9e0774267e0ba` | verified |
| `pressure` | `pres1984.xls` | `00d8b12da3930d2e4fb321cca3020517db94813de2cd14c4561c7d060d34002a` | verified |
| `solar_radiation` | `sunF1984.xls` | `0f818f05d2ba2f0053861002167ffba346b68f8eac9c117ddacbabbde609d562` | verified |
| `sunshine_duration` | `sunL1984.xls` | `e59d05610dcba5f061f3d1bf393e32e8d9bbc7e7f388c512b2fb487535d681a1` | verified |
| `wind_speed` | `wv1984.xls` | `16268dc370250406113bccc01ad6a2f3675645568422e71b9c836ea2590b2cd0` | verified |
| `wind_direction` | `wd1984.xls` | `9eb4cddd6b5d0e7356bbfdcc6762ef048b9f1064926ed99cded26dbeabf4e0f6` | verified |
| `dew_point_temperature` | `dewp1984.xls` | `ee4d7ec91fcceff3e4e1e5efc13061966c6c3ea0c07fc4008e656d981c8b1d06` | verified |
| `weather_code` | `weat1984.xls` | `4432b4f1ec2074bd8a01d0c2bb6abe64046afd301d359dd365d502832a3bbe0d` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1984-10-01 1時 | None | None | None | None | 2.3 | NE | None | — |
| 1984-10-01 12時 | 22.1 | 66.2 | None | None | 4.3 | ENE | 15.5 | 1 |

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
