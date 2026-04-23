import tkinter as tk
from tkinter import ttk
import math

# ==========================================
# 1. MODEL: Gul konfiguratsiyasi (Class)
# ==========================================
class FlowerConfig:
    """Gul turi, rangi va parametrlarini boshqaruvchi obyekt"""
    DEFAULT_COLOR = "#FF6B8B"
    DEFAULT_CENTER = "#FFD166"
    DEFAULT_PETALS = 6

    def __init__(self, name: str):
        self.name = name.strip().lower()
        self.color, self.petal_count, self.center_color = self._resolve_config()

    def _resolve_config(self):
        """Kiritilgan nomga mos rang va gul parametrlarini aniqlash"""
        configs = {
            'atirgul': ("#E63946", 5, "#F4A261"),
            'rose': ("#E63946", 5, "#F4A261"),
            'lola': ("#FF9F1C", 6, "#2B2D42"),
            'tulip': ("#FF9F1C", 6, "#2B2D42"),
            'kungaboqar': ("#FFD166", 12, "#6B4226"),
            'sunflower': ("#FFD166", 12, "#6B4226"),
            'binafsha': ("#9B5DE5", 5, "#FEE440"),
            'violet': ("#9B5DE5", 5, "#FEE440"),
            'romashka': ("#F8F9FA", 8, "#FFD166"),
            'daisy': ("#F8F9FA", 8, "#FFD166"),
        }
        for key, val in configs.items():
            if key in self.name or self.name in key:
                return val
        return self.DEFAULT_COLOR, self.DEFAULT_PETALS, self.DEFAULT_CENTER


# ==========================================
# 2. BOSHQARUV: O'sish bosqichlari (Class)
# ==========================================
class GrowthModel:
    """O'sish jarayonini 0.0 dan 1.0 gacha progress orqali boshqaradi"""
    STAGES = [
        "Urug' va tuproqda",
        "Nish chiqishi",
        "Poya o'sishi",
        "Barglar paydo bo'lishi",
        "G'uncha hosil bo'lishi",
        "Gul to'liq ochilishi"
    ]

    def __init__(self):
        self.progress = 0.0
        self.current_stage_idx = 0

    def update(self, step: float) -> bool:
        self.progress = min(1.0, self.progress + step)
        thresholds = [0.0, 0.15, 0.35, 0.55, 0.75, 0.90]
        for i, t in enumerate(thresholds):
            if self.progress >= t:
                self.current_stage_idx = min(i, len(self.STAGES) - 1)
        return self.progress >= 1.0

    def get_stage_name(self) -> str:
        return self.STAGES[self.current_stage_idx]

    def get_visual_params(self) -> dict:
        """Progressga qarab ko'rsatkichlarni hisoblash"""
        p = self.progress
        return {
            "stem_height": max(0, (p - 0.1) / 0.7) * 260,
            "leaf_size": max(0, min(1, (p - 0.35) / 0.2)) * 30,
            "bud_size": max(0, min(1, (p - 0.55) / 0.15)) * 18,
            "bloom_scale": max(0, min(1, (p - 0.75) / 0.25)),
            "soil_wetness": max(0, 1 - p * 2)
        }


