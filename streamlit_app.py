import streamlit as st
import random
import sympy
import time
from collections import Counter

# --- ユーティリティ関数 ---
def generate_number(difficulty_label):
    if difficulty_label == "簡単 (2-50)":
        return random.randint(2, 50)
    elif difficulty_label == "普通 (2-100)":
        return random.randint(2, 100)
    elif difficulty_label == "難しい (50-200)":
        return random.randint(50, 200)
    else:
        return random.randint(100, 500)

# --- セッション初期化 ---
default_state = {
    'current_number': generate_number("普通 (2-100)"),
    'score': 0,
    'attempts': 0,
    'mode': "通常",
    'start_time': None,
    'problem_number': 1,
    'player_input': "",
    'history': []
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- タイトル ---
st.title("素因数分解ゲーム 🔢")

# --- モード・タイム設定 ---
st.sidebar.title("🎮 ゲームモード")
st.session_state.mode = st.sidebar.radio("モードを選択:", ["通常", "タイムアタック"], key="mode_select")
time_limit = 20
if st.session_state.mode == "タイムアタック":
    time_limit = st.sidebar.selectbox("制限時間（秒）", [10, 20, 30], index=1)

# --- 難易度設定 ---
difficulty = st.selectbox("難易度を選んでください", ["簡単 (2-50)", "普通 (2-100)", "難しい (50-200)", "超難しい (100-500)"])
if st.button("新しい難易度で問題を生成"):
    st.session_state.current_number = generate_number(difficulty)
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.problem_number = 1
    st.session_state.start_time = time.time()
    st.session_state.player_input = ""
    st.session_state.history = []
    st.rerun()

# --- ステータス表示 ---
col1, col2, col3 = st.columns([1, 1, 1])
col1.write(f"問題番号: {st.session_state.problem_number}")
col2.metric("正解数", st.session_state.score)
col3.metric("挑戦回数", st.session_state.attempts)

# --- 問題文 ---
st.write(f"### この数の素因数分解をしてください: **{st.session_state.current_number}**")

# --- ヒント表示 ---
if st.checkbox("ヒントを見る", key="hint_checkbox"):
    n = st.session_state.current_number
    hints = [f"{d}で割り切れます" for d in [2, 3, 5] if n % d == 0]
    if hints:
        st.info("💡 ヒント: " + "、".join(hints))

# --- タイムアタック処理 ---
if st.session_state.mode == "タイムアタック":
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    elapsed = time.time() - st.session_state.start_time
    remaining_time = max(0, time_limit - int(elapsed))
    st.warning(f"⏱️ 残り時間: {remaining_time}秒")

    if remaining_time == 0:
        st.error("⌛ タイムオーバー！")
        time.sleep(1)
        st.session_state.attempts += 1
        st.session_state.current_number = generate_number(difficulty)
        st.session_state.problem_number += 1
        st.session_state.start_time = time.time()
        st.session_state.player_input = ""
        st.rerun()

# --- 入力欄 ---
player_input = st.text_input(
    "素因数をカンマ区切りで入力してください（例: 2, 3, 5）",
    value=st.session_state.player_input,
    key="input_box"
)

# --- 答え合わせ ---
if st.button("答え合わせ！", type="primary"):
    st.session_state.player_input = player_input
    if player_input.strip():
        correct_factors = sympy.factorint(st.session_state.current_number)
        correct_answer = []
        for factor, count in correct_factors.items():
            correct_answer.extend([factor] * count)
        correct_answer = sorted(correct_answer)

        try:
            player_answer = sorted([int(x.strip()) for x in player_input.split(',') if x.strip()])
        except ValueError:
            st.error("⚠️ 数字以外の値が含まれています。")
            st.stop()

        # 素数チェック
        if not all(sympy.isprime(x) for x in player_answer):
            st.warning("⚠️ 素因数には素数のみを入力してください。")

        st.session_state.attempts += 1

        # 結果判定
        is_correct = Counter(player_answer) == Counter(correct_answer)
        if is_correct:
            st.success("🎉 正解です！")
            st.session_state.score += 1
        else:
            st.error("❌ 間違いです！")

        st.write(f"正解: {st.session_state.current_number} = {' × '.join(map(str, correct_answer))}")

        # 履歴に保存
        st.session_state.history.insert(0, {
            'number': st.session_state.current_number,
            'correct': correct_answer,
            'player': player_answer,
            'result': '⭕' if is_correct else '❌'
        })
        st.session_state.history = st.session_state.history[:5]

        st.session_state.problem_number += 1
        st.session_state.current_number = generate_number(difficulty)
        st.session_state.start_time = time.time()
        st.session_state.player_input = ""
        st.rerun()
    else:
        st.warning("答えを入力してください")

# --- その他のボタン ---
col1, col2 = st.columns(2)
with col1:
    if st.button("新しい問題"):
        st.session_state.current_number = generate_number(difficulty)
        st.session_state.start_time = time.time()
        st.session_state.problem_number += 1
        st.session_state.player_input = ""
        st.rerun()
with col2:
    if st.button("スコアリセット"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.problem_number = 1
        st.session_state.start_time = time.time()
        st.session_state.player_input = ""
        st.session_state.history = []
        st.rerun()

# --- 正解率 ---
if st.session_state.attempts > 0:
    accuracy = (st.session_state.score / st.session_state.attempts) * 100
    st.write(f"### 正解率: {accuracy:.1f}%")
    if accuracy >= 80:
        st.success("🏆 素因数分解マスター！")
    elif accuracy >= 60:
        st.info("📚 順調に上達しています！")
    elif accuracy >= 40:
        st.warning("💪 もう少し頑張りましょう！")
    else:
        st.error("🔥 練習あるのみです！")

# --- 解答履歴表示 ---
if st.session_state.history:
    st.write("### 📝 最近の解答履歴（最新5問）")
    for h in st.session_state.history:
        st.write(f"{h['number']} → {h['player']} （正解: {h['correct']}） {h['result']}")
