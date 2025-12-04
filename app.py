import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# アプリの設定
# ---------------------------------------------------------
st.set_page_config(page_title="タスクB：レビュー対象の確認", layout="centered")

# ---------------------------------------------------------
# データの読み込み関数
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
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
1. 下のボックスにあなたの **Worker ID** を入力してください。
2. あなたがレビューすべき **3つのストーリー** が表示されます。
3. ストーリーを読み、**クラウドワークスの作業画面に戻って**、それぞれのレビューを入力してください。
""")

# ID入力フォーム
worker_id = st.text_input("ここにWorker IDを入力 (半角数字)", "").strip()

# データ読み込みエラー時の警告
if df_std_assign is None or df_hier_assign is None:
    st.error("エラー：データファイルが読み込めません。")
    st.stop()

if worker_id:
    # --- グループ判定 ---
    std_row = df_std_assign[df_std_assign['Reviewer_ID'] == worker_id]
    hier_row = df_hier_assign[df_hier_assign['Reviewer_ID'] == worker_id]

    target_row = None

    if not std_row.empty:
        target_row = std_row.iloc[0]
    elif not hier_row.empty:
        target_row = hier_row.iloc[0]

    # --- 画面表示 ---
    if target_row is not None:
        st.success("確認できました。以下の3つのストーリーをレビューしてください。")
        st.warning("※ レビューはここではなく、クラウドワークスの回答欄に入力してください。")

        st.write("---")

        # 3人分ループして表示
        for i in range(1, 4):
            story_col = f'Reviewee_{i}_Story'
            r_story = target_row[story_col]

            st.header(f"📖 ストーリー {i}")

            if str(r_story) == 'N/A' or pd.isna(r_story):
                st.info("※ この項目のレビュー対象はありません（回答欄には「なし」と記入してください）")
            else:
                # ストーリーを表示（コピーしやすいようにcodeブロックやtext_areaを使う手もありますが、読みやすさ重視でinfoにします）
                st.info(r_story)

                # ワーカーへの誘導
                st.caption(f"👆 この内容を読み、クラウドワークスの「ストーリー{i}のレビュー」欄に感想を書いてください。")

            st.write("---")

    else:
        st.error("IDが見つかりません。入力ミスがないか確認してください。")
