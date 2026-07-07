"""
theme.py

Central theme used by every UI component.
Never hardcode colors anywhere else.
"""

from dataclasses import dataclass


# ----------------------------------------------------------
# Theme Model
# ----------------------------------------------------------

@dataclass(frozen=True)
class ThemeData:

    # Colors

    background: str
    surface: str
    surface_alt: str
    card: str

    primary: str
    primary_hover: str
    primary_pressed: str

    success: str
    warning: str
    danger: str

    text: str
    text_secondary: str

    border: str
    divider: str

    # Radius

    radius_sm: int
    radius_md: int
    radius_lg: int

    # Spacing

    space_xs: int
    space_sm: int
    space_md: int
    space_lg: int
    space_xl: int

    # Font

    font_family: str

    title_size: int
    heading_size: int
    body_size: int
    small_size: int

    animation: int


# ----------------------------------------------------------
# Dark Theme
# ----------------------------------------------------------

DARK = ThemeData(

    background="#09090B",

    surface="#111827",

    surface_alt="#1F2937",

    card="#161B22",

    primary="#3B82F6",

    primary_hover="#2563EB",

    primary_pressed="#1D4ED8",

    success="#22C55E",

    warning="#F59E0B",

    danger="#EF4444",

    text="#F8FAFC",

    text_secondary="#94A3B8",

    border="#2E3440",

    divider="#374151",

    radius_sm=8,

    radius_md=12,

    radius_lg=18,

    space_xs=4,

    space_sm=8,

    space_md=12,

    space_lg=18,

    space_xl=26,

    font_family="Inter",

    title_size=26,

    heading_size=20,

    body_size=14,

    small_size=12,

    animation=180,
)


# ----------------------------------------------------------
# Light Theme
# ----------------------------------------------------------

LIGHT = ThemeData(

    background="#F8FAFC",

    surface="#FFFFFF",

    surface_alt="#F1F5F9",

    card="#FFFFFF",

    primary="#2563EB",

    primary_hover="#1D4ED8",

    primary_pressed="#1E40AF",

    success="#16A34A",

    warning="#D97706",

    danger="#DC2626",

    text="#111827",

    text_secondary="#64748B",

    border="#CBD5E1",

    divider="#E5E7EB",

    radius_sm=8,

    radius_md=12,

    radius_lg=18,

    space_xs=4,

    space_sm=8,

    space_md=12,

    space_lg=18,

    space_xl=26,

    font_family="Inter",

    title_size=26,

    heading_size=20,

    body_size=14,

    small_size=12,

    animation=180,
)


# ----------------------------------------------------------
# Active Theme
# ----------------------------------------------------------

Theme = DARK