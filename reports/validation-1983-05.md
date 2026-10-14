# 1983年5月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1983/05.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 104 | 640 | `source_blank`: 640 |
| `station_pressure_hpa` | 124 | 124 | 0 | — |
| `sea_level_pressure_hpa` | 124 | 124 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 464 | 63 | `source_blank`: 63 |
| `sunshine_duration_h` | 527 | 296 | 231 | `source_blank`: 231 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 728 | 16 | `source_dash`: 16 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1983.xls` | `9c28c2527ead706bd0197ac822ff86b09304251a3d20d2a168701bdfbe01f035` | verified |
| `humidity` | `humi1983.xls` | `ed25dcb544b6cccb8039f30c36bc5ced349d53779ef50bb7f8832e1cc0b0a564` | verified |
| `precipitation` | `prec1983.xls` | `34da6eb5b163b57bd7cc56ccc7f377255098d83ae3d8c1c26916d221824275e9` | verified |
| `pressure` | `pres1983.xls` | `8e838ac51f1add321357e23be50c121f2935d9b369b8a83e38ad513a236c52dc` | verified |
| `solar_radiation` | `sunF1983.xls` | `2ba2e8efa2eece149150852866457c3990ab76616935edd2f82aa67b77fd5959` | verified |
| `sunshine_duration` | `sunL1983.xls` | `965bcdcb70bd9e2a1b054161ab5cd1113de6489e44040cf2b59ed93a9bee45d6` | verified |
| `wind_speed` | `wv1983.xls` | `ec2be14ee02e4a65589e508683679197fd8e3dc92b8edac8769c5a0005b22d05` | verified |
| `wind_direction` | `wd1983.xls` | `f201df677bfd405bf502460db23809a5a670f582264fcab0bf25ae9dc535266d` | verified |
| `dew_point_temperature` | `dewp1983.xls` | `b0a353f67e478fec7575ae1066c91776feba4502c7ab378080658552abe0369f` | verified |
| `weather_code` | `weat1983.xls` | `c9aaf3626e46e18cdb245ea85148992bca329d5f0bcb689f6b080f0fd9f60a10` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1983-05-01 1時 | None | None | None | None | 1.7 | NNW | None | — |
| 1983-05-01 12時 | 15.1 | 53.4 | None | None | 0.8 | ESE | 5.7 | 3 |

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
