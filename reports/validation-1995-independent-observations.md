# 1995年・原資料照合と公開記録

- 全12か月、365日、時刻別レコード8,760件、全11観測要素を収録。
- チェックサム確認済みの原ZIP・XLS（各10件）からLibreOfficeで読取用XLSXへ変換し、53,655個の観測対象セルを独立した座標・値変換処理で照合した。
- 生成前後の全月照合、日別集計、観測時刻、値・フラグ・原表記、YAML/JSON一致を検証した。観測値の未解釈表記は0件。
- Actions内の28件の回帰テストが成功。公開手順に加えた瞬間風速の列ずれテストもローカルで確認し、全29件が成功した。

## 1996年との差異

露点温度はM列に「日」が再掲され、最低値・時刻はN/O列。風速はAF列に「日」が再掲され、最大瞬間風速の方位・風速・時刻はAG/AH/AI列。年月ごとに見出しを照合し、再掲された日付を測定値として読まない。

気温・湿度・露点温度・気圧は3時間観測、風・降水量は1〜24時、日射・日照は4〜20時、天気は12時。非観測時刻はnullとnot_scheduledで保持する。空欄・ダッシュ・空白文字列をゼロや欠測へ推測変換しない。日別集計と極値時刻の原表記を保持し、観測値から再計算しない。

## 証跡と限界

- 原資料診断： https://github.com/kojikomatsuzaki/hitachi-weather-data/actions/runs/38482684647
- 全月独立検証： https://github.com/kojikomatsuzaki/hitachi-weather-data/actions/runs/38483551009
- 検証Artifact：11858763659（SHA-256: 6657c21770eddfe7035a9ba9c9b9bb3e882ef47510dcedfdb2f988f2d629a769）
- 公開生成物取り込み： https://github.com/kojikomatsuzaki/hitachi-weather-data/actions/runs/38484403086
- 機械可読結果： reports/integration-1995-complete.json

独立性は本番パーサーと検証パーサーの間にあり、LibreOffice変換自体を別の読取ソフトで独立保証したものではない。未解釈値0件は原資料に誤記がないことを意味しない。1994年以前の自動遡及は停止し、next_yearを1994とした。
