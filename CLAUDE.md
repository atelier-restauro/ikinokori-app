# イキノコリ！ アプリ版 — 引き継ぎメモ

ゲーム全体の引き継ぎメモ（Claude Docs）：https://claude.ai/artifact/M1sETkR2ydo9xzApTqQKVt
公開ページ（ブラウザ版）：https://claude.ai/artifact/AEeNFzBgjey7HauZcF5oB2

## 守るルール
- 返事は日本語・フランクに。専門用語は言いかえる。
- 公開ページ（ブラウザ版）を書きかえるときは、毎回かいとに確認する。このリポジトリ（アプリ版）は確認なしで更新してよい（11/27 かいと）。
- パスワード・カード番号・鍵の中身はチャットに貼らせない。
- 更新ごとに TestFlight「テストの内容」と Play の `<ja-JP>` リリースノートを出す。
- コミットの最後に Co-Authored-By と Claude-Session の2行。

## 仕組み（Re:Museum と同じ）
- main に push → Codemagic が iOS（TestFlight へ自動で送る）と Android（aab）を自動ビルド。
- *.md・tools/・fonts/ だけの変更ではビルドしない（codemagic.yaml の changeset）。
- アプリID `jp.ikinokori.app`（変えられない）。ホーム画面の名前「イキノコリ！」。縦向きのみ・iPhoneのみ（iPadは不可）。
- iOS の署名は Re:Museum と同じやり方（ビルドのたびに配布用の証明書を作り直す）。App Store Connect の連携 `codemagic` を使う。
- Android の署名は Codemagic の鍵 `upload`（Re:Museum と共用）。versionCode は Codemagic のビルド番号そのまま。

## game.html の作り方
- 公開ページの HTML から `tools/make_app.py` で作る。ゲームそのものを直すときは、公開ページを直す → HTML を取り出す → これを通し直す、の順（アプリ版だけ直さない）。
  - 公開ページの HTML は claude-artifacts の read_file（paths に index.html）で取り出せる。
  - `python3 tools/make_app.py 公開ページ.html game.html`（fontTools と brotli が必要）
- アプリ版でやっていること：フォント（DotGothic16・M PLUS 1p、OFL）を使う文字だけにしぼって中に入れる／縦の画面いっぱい・ノッチよけ（env(safe-area-inset-*)。Android は MainActivity で切り欠きの分だけ下げる）／ランキングを出さず自分のベスト5／「ブラウザ」→「端末」／テスト版の番号（APP_VER）と「感想を送る」（FEEDBACK_URL、空なら出さない）。
- アイコン `icon.png`（1024・ドット絵64マスを16倍）、起動画面 `splash.png`（2732）。どちらもゲームの spr() で描いた。

## 状況
- 11/27：箱（このリポジトリ）を作成。game.html β0.1（2026-11-27 の公開版から）・ビルド設定・アイコン案A（地層と海、右上から隕石が落ちてくる。11/27 かいと決定）・起動画面。
- かいとの残り：Apple Developer でアプリID登録 → App Store Connect で新規App → Codemagic にこのリポジトリをつなぐ → 最初のビルド → Play Console で新規アプリ＋クローズドテスト。
- 友達テスト：3〜5人・iOS と Android のクローズドテスト。ランキングは試さない。Play で一般公開するには、このアプリで12人以上が14日続けてクローズドテストに参加している必要がある（アプリごと）。
- 「感想を送る」のGoogleフォームは、かいとが作ったら FEEDBACK_URL に入れる。

## 気をつけること（テストで見る）
- iOS の localStorage は消えることがある（Re:Museum は Filesystem にも保存して対策した）。テストで消えたら同じ対策を入れる。
- 系統の1枚絵の保存は、アプリでは「長押しで保存」の画面になる。保存できるか確認。
- iPhone のマナーモードでは音が鳴らない。
