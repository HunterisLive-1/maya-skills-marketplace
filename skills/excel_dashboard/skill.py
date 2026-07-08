"""Excel Dashboard — build a self-contained HTML dashboard from an .xlsx/.csv file.

stdin: full path to the data file (e.g. C:/Users/x/sales.xlsx).
Output: maya_dashboard_<name>.html on the Desktop, opened in the browser.
Needs pandas (+ openpyxl for .xlsx) — Maya's environment ships both.
"""
import html
import os
import sys
from pathlib import Path

ACCENT = "#2a78d6"  # validated single-series hue
INK, MUTED, GRID = "#1d232b", "#6b7684", "#e6e9ee"


def esc(v) -> str:
    return html.escape(str(v))


def load_frame(path: Path):
    import pandas as pd
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)


def bar_chart_svg(labels, values) -> str:
    """Horizontal bars: single hue, thin marks, 2px gaps, muted value labels."""
    if not len(values):
        return ""
    vmax = max(values) or 1
    bar_h, gap, label_w, chart_w = 22, 8, 170, 420
    rows = []
    for i, (lab, val) in enumerate(zip(labels, values)):
        y = i * (bar_h + gap)
        w = max(2, val / vmax * (chart_w - 70))
        rows.append(
            f'<text x="{label_w - 8}" y="{y + bar_h / 2 + 4}" text-anchor="end" '
            f'font-size="12" fill="{INK}">{esc(str(lab)[:24])}</text>'
            f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="3" fill="{ACCENT}"/>'
            f'<text x="{label_w + w + 6}" y="{y + bar_h / 2 + 4}" font-size="11" '
            f'fill="{MUTED}">{val:,.0f}</text>'
        )
    height = len(values) * (bar_h + gap)
    return (f'<svg viewBox="0 0 {label_w + chart_w} {height}" width="100%" '
            f'style="max-width:640px">{"".join(rows)}</svg>')


def main():
    raw = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    if not raw:
        print("Excel Dashboard ready. stdin par file ka full path bhejo (.xlsx ya .csv).")
        print("Example: C:/Users/hunte/Documents/sales.xlsx")
        return

    path = Path(raw.strip().strip('"'))
    if not path.is_file():
        print(f"File nahi mili: {path}")
        return

    try:
        df = load_frame(path)
    except ImportError as e:
        print(f"Library missing ({e}) — 'pip install pandas openpyxl' chahiye.")
        return
    except Exception as e:
        print(f"File read nahi hui: {e}")
        return
    if df.empty:
        print("File khaali hai — dashboard banane ke liye data chahiye.")
        return

    num_cols = df.select_dtypes("number").columns.tolist()
    txt_cols = [c for c in df.columns if c not in num_cols]

    # Stat tiles: rows, columns + sum/avg of first numeric column
    tiles = [("Rows", f"{len(df):,}"), ("Columns", str(len(df.columns)))]
    if num_cols:
        s = df[num_cols[0]]
        tiles += [(f"Total {num_cols[0]}", f"{s.sum():,.0f}"),
                  (f"Avg {num_cols[0]}", f"{s.mean():,.1f}")]
    tiles_html = "".join(
        f'<div class="tile"><div class="tile-val">{esc(v)}</div>'
        f'<div class="tile-label">{esc(k)}</div></div>' for k, v in tiles)

    # Chart: first numeric column summed by first text column (top 10)
    chart_html = ""
    if num_cols and txt_cols:
        top = (df.groupby(txt_cols[0], dropna=True)[num_cols[0]]
                 .sum().sort_values(ascending=False).head(10))
        chart_html = (f'<div class="panel"><h2>{esc(num_cols[0])} by {esc(txt_cols[0])} '
                      f'<span class="sub">(top {len(top)})</span></h2>'
                      + bar_chart_svg(top.index.tolist(), top.values.tolist()) + "</div>")

    # Data preview table (first 15 rows) — the accessible fallback for the chart
    head = df.head(15)
    table = ("<table><thead><tr>" + "".join(f"<th>{esc(c)}</th>" for c in head.columns)
             + "</tr></thead><tbody>"
             + "".join("<tr>" + "".join(f"<td>{esc(v)}</td>" for v in row) + "</tr>"
                       for row in head.itertuples(index=False))
             + "</tbody></table>")

    page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Dashboard — {esc(path.stem)}</title><style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f7fa; color: {INK};
       margin: 0; padding: 28px; }}
h1 {{ font-size: 22px; margin: 0 0 4px 0; }}
.sub {{ color: {MUTED}; font-size: 12px; font-weight: 400; }}
.tiles {{ display: flex; gap: 14px; flex-wrap: wrap; margin: 18px 0; }}
.tile {{ background: #fff; border: 1px solid {GRID}; border-radius: 10px;
        padding: 14px 22px; min-width: 130px; }}
.tile-val {{ font-size: 24px; font-weight: 600; color: {ACCENT}; }}
.tile-label {{ font-size: 11px; color: {MUTED}; letter-spacing: 0.4px; margin-top: 2px; }}
.panel {{ background: #fff; border: 1px solid {GRID}; border-radius: 10px;
         padding: 18px 22px; margin-bottom: 18px; overflow-x: auto; }}
h2 {{ font-size: 14px; margin: 0 0 14px 0; }}
table {{ border-collapse: collapse; font-size: 12px; width: 100%; }}
th {{ text-align: left; color: {MUTED}; font-weight: 600; padding: 6px 10px;
     border-bottom: 2px solid {GRID}; }}
td {{ padding: 5px 10px; border-bottom: 1px solid {GRID}; }}
</style></head><body>
<h1>{esc(path.stem)} <span class="sub">· dashboard by Maya</span></h1>
<div class="tiles">{tiles_html}</div>
{chart_html}
<div class="panel"><h2>Data preview <span class="sub">(first {len(head)} rows)</span></h2>{table}</div>
</body></html>"""

    desktop = Path.home() / "Desktop"
    desktop.mkdir(exist_ok=True)
    out = desktop / f"maya_dashboard_{path.stem[:40]}.html"
    out.write_text(page, encoding="utf-8")
    print(f"Dashboard ban gaya: {out}")
    try:
        os.startfile(out)  # noqa: S606 — intended: open in default browser
        print("Browser mein khol diya.")
    except OSError:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Dashboard error: {e}")
