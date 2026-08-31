# 2000年1月データ検証報告

## 検証結果

- 判定：合格
- 生成ファイル：`data/hitachi-city-hall/2000/01.yaml`
- 日数：31
- 時間観測レコード数：744
- YAML再読込：成功（生成直前のデータ構造と一致）
- 原ExcelのSHA-256：10ファイルすべて一致

## 観測要素別の抽出件数

| 観測要素 | 原資料上のセル数 | 値あり | null | フラグ |
|---|---:|---:|---:|---|
| `temperature_c` | 744 | 744 | 0 | — |
| `relative_humidity_percent` | 744 | 744 | 0 | — |
| `precipitation_mm` | 744 | 130 | 614 | `source_blank`: 614 |
| `station_pressure_hpa` | 744 | 744 | 0 | — |
| `sea_level_pressure_hpa` | 744 | 744 | 0 | — |
| `global_solar_radiation_mj_m2` | 527 | 527 | 0 | — |
| `sunshine_duration_h` | 527 | 527 | 0 | — |
| `wind_speed_m_s` | 744 | 744 | 0 | — |
| `wind_direction` | 744 | 739 | 5 | `source_dash`: 5 |
| `dew_point_temperature_c` | 744 | 744 | 0 | — |
| `weather_at_noon` | 31 | 31 | 0 | — |

## 原Excelの整合性確認

| 要素 | ファイル | SHA-256 | 判定 |
|---|---|---|---|
| `temperature` | `temperature.xls` | `693e2d507f0980a2b4a2d9a59a9b45f6402ef7971e624a9c52262203a417c32c` | verified |
| `humidity` | `humidity.xls` | `4c3e8924ff0b98afbd6b1777d1114ab664a5006cf562deb65d0ebf19130e175a` | verified |
| `precipitation` | `precipitation.xls` | `f160b7f4960c7643a22132265cbb3f41963537a191781b1f78daa44c90ae21ac` | verified |
| `pressure` | `pressure.xls` | `defefeb4ec929fc7d6e77dacfb222266e99168688b563e49def55f9deaf8df63` | verified |
| `solar_radiation` | `solar_radiation.xls` | `2edfefe35f8e72eda7f58b70334703aa8401d5815800ecb4be2e0d9c81f26e20` | verified |
| `sunshine_duration` | `sunshine_duration.xls` | `a338538cc3779d955790cd812bfe6259933b4278e2bf18ff7357882a0bb1cef3` | verified |
| `wind_speed` | `wind_speed.xls` | `5415cec686420caed36bf13e3621a4f7baf08a35c3de0d6fa5a17014685d4cd7` | verified |
| `wind_direction` | `wind_direction.xls` | `993583fe42afa01c08f28a2dadca0b187bbcc2e237eed1d4218c30cf1d60c3b9` | verified |
| `dew_point_temperature` | `dew_point.xls` | `3a2e4e22f9023c2473b60688677eda37755746262bf6b602aefc7955b3e8372d` | verified |
| `weather_at_noon` | `weather.xls` | `b83460f4494f5538eb91b47af5dd5947aabaecea98cf046e3e47fda35e4035ab` | verified |

## 代表値の確認

次の値は、原Excelと生成YAMLの双方で一致することを確認した。

| 原資料上の日時 | 気温 | 湿度 | 現地気圧 | 海面気圧 | 風速 | 風向 | 露点 | 天気 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| 2000-01-01 1時 | 6.1 | 62.5 | 1012.3 | 1019.8 | 2.1 | NNW | -0.5 | — |
| 2000-01-01 12時 | 12.8 | 30.7 | 1011.5 | 1018.8 | 4.1 | W | -4.1 | 0 |

## 現段階での保留事項

- 1時から24時の各値が示す観測・集計区間は、原資料の表記を維持した。
- 降水量の空欄は0と断定せず、`null`と`source_blank`で保存した。
- 日別集計値はこの段階では収録せず、時間観測値とは別の工程で扱う。

## 2014年・2025年版との形式差

- 時間観測値の月別シートと時刻列は、2025年版の共通処理で抽出できた。
- 12時の天気は2014年版と同じ日本語表記で、2025年版は数値コードだった。
- 日本語の天気表記は `metadata/elements.yaml` の共通語彙へ対応付けた。

## 2000年問題に関する確認

- 生成された全744レコードの日付は、2000-01-01から2000-01-31の範囲にある。
- 2桁年への短縮、1900年への誤認、日付の欠落は検出されなかった。
- 原Excelの月別表は日番号を保持しており、年と月は出典メタデータから明示的に付与した。
