import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# アプリの設定
# ---------------------------------------------------------
st.set_page_config(page_title="タスクB：レビュー対象の確認", layout="centered")

# ここにお題（導入文）を定義します
INTRO_TEXT = """
地獄を統べる大魔王は、人間界の視察のため、数百年ぶりに渋谷のスクランブル交差点に降り立った。
周囲の人間は、大魔王を見ても逃げ惑うどころか、四角い板（スマホ）を見つめて歩いている。
呆気にとられた大魔王は、とりあえず目の前のコンビニに入ろうとしたが、入り口で立ち止まってしまった。
"""

# ---------------------------------------------------------
# データの読み込み関数
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # ファイル読み込み処理
        df_std = pd.read_csv('standard_group_assignments_with_stories.csv')
        df_hier = pd.read_csv('hierarchical_group_assignments_with_stories.csv')

        # ID照合のため文字列型に統一
        df_std['Reviewer_ID'] = df_std['Reviewer_ID'].astype(str).apply(lambda x: x.replace('.0', ''))
        df_hier['Reviewer_ID'] = df_hier['Reviewer_ID'].astype(str).apply(lambda x: x.replace('.0', ''))

        return df_std, df_hier
    except FileNotFoundError:
        return None, None

df_std_assign, df_hier_assign = load_data()

# ---------------------------------------------------------
# メイン画面
# ---------------------------------------------------------
st.title("タスクB：レビュー対象の表示")
st.markdown("""
### 手順
1. 下のボックスにあなたの **ユーザーID** を入力してください。  
2. 【お題（導入文）】と、それに続くストーリーが **3つ** 表示されます。
3. それぞれを読み、**クラウドワークスの作業画面に戻って** 回答を入力してください。
""") 
# ID入力フォーム
# 変数名を user_id にし、ラベルを「ユーザーID」に
user_id = st.text_input("ここにユーザーIDを入力 (半角数字)", "").strip()

# データ読み込みエラー時の警告
if df_std_assign is None or df_hier_assign is None:
    st.error("エラー：データファイルが読み込めません。")
    st.stop()

if user_id: 
    # --- グループ判定---
    std_row = df_std_assign[df_std_assign['Reviewer_ID'] == user_id]
    hier_row = df_hier_assign[df_hier_assign['Reviewer_ID'] == user_id]

    target_row = None

    if not std_row.empty:
        target_row = std_row.iloc[0]
    elif not hier_row.empty:
        target_row = hier_row.iloc[0]

    # --- 画面表示 ---
    if target_row is not None:
        st.success("確認できました。以下の3つのストーリーをレビューしてください。")

        st.write("---")

        # 3人分ループして表示
        for i in range(1, 4):
            story_col = f'Reviewee_{i}_Story'
            r_story = target_row[story_col]

            st.header(f"📖 ストーリー {i}")

            if str(r_story) == 'N/A' or pd.isna(r_story):
                st.warning("※ この項目のレビュー対象はありません（クラウドワークスの回答欄には「なし」と記入してください）")
            else:
                # ここから下がお題を表示する追加ロジック
                st.markdown("**【お題（導入文）】**")
                st.markdown(f"> {INTRO_TEXT}") # 引用表示で見やすくする

                st.markdown(f"**【ストーリー{i}の内容】**")
                st.success(r_story) # ストーリー本文を目立たせる

                st.caption(f"👆 読み終わったら、クラウドワークスの **ストーリー{i}に関するすべての設問（評価・記述）** に回答してください。")
                # ここまでが追加ロジック

            st.write("---")

    else:
        st.error("IDが見つかりません。入力ミスがないか確認してください。")
