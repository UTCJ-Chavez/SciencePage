import math
import random
import tkinter as tk

# Game list initialized directly from your selection
GAMES = [
    "Thems Fighting Herds",
    "DNF Duel",
    "Samurai Shodown (2019)",
    "King of Fighters XV",
    "King of Fighters '98 UM",
    "King of Fighters 2002 UM",
    "Fatal Fury: COTW",
    "Tekken 7",
    "Rivals of Aether II",
    "Idol Showdown",
    "BlazBlue: Central Fiction",
    "Guilty Gear -Strive-",
    "GG Accent Core Plus R",
    "Nick All-Star Brawl",
    "Skullgirls",
    "Soulcalibur",
    "Street Fighter 6",
]

# Color palette mapped across wheel slices
COLORS = [
    "#FF5733",
    "#33FF57",
    "#3357FF",
    "#F39C12",
    "#9B59B6",
    "#1ABC9C",
    "#E74C3C",
    "#2ECC71",
    "#3498DB",
    "#E67E22",
    "#8E44AD",
    "#16A085",
    "#D35400",
    "#27AE60",
    "#2980B9",
    "#F1C40F",
    "#C0392B",
]


class VisualRoulette:

    def __init__(self, root):
        self.root = root
        self.root.title("Fighting Game Roulette")
        self.root.geometry("600x720")
        self.root.configure(bg="#1e1e2e")

        self.canvas_size = 500
        self.center = self.canvas_size / 2
        self.radius = 220

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#1e1e2e",
            highlightthickness=0,
        )
        self.canvas.pack(pady=20)

        self.result_label = tk.Label(
            root,
            text="Press SPIN to select a game!",
            font=("Helvetica", 16, "bold"),
            fg="#f5e0dc",
            bg="#1e1e2e",
        )
        self.result_label.pack(pady=10)

        # Fixed button configuration using valid Tkinter options (padx and pady)
        self.spin_button = tk.Button(
            root,
            text="SPIN!",
            font=("Helvetica", 14, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            padx=20,
            pady=10,
            command=self.start_spin,
        )
        self.spin_button.pack(pady=10)

        self.current_angle = 0.0
        self.speed = 0.0
        self.is_spinning = False

        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.delete("all")
        num_items = len(GAMES)
        slice_angle = 360.0 / num_items

        for i, game in enumerate(GAMES):
            start_deg = self.current_angle + (i * slice_angle)
            color = COLORS[i % len(COLORS)]

            # Sector slice definition
            self.canvas.create_arc(
                self.center - self.radius,
                self.center - self.radius,
                self.center + self.radius,
                self.center + self.radius,
                start=start_deg,
                extent=slice_angle,
                fill=color,
                outline="#181825",
                width=2,
            )

            # Center text positioning
            mid_angle_rad = math.radians(start_deg + (slice_angle / 2))
            text_x = self.center + (self.radius * 0.65) * math.cos(
                mid_angle_rad
            )
            text_y = self.center - (self.radius * 0.65) * math.sin(
                mid_angle_rad
            )

            display_text = (
                game[:14] + "..." if len(game) > 16 else game
            )

            self.canvas.create_text(
                text_x,
                text_y,
                text=display_text,
                fill="#ffffff",
                font=("Helvetica", 9, "bold"),
                angle=int(-start_deg - (slice_angle / 2)),
            )

        # Central hub element
        self.canvas.create_oval(
            self.center - 25,
            self.center - 25,
            self.center + 25,
            self.center + 25,
            fill="#11111b",
            outline="#cdd6f4",
            width=3,
        )

        # Indicator needle positioning at top center
        pointer_size = 15
        top_y = self.center - self.radius - 5
        self.canvas.create_polygon(
            self.center - pointer_size,
            top_y - pointer_size,
            self.center + pointer_size,
            top_y - pointer_size,
            self.center,
            top_y + 10,
            fill="#f38ba8",
            outline="#ffffff",
            width=2,
        )

    def start_spin(self):
        if not self.is_spinning:
            self.is_spinning = True
            self.spin_button.config(state=tk.DISABLED)
            self.result_label.config(
                text="Spinning...", fg="#f5e0dc"
            )
            self.speed = random.uniform(25.0, 40.0)
            self.animate_spin()

    def animate_spin(self):
        if self.speed > 0.1:
            self.current_angle = (self.current_angle + self.speed) % 360
            self.speed *= 0.975  # Friction coefficient applied per tick
            self.draw_wheel()
            self.root.after(16, self.animate_spin)
        else:
            self.is_spinning = False
            self.speed = 0
            self.draw_wheel()
            self.spin_button.config(state=tk.NORMAL)
            self.determine_winner()

    def determine_winner(self):
        num_items = len(GAMES)
        slice_angle = 360.0 / num_items

        # Top pointer constant angle reference
        pointer_angle = 90.0
        relative_angle = (pointer_angle - self.current_angle) % 360
        winning_index = int(relative_angle // slice_angle) % num_items

        winning_game = GAMES[winning_index]
        self.result_label.config(
            text=f"🔥 TONIGHT'S MATCH: {winning_game.upper()} 🔥",
            fg="#a6e3a1",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualRoulette(root)
    root.mainloop()