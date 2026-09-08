import copy

from manimlib import *
from manimlib.mobject.svg.old_tex_mobject import *

from custom.backdrops import *
from custom.banner import *
from custom.characters.pi_creature import *
from custom.characters.pi_creature_animations import *
from custom.characters.pi_creature_scene import *
from custom.deprecated import *
from custom.drawings import *
from custom.end_screen import *
from custom.filler import *
from custom.logo import *
from custom.opening_quote import *
from once_useful_constructs.vector_space_scene import *
from once_useful_constructs.matrix_multiplication import *

# Legacy compatibility shims for older 3b1b scene files.
OldTex = Tex
OldTexText = TexText


def _legacy_merge_config(base, update):
	for key, value in update.items():
		if isinstance(value, dict) and isinstance(base.get(key), dict):
			_legacy_merge_config(base[key], value)
		else:
			base[key] = copy.deepcopy(value)
	return base


def _legacy_config_for_class(cls):
	config = {}
	for base in reversed(cls.mro()):
		if hasattr(base, "CONFIG"):
			_legacy_merge_config(config, base.CONFIG)
	return config


def _apply_legacy_config(obj, kwargs=None):
	config = _legacy_config_for_class(obj.__class__)
	if kwargs:
		_legacy_merge_config(config, kwargs)
	for key, value in config.items():
		setattr(obj, key, value)
	return config


_MOBJECT_INIT_KWARGS = {
	"color", "opacity", "shading", "texture_paths", "is_fixed_in_frame",
	"depth_test", "z_index",
}

_VMOBJECT_INIT_KWARGS = _MOBJECT_INIT_KWARGS | {
	"fill_color", "fill_opacity", "stroke_color", "stroke_opacity",
	"stroke_width", "stroke_behind", "background_image_file", "long_lines",
	"joint_type", "flat_stroke", "scale_stroke_with_zoom",
	"use_simple_quadratic_approx", "anti_alias_width", "fill_border_width",
}

_SCENE_INIT_KWARGS = {
	"window", "camera_config", "file_writer_config", "skip_animations",
	"always_update_mobjects", "start_at_animation_number",
	"end_at_animation_number", "show_animation_progress",
	"leave_progress_bars", "preview_while_skipping", "presenter_mode",
	"default_wait_time",
}

_ANIMATION_INIT_KWARGS = {
	"run_time", "time_span", "lag_ratio", "rate_func", "name", "remover",
	"final_alpha_value", "suspend_mobject_updating",
}


_mobject_init = Mobject.__init__


def _legacy_mobject_init(self, *submobjects, **kwargs):
	config = _apply_legacy_config(self, kwargs)
	call_kwargs = {
		key: config[key]
		for key in _MOBJECT_INIT_KWARGS
		if key in config
	}
	if submobjects and all(isinstance(mob, Mobject) for mob in submobjects):
		_mobject_init(self, **call_kwargs)
		self.add(*submobjects)
	else:
		_mobject_init(self, *submobjects, **call_kwargs)


Mobject.__init__ = _legacy_mobject_init

if not hasattr(Mobject, "ingest_submobjects"):
	def _legacy_ingest_submobjects(self):
		return self

	Mobject.ingest_submobjects = _legacy_ingest_submobjects

_vmobject_init = VMobject.__init__


def _legacy_vmobject_init(self, *submobjects, **kwargs):
	config = _apply_legacy_config(self, kwargs)
	call_kwargs = {
		key: config[key]
		for key in _VMOBJECT_INIT_KWARGS
		if key in config
	}
	if submobjects and all(isinstance(mob, Mobject) for mob in submobjects):
		_vmobject_init(self, **call_kwargs)
		self.add(*submobjects)
	else:
		_vmobject_init(self, *submobjects, **call_kwargs)


VMobject.__init__ = _legacy_vmobject_init

_arrow_init = Arrow.__init__


def _legacy_arrow_init(self, *args, **kwargs):
	# Newer manimlib draws arrows as filled shapes, and Arrow's own default for
	# fill_color wins over the generic `color` kwarg. Legacy scenes assume
	# `color` tints the whole arrow, so mirror it onto the fill.
	if "color" in kwargs and "fill_color" not in kwargs:
		kwargs["fill_color"] = kwargs["color"]
	_arrow_init(self, *args, **kwargs)


Arrow.__init__ = _legacy_arrow_init

_tex_init = Tex.__init__


def _legacy_tex_init(self, *args, **kwargs):
	# Legacy scenes pass a list of strings, e.g. OldTexText(["Matrices as", "..."]),
	# where current manimlib expects them as separate positional arguments.
	if len(args) == 1 and isinstance(args[0], (list, tuple)):
		args = tuple(args[0])
	_tex_init(self, *args, **kwargs)


Tex.__init__ = _legacy_tex_init

