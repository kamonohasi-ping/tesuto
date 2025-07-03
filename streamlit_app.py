import streamlit as st
import random
import sympy

# タイトル
st.title("素因数分解ゲーム 🔢")

# ゲームのルール
st.write("""
素因数分解を行うゲームです。以下の手順でプレイできます：
1. ランダムな整数が表示されます
2. その整数の素因数分解をしてください
3. 素因数をカンマ区切りで入力してください（例: 2, 3, 5）
4. 同じ素因数が複数ある場合は、その回数分入力してください（例: 12 = 2 × 2 × 3 なら「2, 2, 3」）
""")

# セッション状態の初期化
if 'current_number' not in st.session_state:
    st.session_state.current_number = random.randint(2, 100)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# スコア表示
col1, col2 = st.columns(2)
with col1:
    st.metric("正解数", st.session_state.score)
with col2:
    st.metric("挑戦回数", st.session_state.attempts)

# 現在の問題表示
st.write(f"### この数の素因数分解をしてください: **{st.session_state.current_number}**")

# ヒント機能
if st.checkbox("ヒントを見る"):
    # 2で割り切れるかどうかなど、簡単なヒントを表示
    hints = []
    if st.session_state.current_number % 2 == 0:
        hints.append("この数は偶数です（2で割り切れます）")
    if st.session_state.current_number % 3 == 0:
        hints.append("この数は3で割り切れます")
    if st.session_state.current_number % 5 == 0:
        hints.append("この数は5で割り切れます")
    
    if hints:
        st.info("💡 ヒント: " + "、".join(hints))

# プレイヤーの入力欄
player_input = st.text_input(
    "素因数をカンマ区切りで入力してください", 
    placeholder="例: 2, 3, 5",
    help="同じ素因数が複数ある場合は、その回数分入力してください"
)

# ボタンを横に並べる
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("答え合わせ！", type="primary"):
        if player_input.strip():
            # sympyで素因数分解を実施
            correct_factors = sympy.factorint(st.session_state.current_number)
            # 正しい素因数分解の結果をリストに変換（重複を含む）
            correct_answer = []
            for factor, count in correct_factors.items():
                correct_answer.extend([factor] * count)
            correct_answer = sorted(correct_answer)

            # プレイヤーの答えをリストに変換
            try:
                player_answer = [int(x.strip()) for x in player_input.split(',') if x.strip()]
                player_answer = sorted(player_answer)
                
                # 挑戦回数を増やす
                st.session_state.attempts += 1
                
                # 判定
                if player_answer == correct_answer:
                    st.success("🎉 正解です！素晴らしい！")
                    st.session_state.score += 1
                    
                    # 素因数分解の式を表示
                    factor_str = " × ".join([str(f) for f in correct_answer])
                    st.write(f"**{st.session_state.current_number} = {factor_str}**")
                else:
                    st.error(f"❌ 間違いです！")
                    factor_str = " × ".join([str(f) for f in correct_answer])
                    st.write(f"正しい答えは: **{st.session_state.current_number} = {factor_str}**")
                    
            except ValueError:
                st.error("⚠️ 数値を正しく入力してください（例: 2, 3, 5）")
        else:
            st.warning("答えを入力してください")

with col2:
    if st.button("新しい問題"):
        st.session_state.current_number = random.randint(2, 100)
        st.rerun()

with col3:
    if st.button("スコアリセット"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.rerun()

# 難易度選択
st.write("---")
st.write("### 難易度設定")
difficulty = st.selectbox(
    "難易度を選択してください",
    ["簡単 (2-50)", "普通 (2-100)", "難しい (50-200)", "超難しい (100-500)"]
)

if st.button("新しい難易度で問題を生成"):
    if difficulty == "簡単 (2-50)":
        st.session_state.current_number = random.randint(2, 50)
    elif difficulty == "普通 (2-100)":
        st.session_state.current_number = random.randint(2, 100)
    elif difficulty == "難しい (50-200)":
        st.session_state.current_number = random.randint(50, 200)
    else:  # 超難しい
        st.session_state.current_number = random.randint(100, 500)
    st.rerun()

# 正解率表示
if st.session_state.attempts > 0:
    accuracy = (st.session_state.score / st.session_state.attempts) * 100
    st.write(f"### 正解率: {accuracy:.1f}%")
    
    # 正解率に応じてメッセージ表示
    if accuracy >= 80:
        st.success("🏆 素因数分解マスター！")
    elif accuracy >= 60:
        st.info("📚 順調に上達しています！")
    elif accuracy >= 40:
        st.warning("💪 もう少し頑張りましょう！")
    else:
        st.error("🔥 練習あるのみです！")

# 素因数分解の基本説明
with st.expander("素因数分解とは？"):
    st.write("""
    **素因数分解**とは、ある整数を素数の積として表すことです。
    
    **例:**
    - 12 = 2 × 2 × 3 = 2² × 3
    - 18 = 2 × 3 × 3 = 2 × 3²
    - 30 = 2 × 3 × 5
    
    **素数**とは、1とその数自身以外に約数を持たない1より大きい自然数です。
    （例: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...）
    
    **コツ:**
    1. まず2で割り切れるかチェック
    2. 次に3で割り切れるかチェック
    3. 5, 7, 11...と順番に素数で割っていく
    4. 割り切れなくなったら完了
    """)
