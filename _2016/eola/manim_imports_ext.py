import copy
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

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

# -----------------------------------------------------------------------------
# Legacy EOLA compatibility layer (2016 scenes -> current manimlib)
# -----------------------------------------------------------------------------

# OldTex* can fail on newer manimlib's legacy SVG path; modern Tex classes are
# much more stable for these scenes.
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


# Older videos frequently do Mobject(*mobjects) and VMobject(*mobjects).
# Restore that constructor behavior while preserving modern defaults.
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


# Newer PiCreature.get_bubble requires explicit content. Legacy scenes often
# call get_bubble() with no args.
_pi_get_bubble = PiCreature.get_bubble


def _legacy_get_bubble(self, content="", bubble_type=ThoughtBubble, **bubble_config):
	return _pi_get_bubble(self, content, bubble_type=bubble_type, **bubble_config)


PiCreature.get_bubble = _legacy_get_bubble


# Small geometry helpers expected by older code.
if "DoubleArrow" not in globals():
	def DoubleArrow(start, end, **kwargs):
		arrow = Arrow(start, end, **kwargs)
		arrow.add_tip(at_start=True)
		return arrow


if "Point" not in globals():
	def Point(location=ORIGIN):
		return VectorizedPoint(location)


class RandolphScene(PiCreatureScene):
	def create_pi_creature(self):
		return Randolph(**self.default_pi_creature_kwargs)

	def setup(self):
		super().setup()
		self.randy = self.pi_creature
