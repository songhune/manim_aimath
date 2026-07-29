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


# Older videos frequently do VMobject(*mobjects). Restore that constructor
# behavior while preserving modern VMobject defaults.
_vmobject_init = VMobject.__init__


def _legacy_vmobject_init(self, *submobjects, **kwargs):
	_vmobject_init(self, **kwargs)
	if submobjects:
		self.add(*submobjects)


VMobject.__init__ = _legacy_vmobject_init


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
