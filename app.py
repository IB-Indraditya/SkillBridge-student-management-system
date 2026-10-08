import os, io, json, uuid, sqlite3, tempfile
import numpy as np, pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, abort
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key")
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
OUT = os.path.join(tempfile.gettempdir(), "skillbridge"); os.makedirs(OUT, exist_ok=True)

# Column roles are detected from header names, so any file layout works.
KEYS = {
    "placed": ["placed", "placement", "selected", "hired", "status", "outcome"],
    "salary": ["salary", "ctc", "package", "wage"],
    "score": ["score", "marks", "assessment", "grade", "percent"],
    "attendance": ["attendance"],
    "course": ["course", "trade", "program", "sector", "batch"],
    "source": ["source", "mobili", "channel", "referral"],
    "location": ["district", "city", "state", "location", "centre", "center"],
    "employer": ["employer", "company"],
}
YES = {"placed", "yes", "y", "1", "true", "selected", "hired", "employed"}

def find(df, role):
    for c in df.columns:
        if any(w in str(c).lower() for w in KEYS[role]):
            return c

def load(f):
    n = f.filename.lower()
    if n.endswith(".csv"):
        return {"data": pd.read_csv(f)}
    if n.endswith((".xlsx", ".xls")):
        return pd.read_excel(f, sheet_name=None)
    if n.endswith((".sql", ".db", ".sqlite")):
        con = sqlite3.connect(":memory:")
        if n.endswith(".sql"):
            con.executescript(f.read().decode("utf-8", "ignore"))
        else:
            p = os.path.join(OUT, uuid.uuid4().hex); f.save(p); con = sqlite3.connect(p)
        names = pd.read_sql("select name from sqlite_master where type='table'", con)["name"]
        return {t: pd.read_sql(f'select * from "{t}"', con) for t in names}
    raise ValueError("Use a .csv, .xlsx, .xls, .sql, .db or .sqlite file.")

def is_placed(s):
    return s.astype(str).str.strip().str.lower().isin(YES).astype(int)

def counts(s, top=8):
    v = s.astype(str).value_counts().head(top)
    return list(v.index), [int(x) for x in v.values]

