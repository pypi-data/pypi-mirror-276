from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from aiofiles import open as async_open
else:
	def _throw_plug(p, m, **kw):
		raise ModuleNotFoundError

try:
	from aiofiles import open as async_open
	from aiofiles.ospath import wrap as wrap2async
except ImportError:
	async_open = _throw_plug
	wrap2async = _throw_plug
