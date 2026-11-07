#pragma once

namespace Window {
class SessionController;
} // namespace Window

namespace Ovygram {

// Shows the content of a "section" surface in the main column of the
// window, in place of a chat. The section stays in the window history
// (Back returns to it) until the plugin closes it; when the history drops
// it, PluginUi::sectionGone() closes the surface.
void ShowPluginSection(
	not_null<Window::SessionController*> controller,
	const QString &objectId);

} // namespace Ovygram
