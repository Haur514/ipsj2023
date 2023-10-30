# ここは

* 情報処理学会論文誌へ投稿した論文の実験データをまとめたリポジトリ．
* SBFLとExceptionHunterの結果が`./data/`に保存されている．
    * 実欠陥の実験結果: `real_faults_result.csv`
    * 人工欠陥の実験結果: `artificial_faults_result.csv`

# CSVファイルの見方

|カラム名|入っているデータ|
|---|---|
|`fileName`|欠陥を含むファイル名|
|`buggy_line`|欠陥箇所の行番号|
|`rank`|欠陥箇所の順位|
|`rEFail`|失敗テストに占める例外期待テストの割合|
|`rEPass`|成功テストに占める例外期待テストの割合|
|`num_failed_cetest`|失敗したカスタム例外期待テスト|
|`num_passed_cetest`|成功したカスタム例外期待テスト|
|`num_failed_stetest`|失敗した標準/サードパーティ例外期待テスト|
|`num_passed_stetest`|成功した標準/サードパーティ例外期待テスト|
|`num_failed_test`|失敗テストの総数|
|`failed_tests_coverage_length`|失敗テストの実行経路の長さ|
|`num_passed_test_execute_buggy_line`|欠陥箇所を実行した成功テストの数|
|`num_failed_test_execute_buggy_line`|欠陥箇所を実行した成功テストの数|
|`type_refail`|`rEFail`による欠陥の区分|
|`type_repass`|`rEPass`による欠陥の区分|
|`bug_id`|欠陥ID|


# データの取得方法
```
bash run.sh
```
RQ1-3の実験結果がresult.txtに保存されます．

