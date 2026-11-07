#pragma once

class PeerData;
class QWidget;

namespace Ovygram {

// Called from HistoryView::ChatWidget::updateControlsGeometry(), the widget
// that shows chats. Places the plugin bars of `peer` into the chat widget at
// (left, top) and returns their total height, so the chat moves the messages
// below them. Returns 0 when no plugin shows a bar in this chat.
[[nodiscard]] int LayoutChatBars(
	QWidget *chat,
	PeerData *peer,
	int left,
	int top,
	int width);

} // namespace Ovygram
