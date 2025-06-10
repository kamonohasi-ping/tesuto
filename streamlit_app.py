import streamlit as st
import random
import sympy

# タイトル
st.title("素因数分解ゲーム")

# ゲームのルール
st.write("""
素因数分解を行うゲームです。以下の手順でプレイできます：
1. ランダムな整数が表示されます。
2. その整数の素因数分解をしてください。
3. 答えを入力したら、正誤を判定します。
""")

# ランダムな数を生成
number = random.randint(2, 100)  # 2～100の間でランダムな整数を生成
st.write(f"この数の素因数分解をしてください: {number}")

# プレイヤーの入力欄
player_input = st.text_input("あなたの答えを入力してください (例: 2, 5, 7)")

# 解答ボタン
if st.button("答え合わせ！"):
    # sympyで素因数分解を実施
    correct_factors = sympy.factorint(number)
    # 正しい素因数分解の結果をリストに変換
    correct_answer = sorted([str(factor) for factor in correct_factors.keys() for _ in range(correct_factors[factor])])

    # プレイヤーの答えをリストに変換
    player_answer = sorted(player_input.split(','))
    
    # 判定
    if player_answer == correct_answer:
        st.success("正解です！🎉")
    else:
        st.error(f"間違いです！ 正しい答えは: {', '.join(correct_answer)}")