# Old NumberPlane/Axes took their extent as x_min/x_max/x_radius and their color
# as a single `color` kwarg; current manimlib takes x_range/y_range and styles
# the grid through axis_config / background_line_style.
_LEGACY_AXES_KEYS = {
	"x_min", "x_max", "y_min", "y_max", "x_radius", "y_radius",
	"x_line_frequency", "y_line_frequency", "tick_frequency",
	"secondary_line_ratio", "secondary_color", "secondary_stroke_width",
	"written_coordinate_height", "number_scale_val", "num_pair_at_center",
	"propagate_style_to_family", "space_unit_to_x_unit", "space_unit_to_y_unit",
}


def _legacy_axis_range(kwargs, prefix, default_radius):
	radius = kwargs.get(f"{prefix}_radius")
	low = kwargs.get(f"{prefix}_min")
	high = kwargs.get(f"{prefix}_max")
	if radius is not None:
		low = -radius if low is None else low
		high = radius if high is None else high
	if low is None and high is None:
		return None
	low = -default_radius if low is None else low
	high = default_radius if high is None else high
	step = kwargs.get(f"{prefix}_line_frequency") or kwargs.get("tick_frequency") or 1.0
	return (low, high, step)


def _normalize_legacy_axes_kwargs(args, kwargs):
	"""Translate legacy kwargs in place, returning the `color` to apply afterwards."""
	if "secondary_line_ratio" in kwargs:
		kwargs.setdefault("faded_line_ratio", kwargs["secondary_line_ratio"])
	for index, (prefix, default_radius) in enumerate([
		("x", FRAME_X_RADIUS), ("y", FRAME_Y_RADIUS)
	]):
		key = f"{prefix}_range"
		rng = _legacy_axis_range(kwargs, prefix, default_radius)
		if rng is not None and len(args) <= index and key not in kwargs:
			kwargs[key] = rng
	for key in _LEGACY_AXES_KEYS:
		kwargs.pop(key, None)
	return kwargs.pop("color", None)


def _make_legacy_axes_init(original_init):
	def legacy_init(self, *args, **kwargs):
		color = _normalize_legacy_axes_kwargs(args, kwargs)
		original_init(self, *args, **kwargs)
		if color is not None:
			self.set_color(color)
	return legacy_init


Axes.__init__ = _make_legacy_axes_init(Axes.__init__)
NumberPlane.__init__ = _make_legacy_axes_init(NumberPlane.__init__)

_matrix_init = Matrix.__init__


def _legacy_matrix_init(self, matrix, *args, **kwargs):
	# Legacy scenes hand a flat vector to Matrix and expect a column.
	if isinstance(matrix, (list, tuple, np.ndarray)) and len(matrix) > 0:
		if not isinstance(matrix[0], (list, tuple, np.ndarray)):
			matrix = [[entry] for entry in matrix]
	_matrix_init(self, matrix, *args, **kwargs)


Matrix.__init__ = _legacy_matrix_init


def _legacy_get_mob_matrix(self):
	# Legacy scenes treat this as a numpy array (.flatten(), .shape, np.transpose).
	# Building it element by element avoids numpy recursing into the mobjects.
	rows = self.mob_matrix
	array = np.empty((len(rows), len(rows[0]) if rows else 0), dtype=object)
	for i, row in enumerate(rows):
		for j, mob in enumerate(row):
			array[i, j] = mob
	return array


Matrix.get_mob_matrix = _legacy_get_mob_matrix

_scene_init = Scene.__init__


def _legacy_scene_init(self, *args, **kwargs):
	config_kwargs = {
		key: value
		for key, value in kwargs.items()
		if key not in _SCENE_INIT_KWARGS
	}
	config = _apply_legacy_config(self, config_kwargs)
	call_kwargs = {
		key: kwargs[key] if key in kwargs else config[key]
		for key in _SCENE_INIT_KWARGS
		if key in kwargs or key in config
	}
	_scene_init(self, *args, **call_kwargs)


Scene.__init__ = _legacy_scene_init

_animation_init = Animation.__init__


def _legacy_animation_init(self, mobject, *args, **kwargs):
	config = _apply_legacy_config(self, kwargs)
	call_kwargs = {
		key: kwargs[key] if key in kwargs else config[key]
		for key in _ANIMATION_INIT_KWARGS
		if key in kwargs or key in config
	}
	_animation_init(self, mobject, *args, **call_kwargs)


Animation.__init__ = _legacy_animation_init

_pi_get_bubble = PiCreature.get_bubble


def _legacy_get_bubble(self, content="", bubble_type=ThoughtBubble, **bubble_config):
	return _pi_get_bubble(self, content, bubble_type=bubble_type, **bubble_config)


PiCreature.get_bubble = _legacy_get_bubble

if "DoubleArrow" not in globals():
	def DoubleArrow(start, end, **kwargs):
		arrow = Arrow(start, end, **kwargs)
		arrow.add_tip(at_start=True)
		return arrow


if "matrix_to_mobject" not in globals():
	def matrix_to_mobject(matrix):
		return Matrix(matrix)


if "Point" not in globals():
	def Point(location=ORIGIN):
		return VectorizedPoint(location)


class RandolphScene(PiCreatureScene):
	def create_pi_creature(self):
		return Randolph(**self.default_pi_creature_kwargs)

	def setup(self):
		super().setup()
		self.randy = self.pi_creature
