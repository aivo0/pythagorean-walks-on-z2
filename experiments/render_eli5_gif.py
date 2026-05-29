"""Render an ELI5 animated GIF for the Pythagorean-walk problem."""

from __future__ import annotations

from math import atan2, cos, sin
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "pythagorean-walks-eli5.gif"

WIDTH = 960
HEIGHT = 560
FRAME_DURATION_MS = 280
BG = (255, 249, 238)
GRID = (224, 211, 188)
AXIS = (166, 148, 119)
TEXT = (47, 48, 51)
MUTED = (94, 95, 96)
GREEN = (27, 128, 91)
BLUE = (42, 111, 176)
RED = (204, 75, 58)
ORANGE = (224, 137, 50)
PAPER = (255, 252, 245)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE = load_font(34, bold=True)
HEADING = load_font(24, bold=True)
BODY = load_font(19)
SMALL = load_font(15)
LABEL = load_font(16, bold=True)


def text_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    lines: list[str],
    *,
    width: int = 430,
    fill: tuple[int, int, int] = PAPER,
) -> None:
    x, y = xy
    line_height = 26
    padding = 16
    height = padding * 2 + line_height * len(lines)
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=18,
        fill=fill,
        outline=(226, 209, 176),
        width=2,
    )
    for index, line in enumerate(lines):
        font = HEADING if index == 0 else BODY
        color = TEXT if index == 0 else MUTED
        draw.text((x + padding, y + padding + index * line_height), line, font=font, fill=color)


def bounds_transform(bounds: tuple[int, int, int, int]):
    xmin, xmax, ymin, ymax = bounds
    left, top, right, bottom = 70, 92, WIDTH - 55, HEIGHT - 50
    sx = (right - left) / (xmax - xmin)
    sy = (bottom - top) / (ymax - ymin)
    scale = min(sx, sy)
    xmid = (xmin + xmax) / 2
    ymid = (ymin + ymax) / 2
    cx = (left + right) / 2
    cy = (top + bottom) / 2

    def point(p: tuple[float, float]) -> tuple[int, int]:
        x, y = p
        return (round(cx + (x - xmid) * scale), round(cy - (y - ymid) * scale))

    return point


def make_canvas(
    title: str,
    subtitle: str,
    bounds: tuple[int, int, int, int] = (-5, 10, -5, 12),
) -> tuple[Image.Image, ImageDraw.ImageDraw, Callable[[tuple[float, float]], tuple[int, int]]]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.text((34, 24), title, font=TITLE, fill=TEXT)
    draw.text((36, 64), subtitle, font=BODY, fill=MUTED)

    to_px = bounds_transform(bounds)
    xmin, xmax, ymin, ymax = bounds
    for x in range(xmin, xmax + 1):
        p1 = to_px((x, ymin))
        p2 = to_px((x, ymax))
        draw.line((p1, p2), fill=GRID, width=1)
    for y in range(ymin, ymax + 1):
        p1 = to_px((xmin, y))
        p2 = to_px((xmax, y))
        draw.line((p1, p2), fill=GRID, width=1)

    if xmin <= 0 <= xmax:
        draw.line((to_px((0, ymin)), to_px((0, ymax))), fill=AXIS, width=2)
    if ymin <= 0 <= ymax:
        draw.line((to_px((xmin, 0)), to_px((xmax, 0))), fill=AXIS, width=2)

    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            px, py = to_px((x, y))
            draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill=(127, 120, 108))

    return image, draw, to_px


def line_with_arrow(
    draw: ImageDraw.ImageDraw,
    to_px,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    *,
    width: int = 6,
    progress: float = 1.0,
) -> None:
    sx, sy = start
    ex, ey = end
    current = (sx + (ex - sx) * progress, sy + (ey - sy) * progress)
    p1 = to_px(start)
    p2 = to_px(current)
    draw.line((p1, p2), fill=color, width=width)
    if progress < 0.2:
        return
    angle = atan2(p2[1] - p1[1], p2[0] - p1[0])
    size = 14
    left = (
        p2[0] - size * cos(angle - 0.55),
        p2[1] - size * sin(angle - 0.55),
    )
    right = (
        p2[0] - size * cos(angle + 0.55),
        p2[1] - size * sin(angle + 0.55),
    )
    draw.polygon((p2, left, right), fill=color)


def node(
    draw: ImageDraw.ImageDraw,
    to_px,
    point: tuple[int, int],
    label: str,
    color: tuple[int, int, int],
) -> None:
    x, y = to_px(point)
    draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=color, outline=(255, 255, 255), width=3)
    draw.text((x + 12, y - 18), label, font=LABEL, fill=color)


def badge(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color) -> None:
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=LABEL)
    w = bbox[2] - bbox[0] + 22
    h = bbox[3] - bbox[1] + 14
    draw.rounded_rectangle((x, y, x + w, y + h), radius=14, fill=color)
    draw.text((x + 11, y + 7), text, font=LABEL, fill=(255, 255, 255))


def frame_lattice() -> Image.Image:
    image, draw, to_px = make_canvas(
        "Pythagorean walks, ELI5",
        "Dots are integer lattice points.",
        bounds=(-5, 8, -5, 6),
    )
    node(draw, to_px, (0, 0), "Start", BLUE)
    text_box(
        draw,
        (510, 112),
        [
            "The board",
            "Every dot is a point (x,y).",
            "A walk is a chain of jumps",
            "from one dot to another.",
        ],
        width=390,
    )
    return image