# ==========================================
# 3. KO'RINISH: Canvas chizish (Class)
# ==========================================
class FlowerCanvas:
    CANVAS_W = 600
    CANVAS_H = 520
    BASE_Y = 480  # Tuproq ustidagi nuqta

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.canvas.config(bg="#F8F9FA", highlightthickness=0, width=self.CANVAS_W, height=self.CANVAS_H)
        self._draw_initial_scene()

    def _draw_initial_scene(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, self.BASE_Y + 15, self.CANVAS_W, self.CANVAS_H, fill="#7A5C43", outline="")
        self.canvas.create_oval(self.CANVAS_W//2 - 8, self.BASE_Y - 5, self.CANVAS_W//2 + 8, self.BASE_Y + 10, fill="#8B5A2B", outline="#5C3A1A")

    def clear(self):
        self.canvas.delete("all")

    def draw(self, config: FlowerConfig, params: dict):
        self.clear()
        self._draw_background()
        self._draw_soil(params)
        if params["stem_height"] > 2:
            cx = self.CANVAS_W // 2
            self._draw_stem(cx, params)
            self._draw_leaves(cx, config, params)
            self._draw_bud(cx, config, params)
            self._draw_petals(cx, config, params)

    def _draw_background(self):
        self.canvas.create_rectangle(0, 0, self.CANVAS_W, self.BASE_Y + 15, fill="#E8F0F2", outline="")

    def _draw_soil(self, params):
        wet = params["soil_wetness"]
        r = int(90 + wet * 30)
        g = int(65 + wet * 20)
        b = int(40 + wet * 10)
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.canvas.create_rectangle(0, self.BASE_Y + 15, self.CANVAS_W, self.CANVAS_H, fill=color, outline="")
        if params["stem_height"] < 5:
            self.canvas.create_oval(self.CANVAS_W//2 - 6, self.BASE_Y - 2, self.CANVAS_W//2 + 6, self.BASE_Y + 8, fill="#8B5A2B", outline="#5C3A1A")

    def _draw_stem(self, cx, params):
        h = params["stem_height"]
        top_y = self.BASE_Y - h
        thickness = 4 + h / 60
        self.canvas.create_line(cx, self.BASE_Y, cx, top_y, fill="#2D6A4F", width=thickness, capstyle=tk.ROUND)

    def _draw_leaves(self, cx, config, params):
        size = params["leaf_size"]
        if size <= 3: return
        h = params["stem_height"]
        for i, ratio in enumerate([0.3, 0.6]):
            ly = self.BASE_Y - h * ratio
            lx = cx + (18 if i == 0 else -18)
            angle = 0.4 if i == 0 else -0.4
            self._draw_leaf(lx, ly, size, angle)

    def _draw_leaf(self, x, y, size, angle):
        # Soddalashtirilgan va barqaror barg chizish
        pts = []
        for t in range(-20, 21, 2):
            rad = math.radians(t + angle * 90)
            r = size * (0.9 + 0.1 * math.cos(rad))
            pts.append(x + r * math.cos(rad))
            pts.append(y + r * math.sin(rad) * 0.5)
        self.canvas.create_polygon(pts, fill="#52B788", outline="#2D6A4F", smooth=True)

    def _draw_bud(self, cx, config, params):
        b_size = params["bud_size"]
        if b_size <= 2: return
        top_y = self.BASE_Y - params["stem_height"]
        self.canvas.create_oval(cx - b_size, top_y - b_size, cx + b_size, top_y + b_size,
                                fill=config.color, outline="#C1121F", width=2)

    def _draw_petals(self, cx, config, params):
        bloom = params["bloom_scale"]
        if bloom <= 0: return
        top_y = self.BASE_Y - params["stem_height"]
        r_base = 12 + bloom * 35
        
        for i in range(config.petal_count):
            angle = (360 / config.petal_count) * i
            rad = math.radians(angle)
            # Uch nuqtasi
            tx = cx + r_base * 1.3 * math.cos(rad)
            ty = top_y + r_base * 1.3 * math.sin(rad)
            # Kengligi
            perp = math.radians(angle + 90)
            w = r_base * 0.25
            lx = tx + w * math.cos(perp)
            ly = ty + w * math.sin(perp)
            rx = tx - w * math.cos(perp)
            ry = ty - w * math.sin(perp)
            
            pts = [cx, top_y, lx, ly, tx, ty, rx, ry]
            self.canvas.create_polygon(pts, fill=config.color, outline="#A4133C", width=1, smooth=True)

        # Markaz
        sz = 8 * bloom
        self.canvas.create_oval(cx - sz, top_y - sz, cx + sz, top_y + sz,
                                fill=config.center_color, outline="#D4A373")


# ==========================================
# 4. INTERFEYS: Asosiy dastur (Class)
# ==========================================
class FlowerSimulatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🌱 Gul O'sishi Simulyatori")
        self.root.geometry("920x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F2F5")

        self.config = None
        self.model = GrowthModel()
        self.renderer = None
        self.anim_id = None
        self.is_running = False

        self._setup_style()
        self._build_ui()

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#F0F2F5")
        style.configure("TLabel", background="#F0F2F5", font=("Arial", 10))
        style.configure("Title.TLabel", font=("Arial", 14, "bold"), foreground="#1D3557")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=(12, 6))
        style.configure("Accent.TButton", background="#457B9D", foreground="white")
        style.map("Accent.TButton", background=[("active", "#1D3557")])
        style.configure("TProgressbar", thickness=10, background="#2A9D8F")
        style.configure("Status.TLabel", font=("Arial", 9, "italic"), foreground="#555")

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="🌸 Gul O'sishi Simulyatori (OOP + Tkinter)", style="Title.TLabel").pack(pady=(0, 10))

        content = ttk.Frame(main_frame)
        content.pack(fill=tk.BOTH, expand=True)

        # Chap: Canvas
        canvas_frame = ttk.Frame(content, relief="solid", borderwidth=1)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.canvas = tk.Canvas(canvas_frame, width=600, height=520, bg="#E8F0F2")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.renderer = FlowerCanvas(self.canvas)

        # O'ng: Panel
        panel = ttk.Frame(content, width=260)
        panel.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        ttk.Label(panel, text="Gul nomi:").pack(anchor="w", pady=(5, 2))
        self.entry = ttk.Entry(panel, font=("Arial", 10), width=22)
        self.entry.pack(fill=tk.X, pady=(0, 12))
        self.entry.insert(0, "atirgul")

        btn_frame = ttk.Frame(panel)
        btn_frame.pack(fill=tk.X, pady=5)
        self.start_btn = ttk.Button(btn_frame, text="▶ Boshlash", style="Accent.TButton", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        self.reset_btn = ttk.Button(btn_frame, text="↺ Qayta", command=self.reset_simulation)
        self.reset_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.progress = ttk.Progressbar(panel, orient="horizontal", length=240, mode="determinate")
        self.progress.pack(fill=tk.X, pady=12)

        self.stage_label = ttk.Label(panel, text="Bosqich: Tayyor")
        self.stage_label.pack(anchor="w", pady=(5, 8))

        self.info_text = tk.Text(panel, height=6, font=("Consolas", 9), bg="#FFFFFF", relief="flat", wrap=tk.WORD)
        self.info_text.pack(fill=tk.X, pady=5)
        self.info_text.insert(tk.END, "💡 'atirgul', 'lola', 'kungaboqar' kabi nomlarni kiriting.")
        self.info_text.configure(state="disabled")

        self.status_bar = ttk.Label(main_frame, text="Tayyor. Gul nomini kiriting va 'Boshlash' tugmasini bosing.", style="Status.TLabel")
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.start_simulation())

    def start_simulation(self):
        if self.is_running:
            return
        name = self.entry.get().strip()
        if not name:
            self.status_bar.config(text="⚠️ Iltimos, gul nomini kiriting!")
            return

        self.config = FlowerConfig(name)
        self.model = GrowthModel()
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.status_bar.config(text=f"🌱 '{self.config.name.title()}' o'stirish boshlandi...")
        
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"📝 Gul: {self.config.name.title()}\n🎨 Rang: {self.config.color}\n🌸 Barglar: {self.config.petal_count}\n⏳ Jarayon boshlandi...")
        self.info_text.configure(state="disabled")

        self._animate_step()

    def _animate_step(self):
        if not self.is_running:
            return
        try:
            finished = self.model.update(0.008)
            self.progress["value"] = self.model.progress * 100
            self.stage_label.config(text=f"Bosqich: {self.model.get_stage_name()}")
            self.renderer.draw(self.config, self.model.get_visual_params())

            if finished:
                self.is_running = False
                self.start_btn.config(state="normal")
                self.status_bar.config(text="✅ Gul muvaffaqiyatli ochildi! 🎉")
                self.info_text.configure(state="normal")
                self.info_text.insert(tk.END, "\n✅ O'sish tugallandi!")
                self.info_text.configure(state="disabled")
            else:
                self.anim_id = self.root.after(45, self._animate_step)
        except Exception as e:
            self.is_running = False
            self.status_bar.config(text=f"❌ Xatolik: {str(e)}")

    def reset_simulation(self):
        self.is_running = False
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
        self.start_btn.config(state="normal")
        self.progress["value"] = 0
        self.stage_label.config(text="Bosqich: Tayyor")
        self.status_bar.config(text="Simulyator qayta ishga tushirildi.")
        self.renderer.clear()
        self.renderer._draw_initial_scene()
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, "💡 'atirgul', 'lola', 'kungaboqar' kabi nomlarni kiriting.")
        self.info_text.configure(state="disabled")


# ==========================================
# DASTURNI ISHGA TUSHIRISH
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = FlowerSimulatorApp(root)
    root.mainloop()