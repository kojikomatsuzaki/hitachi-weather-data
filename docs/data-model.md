# データモデル案 v0.2.0

## 1. 設計目的

日立市天気相談所が公開する日立市役所観測所の気象観測データを、次の条件を満たす形で保存する。

- 人が読んで意味を確認できる。
- プログラムから安定して処理できる。
- 原資料の年月日、時刻表記、観測要素、欠測表現を追跡できる。
- YAMLを正本とし、JSONやCSVなどをYAMLから生成できる。
- 1953年以降の年代差を失わず、同じ考え方で拡張できる。

## 2. 公式データの構造

2025年の日立市役所観測データは、観測要素ごとに分かれた10個のExcelファイルで公開されている。

1. 気温
2. 湿度
3. 降水量
4. 気圧
5. 日射量
6. 日照時間
7. 風速
8. 風向
9. 露点温度
10. 天気

多くのファイルは、1月から12月までの各シートに「日×時刻」を横持ちで収録している。ただし、次の差異がある。

- 気温、湿度、気圧、風速、風向、露点温度：原則として1時から24時まで。
- 日射量、日照時間：4時から20時まで。
- 天気：観測時刻は年代によって異なるため、データセットごとの観測時刻を記録する。
- 気圧：現地気圧と海面気圧の2系列。
- 日別の平均、合計、極値、極値の発生時刻など、時間値から単純には再現できない値も含まれる。

### 2.1 1953年資料の構造

1953年資料は、1953–2007年一括資料の要素別ZIPに含まれる年別Excelである。
同年1月について確認できた構造は次のとおりである。

- 気温、湿度、現地気圧、風速、風向：6時、9時、14時、22時。
- 天気：9時。
- 日照時間：4時から20時の欄。
- 降水量：1時から24時の欄は空白で、日合計などの日別集計値に記録がある。
- 海面気圧：3時、9時、15時、21時の表はあるが、1月の時刻別セルは空白である。
- 露点温度、全天日射量：1953年の公開資料には収録されていない。

この違いを失わないよう、時刻別観測値、日別集計値、資料への収録状況を分けて保存する。

## 3. 正本YAMLの分割単位

正本は、観測所・年・月ごとに1ファイルとする。

```text
data/
└── hitachi-city-hall/
    └── 2025/
        ├── 01.yaml
        ├── 02.yaml
        └── ...
```

年単位の1ファイルにまとめない理由は、1年分では約8,760件の時間レコードとなり、人が差分を確認しにくくなるためである。

## 4. 時刻の扱い

2000年以降の原資料は1時から24時という表記を用いている。24時を翌日0時へ機械的に変換すると、原資料上の日付との対応が見えにくくなる。

初期段階では、次の2項目を正本として保存する。

```yaml
source_date: "2025-01-01"
source_hour: 24
```

ISO 8601形式の日時は、観測方法と集計区間を確認した後、派生データの生成時に付与する。根拠を確認できるまでは「24時＝翌日0時」と断定しない。

1953年のように観測要素ごとに記録時刻が異なる場合は、`observation_schedules`へ要素別の時刻を記録する。記録のない時刻をnullで補完しない。

## 5. 欠測値・特殊表現

Excel上では、空欄、`-`、`***`などが使われている。

- 存在しない暦日（例：2月30日）はレコード自体を作らない。
- 空欄と`-`は、意味を確認できるまで数値の0へ変換しない。
- 値は`null`とし、必要に応じて`flags`へ原資料上の表現を記録する。
- 天気コード90は、原資料の定義どおり「不明」として保持する。
- その年代の公開資料に観測要素が収録されていない場合は、欠測とは区別して`not_available_for_period`とする。

```yaml
values:
  precipitation_mm: null
flags:
  precipitation_mm: source_blank
```

値が存在しない状態の定義と年代別の採録規則は、[採録方針](collection-policy.md)に定める。

### 5.1 原表記を保持する値

既知の値へ安全に正規化できない文字列・数値は、処理を停止する理由とはせず、
`values`を`null`、`flags`を`unrecognized_source_value`として保存する。同時に
`raw_values`へ原Excelのセル値を保持し、推測による補正を行わない。

```yaml
values:
  wind_direction: null
flags:
  wind_direction: unrecognized_source_value
raw_values:
  wind_direction: "****"
```

