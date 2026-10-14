# 1989年6月データ検証報告

## 検証結果

- 判定：合格（未知の原表記は推測せず保持）
- 生成ファイル：`data/hitachi-city-hall/1989/06.yaml`
- 日数：30
- 時間観測レコード数：720
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 240 | 240 | 0 | — |
| `relative_humidity_percent` | 240 | 240 | 0 | — |
| `precipitation_mm` | 720 | 205 | 515 | `source_blank`: 515 |
| `station_pressure_hpa` | 120 | 120 | 0 | — |
| `sea_level_pressure_hpa` | 120 | 120 | 0 | — |
| `global_solar_radiation_mj_m2` | 510 | 446 | 64 | `source_blank`: 60, `source_dash`: 4 |
| `sunshine_duration_h` | 510 | 141 | 369 | `source_blank`: 368, `unrecognized_source_value`: 1 |
| `wind_speed_m_s` | 720 | 720 | 0 | — |
| `wind_direction` | 720 | 626 | 94 | `source_dash`: 94 |
| `dew_point_temperature_c` | 240 | 240 | 0 | — |
| `weather_code` | 30 | 30 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temp1989.xls` | `26ed949fc9da62c667a1362f1e84beec0aa873ef90533b0d271021c43e928419` | verified |
| `humidity` | `humi1989.xls` | `69e6fb6df276f2f2be10b87bb3982866844890f54b6fca8ff04504cdb82785ef` | verified |
| `precipitation` | `prec1989.xls` | `b8501fb4311febda7df03264f7be93534bf00c091aee4d0539720bad60ecec89` | verified |
| `pressure` | `pres1989.xls` | `e474160a8d821cddb8acd03b2ad4ca6d9ac50347d5273fe351148351b6f0d757` | verified |
| `solar_radiation` | `sunF1989.xls` | `0aa8879264e0692bd862e4f92aba839d6b693863d6800508f0a025d5ac3b1b6a` | verified |
| `sunshine_duration` | `sunL1989.xls` | `0873543f4ecf1e86a8728854ed0603b5df5257b2171b9a92509b18ec04d80562` | verified |
| `wind_speed` | `wv1989.xls` | `f7889ce9d28fab6785f0c3b953a59cb2b34c4c9dbd407e5865e3944024730a13` | verified |
| `wind_direction` | `wd1989.xls` | `2755e1009806c4de99b8a7e4c559cf470ba1e9b1b7248379910c9e82252e03ad` | verified |
| `dew_point_temperature` | `dewp1989.xls` | `43a3ff0db989331a71bd267e00f12dd918159fc1976e8d7a28319f52b2995bd9` | verified |
| `weather_code` | `weat1989.xls` | `f63c8d7cb2459c8640ab76159bdfec3bca90b04d1c1021c2e3a071ad5b68c9e4` | verified |

## 解釈を保留した原表記

次のセルは正常値へ推測変換せず、`raw_values`と`unrecognized_source_value`へ保持した。

| 観測要素 | 日 | 時 | 原表記 |
|---|---:|---:|---|
| `sunshine_duration_h` | 13 | 18 | `.` |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1989-06-01 1時 | None | None | None | None | 0.0 | None | None | — |
| 1989-06-01 12時 | 21.5 | 67.8 | None | None | 2.0 | S | 15.3 | 0 |

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
