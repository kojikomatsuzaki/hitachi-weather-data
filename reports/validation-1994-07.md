# 1994年7月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/1994/07.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 248 | 248 | 0 | — |
| `relative_humidity_percent` | 248 | 248 | 0 | — |
| `precipitation_mm` | 744 | 82 | 662 | `source_blank`: 661, `source_whitespace`: 1 |
| `station_pressure_hpa` | 248 | 248 | 0 | — |
| `sea_level_pressure_hpa` | 248 | 248 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 465 | 62 | `source_blank`: 62 |
| `sunshine_duration_h` | 527 | 207 | 320 | `source_blank`: 320 |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 714 | 30 | `source_dash`: 30 |
| `dew_point_temperature_c` | 248 | 248 | 0 | — |
| `weather_code` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1994.xls` | `a4a333e4dbf77aae65de52a66967cc80df28b7ccffe3bfefc81719b4901346f8` | verified |
| `humidity` | `humi1994.xls` | `fb73a92f03e1310abccc12bec4df015c7b278180c70807a29ed61b0ebde42e3d` | verified |
| `precipitation` | `prec1994.xls` | `aabaeb0af64847afff39c667f51a564ebcde526d06195c2e978b460c2a4c45de` | verified |
| `pressure` | `pres1994.xls` | `57f9de6ed26c0faf570f4f53b9fa8be6fb810151b362bfbdf83d768543c33133` | verified |
| `solar_radiation` | `sunF1994.xls` | `9f912293dcead451fee6a3bd0932e79e00fd1460df8f138bbca11d3e13658f14` | verified |
| `sunshine_duration` | `sunL1994.xls` | `5fd00beef0aa9efdbf8bedff9348131a2ed93ee83dcda5c2e9561042eabb309d` | verified |
| `wind_speed` | `wv1994.xls` | `9ce5295f2798026264c92433fe62d2e0c250b70c51a473a26f25dc1dcdbae834` | verified |
| `wind_direction` | `wd1994.xls` | `b98e9a51452ae818e3ea2a1f086fc88a568f23e17745ef701738fa2a55062f06` | verified |
| `dew_point_temperature` | `dewp1994.xls` | `3824112a15bacc348d3fb5e8857885deae1ed1e54777cffdf18f17f569f3f307` | verified |
| `weather_code` | `weat1994.xls` | `cbe30bea485c0417a62365a0c74aa6728f49b3b50d15c5cf7aa5f23f714681db` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1994-07-01 1時 | None | None | None | None | 1.5 | SSW | None | — |
| 1994-07-01 12時 | 25.4 | 78.0 | 1003.4 | 1010.2 | 3.7 | WSW | 21.2 | 3 |

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