空セルは`source_blank`、半角・全角空白やタブなど不可視文字だけのセルは
`source_whitespace`として区別する。後者は不可視文字を含む原文字列を
`raw_values`へ保持する。観測要素自体が原資料にない
`not_available_for_period`とも区別する。

ただし、表題、見出し、シート構造、観測要素とファイルの対応に異常がある場合は、
セル値のフォールバックを適用しない。資料の取り違えを疑う検証エラーとして、その
観測要素または年の取り込みを保留する。

## 6. 時間観測値と日別集計値

時間観測値と日別集計値を分離する。

- `observations`：原資料の時刻別観測値。
- `daily_summaries`：日平均、日合計、最大・最小、極値の発生時刻など。
- `monthly_summary`：月平均、月合計、月極値など。必要な項目を精査して後から追加する。

最大・最小値には分単位の発生時刻が含まれ、時間値だけからは再現できない。このため、単なる計算結果として捨てず、出典付きの値として保存する。

## 7. 管理ファイル

```text
metadata/
├── elements.yaml
├── stations/
│   └── hitachi-city-hall.yaml
└── sources/
    └── hitachi-city-hall-2025.yaml
```

- `elements.yaml`：観測要素の識別子、名称、単位、値の型。
- `stations/*.yaml`：観測所の名称、所在地、運営主体など。
- `sources/*.yaml`：公式ファイルのURL、取得日、SHA-256ハッシュ値。

### 7.1 主原資料と代替原資料

同じ年・観測要素について複数の公式配布版が存在する場合は、次の役割を分ける。

- `primary_source`：正本YAMLの生成に使用した原資料。
- `alternative_sources`：比較・検証に使用できる別の公式配布版。

各配布版には、URL、取得日、SHA-256を記録する。ZIPに格納された資料では、
ZIP自体のSHA-256に加えて内部ファイル名と内部ファイルのSHA-256も記録する。
配布版同士を比較した場合は、バイナリ一致、バイナリ相違、構造相違などの結果を残す。
代替原資料の値を、主原資料から生成した月別YAMLへ混在させない。

```yaml
files:
  - element: temperature
    primary_source:
      distribution: annual_individual_file
      url: https://example.invalid/temp2000.xls
      sha256: "..."
    alternative_sources:
      - distribution: bulk_element_archive
        archive_url: https://example.invalid/temp.zip
        archive_sha256: "..."
        archive_member: temp2000.xls
        member_sha256: "..."
        comparison_with_primary: binary_different
```

### 7.2 観測所と観測地点の履歴

観測所の名称を維持したまま設置地点が移転した場合、観測所IDは変えず、
`location_periods`で期間別の観測地点を管理する。月別YAMLは、その月に対応する
`location_period_id`を参照する。

```yaml
station:
  id: motoyama
  name_ja: 本山観測所
  location_periods:
    - id: akasawa-sanso
      name_ja: あかさわ山荘
      from: "2000-01"
      to: "2011-12"
    - id: motoyama-shizen-no-mura-campground
      name_ja: もとやま自然の村キャンプ場
      from: "2012-01"
      to: "2014-07"
    - id: former-motoyama-junior-high-school-site
      name_ja: 旧本山中学校敷地
      from: "2014-08"
      to: null
```

この期間は公開データの範囲と公式ページの記述に基づくものであり、観測施設そのものの
設置日を断定するものではない。各月の正本YAMLでは次のように参照する。

```yaml
dataset:
  station_id: motoyama
  location_period_id: former-motoyama-junior-high-school-site
  year: 2014
  month: 8
```

## 8. 今後確認する事項

1. 1時から24時までの各値が示す観測・集計区間。
2. 降水量の空欄、`0`、`-`の意味の違い。
3. 日射量の公式な単位表記。
4. 観測所の緯度、経度、標高および観測機器の設置条件。
5. 公開データの利用条件と、原Excelファイルを再配布できる範囲。

確認できていない事項を推測で埋めず、`null`または未確定として明示する。

## 9. 変換と検証

2000年以降のデータは、公式一覧から出典マニフェストを生成した後、
`scripts/import_hitachi_city_hall_year.py`で原Excelから生成する。年固有の構造差は
取込処理内で判定し、月別YAMLの`source_period_id`と出典マニフェストへ記録する。
変換前に各ExcelのSHA-256を出典マニフェストと照合し、生成後はYAMLを再読込して、
生成直前のデータ構造と一致することを確認する。

月別の検証結果は、`reports/validation-YYYY-MM.md`へ保存する。