def frame_rule(progress: float) -> Image.Image:
    image, draw, to_px = make_canvas(
        "The jump rule",
        "You may jump only by a Pythagorean triangle.",
        bounds=(-2, 6, -2, 6),
    )
    node(draw, to_px, (0, 0), "O", BLUE)
    node(draw, to_px, (3, 4), "(3,4)", GREEN)
    line_with_arrow(draw, to_px, (0, 0), (3, 4), GREEN, progress=progress)
    line_with_arrow(draw, to_px, (0, 0), (5, 0), RED, progress=1.0, width=4)
    line_with_arrow(draw, to_px, (0, 0), (0, 5), RED, progress=1.0, width=4)
    badge(draw, (624, 125), "allowed: 3-4-5", GREEN)
    badge(draw, (624, 174), "forbidden: flat", RED)
    text_box(
        draw,
        (560, 235),
        [
            "Rule",
            "Integer distance is not enough.",
            "The jump cannot be horizontal",
            "or vertical.",
        ],
        width=350,
    )
    return image


def frame_two_hops(progress: float) -> Image.Image:
    image, draw, to_px = make_canvas(
        "Some close dots need two hops",
        "Example: (1,1) is not one jump, but two 5-long jumps work.",
        bounds=(-1, 5, -4, 3),
    )
    path = [(0, 0), (4, -3), (1, 1)]
    node(draw, to_px, path[0], "O", BLUE)
    node(draw, to_px, path[1], "P", ORANGE)
    node(draw, to_px, path[2], "(1,1)", GREEN)
    if progress <= 0.5:
        line_with_arrow(draw, to_px, path[0], path[1], ORANGE, progress=progress * 2)
    else:
        line_with_arrow(draw, to_px, path[0], path[1], ORANGE)
        line_with_arrow(draw, to_px, path[1], path[2], GREEN, progress=(progress - 0.5) * 2)
    text_box(
        draw,
        (530, 115),
        [
            "Two hops",
            "O -> (4,-3) is length 5.",
            "(4,-3) -> (1,1) is length 5.",
            "So (1,1) is distance 2.",
        ],
        width=380,
    )
    return image


def frame_three_hops(progress: float) -> Image.Image:
    image, draw, to_px = make_canvas(
        "A tiny exception needs three hops",
        "The paper proves (1,0) has no two-hop route.",
        bounds=(-4, 10, -3, 13),
    )
    path = [(0, 0), (9, 12), (-3, 3), (1, 0)]
    colors = [ORANGE, ORANGE, GREEN]
    labels = ["O", "A", "B", "(1,0)"]
    node(draw, to_px, path[0], labels[0], BLUE)
    node(draw, to_px, path[1], labels[1], ORANGE)
    node(draw, to_px, path[2], labels[2], ORANGE)
    node(draw, to_px, path[3], labels[3], RED)
    stage = min(2, int(progress * 3))
    local = progress * 3 - stage
    for index in range(stage):
        line_with_arrow(draw, to_px, path[index], path[index + 1], colors[index])
    line_with_arrow(draw, to_px, path[stage], path[stage + 1], colors[stage], progress=local)
    text_box(
        draw,
        (522, 110),
        [
            "Three hops",
            "(1,0) is next door...",
            "but flat jumps are banned.",
            "It needs a detour.",
        ],
        width=380,
    )
    return image


def frame_big_picture() -> Image.Image:
    image, draw, to_px = make_canvas(
        "Big picture",
        "The conjecture: only a few tiny targets need three hops.",
        bounds=(-4, 4, -4, 4),
    )
    exceptions = {
        (-1, 0),
        (1, 0),
        (-2, 0),
        (2, 0),
        (0, -1),
        (0, 1),
        (0, -2),
        (0, 2),
        (-2, -1),
        (-2, 1),
        (2, -1),
        (2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
    }
    for x in range(-4, 5):
        for y in range(-4, 5):
            if (x, y) == (0, 0):
                continue
            px, py = to_px((x, y))
            if (x, y) in exceptions:
                draw.ellipse((px - 9, py - 9, px + 9, py + 9), fill=RED)
            else:
                draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=GREEN)
    node(draw, to_px, (0, 0), "O", BLUE)
    text_box(
        draw,
        (548, 110),
        [
            "What we proved here",
            "All axis dots after 2",
            "are at most two hops away.",
            "So are later (2,1) multiples.",
            "The full non-axis claim",
            "is still open.",
        ],
        width=370,
    )
    badge(draw, (570, 300), "green: <= 2 hops", GREEN)
    badge(draw, (570, 348), "red: known 3-hop orbit", RED)
    return image


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    frames: list[Image.Image] = []
    frames.extend([frame_lattice()] * 8)
    for i in range(8):
        frames.append(frame_rule((i + 1) / 8))
    frames.extend([frame_rule(1.0)] * 5)
    for i in range(12):
        frames.append(frame_two_hops((i + 1) / 12))
    frames.extend([frame_two_hops(1.0)] * 5)
    for i in range(15):
        frames.append(frame_three_hops((i + 1) / 15))
    frames.extend([frame_three_hops(1.0)] * 6)
    frames.extend([frame_big_picture()] * 10)

    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
