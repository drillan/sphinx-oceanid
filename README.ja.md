# sphinx-oceanid

[beautiful-mermaid](https://github.com/niccolozy/beautiful-mermaid) を活用した、Sphinx 向け高品質 Mermaid ダイアグラム拡張機能。

## 特徴

- **beautiful-mermaid レンダリング** — ELK.js ベースのレイアウトエンジンによる高品質 SVG 出力
- **CSS 変数テーマ** — ダーク/ライトテーマの自動検出と即時切替（再レンダリング不要）
- **ゼロコンフィグ** — CDN 配信の beautiful-mermaid で追加設定なしに動作
- **sphinx-revealjs 対応** — IntersectionObserver による非表示スライドの遅延レンダリング
- **パン＆ズーム** — ネイティブ Pointer Events + SVG transform を使用（d3.js 不要）
- **フルスクリーンモーダル** — ビューポートサイズのオーバーレイでダイアグラムを表示
- **外部ファイル対応** — インラインコードの代わりに `.mmd` ファイルを参照可能
- **クラスダイアグラム自動生成** — Python コードからクラス階層図を自動生成

## 対応ダイアグラムタイプ

| タイプ | エイリアス |
|--------|------------|
| `flowchart` | `graph` |
| `sequenceDiagram` | |
| `classDiagram` | |
| `stateDiagram` | `stateDiagram-v2` |
| `erDiagram` | |
| `xychart-beta` | |

非対応のダイアグラムタイプには明示的な警告（またはエラー）が出力されます。無音での劣化は発生しません。

## インストール

sphinx-oceanid は Python 3.13 以上が必要です。

GitHub から直接インストール：

```bash
pip install git+https://github.com/drillan/sphinx-oceanid.git
```

またはリポジトリをクローンしてローカルインストール：

```bash
git clone https://github.com/drillan/sphinx-oceanid.git
cd sphinx-oceanid
pip install .
```

## クイックスタート

`conf.py` に拡張機能を追加します：

```python
extensions = ["sphinx_oceanid"]
```

reStructuredText ファイルで `mermaid` ディレクティブを使用します：

```rst
.. mermaid::

   flowchart LR
     A[開始] --> B[処理] --> C[終了]
```

Markdown（MyST）ファイルの場合：

````markdown
```{mermaid}
sequenceDiagram
  Alice->>Bob: Hello
  Bob-->>Alice: Hi!
```
````

## 設定

すべての設定オプションは `conf.py` で `oceanid_` プレフィックスを使用します：

```python
# conf.py
extensions = ["sphinx_oceanid"]

# テーマ（デフォルト: "auto" — Sphinx テーマからダーク/ライトを検出）
oceanid_theme = "auto"
oceanid_theme_dark = "zinc-dark"
oceanid_theme_light = "zinc-light"

# 全ダイアグラムでズームを有効化（デフォルト: False）
oceanid_zoom = True

# フルスクリーンモーダルを有効化（デフォルト: False）
oceanid_fullscreen = True

# 非対応ダイアグラムタイプへの対応: "warning" または "error"（デフォルト: "warning"）
oceanid_unsupported_action = "warning"
```

## ディレクティブオプション

```rst
.. mermaid::
   :name: my-diagram
   :alt: アクセシビリティ用の説明文
   :align: center
   :caption: ダイアグラムのキャプション（<figcaption> としてレンダリング）
   :title: Mermaid ネイティブタイトル（ダイアグラム内部に表示）
   :zoom:
   :config: {"theme": "forest"}

   flowchart LR
     A --> B --> C
```

## クラスダイアグラム自動生成

Python コードからクラス階層図を自動生成します：

```rst
.. autoclasstree:: mypackage.MyClass
   :full:
   :namespace: mypackage
   :caption: クラス階層
```

## ドキュメント

詳細なドキュメントは [docs/](docs/) ディレクトリを参照してください。

## ライセンス

BSD-3-Clause。詳細は [LICENSE](LICENSE) を参照してください。