def analyse(name, df):
    df = df.copy(); df.columns = [str(c).strip() for c in df.columns]
    dup = int(df.duplicated().sum()); df = df.drop_duplicates()
    R = {"name": name, "kpis": [], "charts": [], "insights": [], "ml": None, "table": None}
    R["kpis"] += [("Records", len(df)), ("Columns", df.shape[1]),
                  ("Missing cells", f"{df.isna().mean().mean()*100:.1f}%"), ("Duplicates removed", dup)]
    cols = {r: find(df, r) for r in KEYS}
    num = df.select_dtypes("number")
    y = None
    if cols["placed"]:
        p = df[cols["placed"]]
        y = is_placed(p) if not pd.api.types.is_numeric_dtype(p) or p.nunique() <= 2 else None
    if y is None and cols["salary"]:
        y = (pd.to_numeric(df[cols["salary"]], errors="coerce").fillna(0) > 0).astype(int)
    if y is not None:
        R["kpis"].insert(0, ("Placement rate", f"{y.mean()*100:.1f}%"))
        R["insights"].append(f"{int(y.sum())} of {len(y)} candidates are placed ({y.mean()*100:.1f}%).")
    for role, label in [("score", "Avg assessment score"), ("attendance", "Avg attendance"), ("salary", "Avg salary")]:
        c = cols[role]
        if c is not None and pd.api.types.is_numeric_dtype(df[c]):
            v = df[c][df[c] > 0].mean() if role == "salary" else df[c].mean()
            R["kpis"].append((label, f"{v:,.1f}"))
    for role, title in [("source", "Mobilisation by source"), ("location", "Candidates by location"),
                        ("course", "Enrolment by course"), ("employer", "Top employers")]:
        c = cols[role]
        if c is not None and 1 < df[c].nunique() < 200:
            l, v = counts(df[c]); R["charts"].append({"title": title, "type": "bar", "labels": l, "values": v})
    c = cols["course"]
    if y is not None and c is not None and 1 < df[c].nunique() < 200:
        g = (y.groupby(df[c]).mean() * 100).round(1).sort_values(ascending=False).head(8)
        R["charts"].append({"title": "Placement rate % by course", "type": "bar", "labels": [str(i) for i in g.index], "values": g.tolist()})
        R["insights"].append(f"Best converting course: {g.index[0]} ({g.iloc[0]}%); weakest: {g.index[-1]} ({g.iloc[-1]}%).")
    if y is not None:
        R["charts"].append({"title": "Placed vs not placed", "type": "doughnut", "labels": ["Placed", "Not placed"],
                            "values": [int(y.sum()), int(len(y) - y.sum())]})
    if cols["score"] is not None and pd.api.types.is_numeric_dtype(df[cols["score"]]):
        h, e = np.histogram(df[cols["score"]].dropna(), bins=8)
        R["charts"].append({"title": "Score distribution", "type": "bar",
                            "labels": [f"{e[i]:.0f}-{e[i+1]:.0f}" for i in range(len(h))], "values": h.tolist()})
    # ML: placement prediction, else clustering
    feats = df.drop(columns=[c for c in [cols["placed"], cols["salary"]] if c], errors="ignore")
    X = pd.DataFrame(index=feats.index)
    for c in feats.columns:
        if pd.api.types.is_numeric_dtype(feats[c]):
            X[c] = feats[c].fillna(feats[c].median())
        elif feats[c].nunique() <= 25:
            X[c] = feats[c].astype("category").cat.codes
    if y is not None and y.nunique() == 2 and len(df) >= 30 and X.shape[1]:
        k = int(max(2, min(5, y.value_counts().min())))
        rf = RandomForestClassifier(200, random_state=42, class_weight="balanced")
        proba = cross_val_predict(rf, X, y, cv=k, method="predict_proba")[:, 1]
        acc = accuracy_score(y, proba > 0.5); rf.fit(X, y)
        imp = pd.Series(rf.feature_importances_, X.columns).sort_values(ascending=False).head(8)
        idn = [c for c in df.columns if "name" in c.lower() or "id" in c.lower()][:2]
        risk = df.assign(placement_probability=(proba * 100).round(1))[y.eq(0)].sort_values("placement_probability").head(15)
        risk = risk[idn + [c for c in imp.index[:3] if c not in idn] + ["placement_probability"]]
        R["ml"] = {"kind": "Placement prediction (Random Forest)", "metric": f"Cross-validated accuracy {acc*100:.1f}%",
                   "importance": {"labels": list(imp.index), "values": [round(float(v) * 100, 1) for v in imp.values]}}
        R["table"] = {"title": "Unplaced candidates needing support first", "df": risk}
        R["insights"].append(f"Strongest placement drivers: {', '.join(imp.index[:3])}.")
    elif X.shape[1] >= 2 and len(df) >= 10:
        Z = (X - X.mean()) / X.std().replace(0, 1)
        km = KMeans(3, n_init=10, random_state=42).fit(Z.fillna(0))
        prof = X.assign(cluster=km.labels_).groupby("cluster").mean().round(2)
        prof.insert(0, "size", np.bincount(km.labels_))
        R["ml"] = {"kind": "Candidate segmentation (K-Means, 3 groups)", "metric": "No placement column found, so groups were discovered automatically",
                   "importance": None}
        R["table"] = {"title": "Segment profiles", "df": prof.reset_index()}
    if not num.empty:
        R["stats"] = num.describe().T.round(2).reset_index().rename(columns={"index": "column"})
    return R

def excel(rid, results):
    with pd.ExcelWriter(os.path.join(OUT, rid + ".xlsx")) as w:
        for i, R in enumerate(results):
            s = f"{i+1}_{R['name']}"[:25]
            pd.DataFrame(R["kpis"], columns=["Metric", "Value"]).to_excel(w, sheet_name=f"{s}_KPI", index=False)
            if R["table"]: R["table"]["df"].to_excel(w, sheet_name=f"{s}_Action", index=False)
            if "stats" in R: R["stats"].to_excel(w, sheet_name=f"{s}_Stats", index=False)

@app.route("/")
def index(): return render_template("index.html")

@app.route("/analyse", methods=["POST"])
def run():
    f = request.files.get("file")
    if not f or not f.filename:
        flash("Choose a file first."); return redirect(url_for("index"))
    try:
        sheets = load(f)
        results = [analyse(n, d) for n, d in sheets.items() if len(d) > 0]
        if not results: raise ValueError("The file has no rows.")
    except Exception as e:
        flash(f"Could not read the file: {e}"); return redirect(url_for("index"))
    rid = uuid.uuid4().hex[:12]
    excel(rid, results)
    for R in results:
        if R["table"]: R["table"]["html"] = R["table"].pop("df").to_html(index=False, classes="grid", border=0)
        if "stats" in R: R["stats"] = R["stats"].to_html(index=False, classes="grid", border=0)
    json.dump({"file": f.filename, "results": results}, open(os.path.join(OUT, rid + ".json"), "w"), default=str)
    return redirect(url_for("report", rid=rid))

@app.route("/report/<rid>")
def report(rid):
    p = os.path.join(OUT, os.path.basename(rid) + ".json")
    if not os.path.exists(p): abort(404)
    return render_template("report.html", rid=rid, **json.load(open(p)))

@app.route("/download/<rid>")
def download(rid):
    p = os.path.join(OUT, os.path.basename(rid) + ".xlsx")
    if not os.path.exists(p): abort(404)
    return send_file(p, as_attachment=True, download_name="skillbridge_report.xlsx")

if __name__ == "__main__":
    app.run(debug=True)
