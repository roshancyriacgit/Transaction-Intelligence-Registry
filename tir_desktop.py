\
import json, pathlib, tkinter as tk
from tkinter import ttk, messagebox, filedialog

from engine.kb_loader import load_kb
from engine.classifier import classify
from engine.selector import select_applicable
from engine.sequencer import sequence_steps
from engine.synthesizer import synthesize

ROOT = pathlib.Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "kb"
CASE_DIR = ROOT / "storage" / "cases"
OUT_DIR  = ROOT / "storage" / "outputs"

TX_TYPES = ["sale","purchase","investment","loan","lease","license","assignment","merger","service"]
ASSET_CLASSES = ["money","shares","securities","immovable_property","movable_goods","services","ip_rights","hybrid"]
PARTY_TYPES = ["individual","company","llp","partnership","trust","govt","foreign_entity"]
TIMING = ["instant","staged","conditional","ongoing"]

def pretty(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TIR — Offline Desktop Reference (Illustrative)")
        self.geometry("1100x700")
        self.kb = load_kb(str(KB_DIR))
        self.parties = []
        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        left = ttk.Frame(paned, padding=10)
        right = ttk.Frame(paned, padding=10)
        paned.add(left, weight=1)
        paned.add(right, weight=3)

        ttk.Label(left, text="Transaction Intake", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,8))

        self.var_case_id = tk.StringVar(value="DEMO-CASE-001")
        self.var_tx_type = tk.StringVar(value="investment")
        self.var_asset = tk.StringVar(value="shares")
        self.var_state = tk.StringVar(value="Maharashtra")
        self.var_city = tk.StringVar(value="Mumbai")
        self.var_timing = tk.StringVar(value="staged")

        self._field(left, "Case ID", self.var_case_id)
        self._combo(left, "Transaction Type", self.var_tx_type, TX_TYPES)
        self._combo(left, "Asset Class", self.var_asset, ASSET_CLASSES)
        self._location(left)
        self._combo(left, "Timing", self.var_timing, TIMING)

        ttk.Separator(left).pack(fill="x", pady=10)
        ttk.Label(left, text="Parties", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,6))
        self._party_editor(left)

        ttk.Separator(left).pack(fill="x", pady=10)
        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=4)
        ttk.Button(btns, text="Run TIR", command=self.run_tir).pack(side="left", fill="x", expand=True)
        ttk.Button(btns, text="Save Case", command=self.save_case).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(btns, text="Load Case", command=self.load_case).pack(side="left", fill="x", expand=True)

        ttk.Separator(left).pack(fill="x", pady=10)
        ttk.Label(left, text="KB Search (Offline)", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,6))
        self.var_search = tk.StringVar()
        srow = ttk.Frame(left)
        srow.pack(fill="x")
        ttk.Entry(srow, textvariable=self.var_search).pack(side="left", fill="x", expand=True)
        ttk.Button(srow, text="Search", command=self.search_kb).pack(side="left", padx=6)
        self.search_results = tk.Listbox(left, height=10)
        self.search_results.pack(fill="both", expand=True, pady=(6,0))
        self.search_results.bind("<<ListboxSelect>>", self.open_selected_rule)

        ttk.Label(right, text="Outputs", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,8))
        self.tabs = ttk.Notebook(right)
        self.tabs.pack(fill="both", expand=True)

        self.txt_snapshot = self._add_tab("Snapshot")
        self.txt_structure = self._add_tab("Structure Options")
        self.txt_steps = self._add_tab("Execution Plan")
        self.txt_filings = self._add_tab("Filings")
        self.txt_record = self._add_tab("TIR Record")
        self.txt_rule = self._add_tab("KB Rule Detail")

        # default parties
        self.parties = [
            {"role":"Investor","name":"Alpha Ventures","party_type":"foreign_entity"},
            {"role":"Issuer","name":"Beta Private Limited","party_type":"company"},
        ]
        self.refresh_party_list()

    def _add_tab(self, name):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=name)
        txt = tk.Text(frame, wrap="word")
        txt.pack(fill="both", expand=True)
        txt.configure(font=("Consolas", 10))
        return txt

    def _field(self, parent, label, var):
        f = ttk.Frame(parent)
        f.pack(fill="x", pady=4)
        ttk.Label(f, text=label).grid(row=0, column=0, sticky="w")
        ttk.Entry(f, textvariable=var).grid(row=1, column=0, sticky="ew")
        f.columnconfigure(0, weight=1)

    def _combo(self, parent, label, var, values):
        f = ttk.Frame(parent)
        f.pack(fill="x", pady=4)
        ttk.Label(f, text=label).grid(row=0, column=0, sticky="w")
        ttk.Combobox(f, values=values, textvariable=var, state="readonly").grid(row=1, column=0, sticky="ew")
        f.columnconfigure(0, weight=1)

    def _location(self, parent):
        f = ttk.Frame(parent)
        f.pack(fill="x", pady=4)
        ttk.Label(f, text="Location (State, City)").grid(row=0, column=0, sticky="w")
        sub = ttk.Frame(f)
        sub.grid(row=1, column=0, sticky="ew")
        ttk.Entry(sub, textvariable=self.var_state, width=18).pack(side="left", fill="x", expand=True)
        ttk.Entry(sub, textvariable=self.var_city, width=18).pack(side="left", fill="x", expand=True, padx=(6,0))
        f.columnconfigure(0, weight=1)

    def _party_editor(self, parent):
        frm = ttk.Frame(parent)
        frm.pack(fill="x")
        self.var_role = tk.StringVar(value="party")
        self.var_pname = tk.StringVar(value="")
        self.var_ptype = tk.StringVar(value=PARTY_TYPES[0])

        ttk.Label(frm, text="Role").grid(row=0, column=0, sticky="w")
        ttk.Label(frm, text="Name").grid(row=0, column=1, sticky="w")
        ttk.Label(frm, text="Type").grid(row=0, column=2, sticky="w")

        ttk.Entry(frm, textvariable=self.var_role, width=10).grid(row=1, column=0, sticky="ew")
        ttk.Entry(frm, textvariable=self.var_pname, width=20).grid(row=1, column=1, sticky="ew", padx=6)
        ttk.Combobox(frm, values=PARTY_TYPES, textvariable=self.var_ptype, state="readonly", width=16).grid(row=1, column=2, sticky="ew")

        ttk.Button(frm, text="Add", command=self.add_party_from_fields).grid(row=1, column=3, padx=6)
        frm.columnconfigure(1, weight=1)

        self.party_list = tk.Listbox(parent, height=7)
        self.party_list.pack(fill="x", pady=(6,0))
        ttk.Button(parent, text="Remove Selected", command=self.remove_selected_party).pack(anchor="w", pady=(6,0))

    def add_party_from_fields(self):
        role = self.var_role.get().strip() or "party"
        name = self.var_pname.get().strip()
        ptype = self.var_ptype.get().strip()
        if not name:
            messagebox.showwarning("Missing", "Party name required.")
            return
        self.parties.append({"role": role, "name": name, "party_type": ptype})
        self.var_pname.set("")
        self.refresh_party_list()

    def remove_selected_party(self):
        sel = self.party_list.curselection()
        if not sel:
            return
        self.parties.pop(sel[0])
        self.refresh_party_list()

    def refresh_party_list(self):
        self.party_list.delete(0, tk.END)
        for p in self.parties:
            self.party_list.insert(tk.END, f"{p['role']}: {p['name']} [{p['party_type']}]")

    def build_intake(self):
        return {
            "case_id": self.var_case_id.get().strip() or "CASE",
            "transaction": {
                "transaction_type": self.var_tx_type.get(),
                "asset_class": self.var_asset.get(),
                "parties": self.parties,
                "location": {"state": self.var_state.get().strip(), "city": self.var_city.get().strip()},
                "timing": self.var_timing.get(),
                "notes": ""
            }
        }

    def run_tir(self):
        intake = self.build_intake()
        c = classify(intake)
        applicable = select_applicable(self.kb["rules"], c)
        steps = sequence_steps(applicable)
        out = synthesize(intake["case_id"], intake, c, applicable, steps)

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUT_DIR / f"{intake['case_id']}_output.json"
        out_path.write_text(pretty(out), encoding="utf-8")

        self.txt_snapshot.delete("1.0", tk.END)
        self.txt_snapshot.insert(tk.END, pretty({"case_id": intake["case_id"], "classification": out["classification"], "intent": out["intent"]}))
        self.txt_structure.delete("1.0", tk.END); self.txt_structure.insert(tk.END, pretty(out["structure_options"]))
        self.txt_steps.delete("1.0", tk.END); self.txt_steps.insert(tk.END, pretty(out["execution_plan"]))
        self.txt_filings.delete("1.0", tk.END); self.txt_filings.insert(tk.END, pretty(out["filings_checklist"]))
        self.txt_record.delete("1.0", tk.END); self.txt_record.insert(tk.END, pretty(out["tir_record"]))

        messagebox.showinfo("Done", f"Output saved locally:\\n{out_path}")

    def save_case(self):
        intake = self.build_intake()
        CASE_DIR.mkdir(parents=True, exist_ok=True)
        path = CASE_DIR / f"{intake['case_id']}.json"
        path.write_text(pretty(intake), encoding="utf-8")
        messagebox.showinfo("Saved", f"Case saved:\\n{path}")

    def load_case(self):
        CASE_DIR.mkdir(parents=True, exist_ok=True)
        file_path = filedialog.askopenfilename(
            title="Open Case",
            initialdir=str(CASE_DIR),
            filetypes=[("JSON case files","*.json"),("All files","*.*")]
        )
        if not file_path:
            return
        intake = json.loads(pathlib.Path(file_path).read_text(encoding="utf-8"))
        t = intake["transaction"]
        self.var_case_id.set(intake.get("case_id","CASE"))
        self.var_tx_type.set(t.get("transaction_type", TX_TYPES[0]))
        self.var_asset.set(t.get("asset_class", ASSET_CLASSES[0]))
        self.var_state.set(t.get("location",{}).get("state",""))
        self.var_city.set(t.get("location",{}).get("city",""))
        self.var_timing.set(t.get("timing", TIMING[0]))
        self.parties = t.get("parties", [])
        self.refresh_party_list()
        messagebox.showinfo("Loaded", f"Loaded case:\\n{file_path}")

    def search_kb(self):
        q = (self.var_search.get() or "").strip().lower()
        self.search_results.delete(0, tk.END)
        if not q:
            return
        matches = []
        for r in self.kb["rules"]:
            hay = " ".join([r.get("id",""), r.get("title",""), r.get("domain",""), r.get("trigger","")]).lower()
            if q in hay:
                matches.append(r)
        for r in matches:
            self.search_results.insert(tk.END, f"{r['id']} | {r['domain']} | {r['title']}")
        self._kb_matches = matches

    def open_selected_rule(self, _evt=None):
        sel = self.search_results.curselection()
        if not sel:
            return
        r = getattr(self, "_kb_matches", [])[sel[0]]
        self.txt_rule.delete("1.0", tk.END)
        self.txt_rule.insert(tk.END, pretty(r))
        self.tabs.select(self.txt_rule.master)

if __name__ == "__main__":
    App().mainloop()
