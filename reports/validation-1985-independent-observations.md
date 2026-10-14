# 1985年・全月原資料照合

- 12か月、365日、8760時間レコード。
- 11要素、50735観測対象セルを独立照合。
- 未解釈の原表記：0件。値とフラグと原表記を保持。
- 原ZIP・XLSのチェックサム、生成前後のセル照合、日別集計、YAML/JSON一致を検証。
- 検証Actions：https://github.com/kojikomatsuzaki/hitachi-weather-data/actions/runs/38516716861
- 比較はLibreOfficeで読取用に変換したXLSXを使う。変換自体の完全性を別ソフトで保証するものではない。
- 原資料の空欄をゼロへ置換せず、非観測時刻をnot_scheduledで区別する。自動遡及は停止中。
