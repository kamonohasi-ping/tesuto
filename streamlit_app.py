import streamlit as st
import random

# タイトル
st.title("じゃんけんゲーム")

# 選択肢
hands = ["グー", "チョキ", "パー"]

# プレイヤーの手
player_hand = st.radio("あなたの手を選んでください", hands)

# ボタンで勝負
if st.button("勝負！"):
    # コンピューターの手をランダムに選ぶ
    computer_hand = random.choice(hands)

    # 結果の表示
    st.write(f"あなたの手：{player_hand}")
    st.write(f"コンピューターの手：{computer_hand}")

    # 勝敗判定
    if player_hand == computer_hand:
        result = "引き分け！"
    elif (player_hand == "グー" and computer_hand == "チョキ") or \
         (player_hand == "チョキ" and computer_hand == "パー") or \
         (player_hand == "パー" and computer_hand == "グー"):
        result = "あなたの勝ち！🎉"
    else:
        result = "あなたの負け！😢"

    st.subheader(result)
