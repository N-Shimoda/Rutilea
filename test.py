def concatenate_with_spaces(string_list):
    # リスト内の文字列を半角スペースで連結
    result = ' '.join(string_list)
    return result

# 仮の入力リストを設定
input_list = ["This", "is", "a", "sample", "list"]

# 関数を呼び出して文字列を作成し出力
result_string = concatenate_with_spaces(input_list)
print(result_string)  # "This is a sample list"