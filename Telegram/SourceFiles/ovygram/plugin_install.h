#pragma once

#include <QtCore/QString>

namespace Ovygram {

// A native application-modal confirmation outside the Plugin API surface tree.
// While it exists, supported plugin UI/native/key APIs cannot inspect or act.
[[nodiscard]] bool InstallationUiActive();
void ShowPluginInstall(
	const QString &path,
	const QString &installationId = QString(),
	Fn<void()> done = nullptr);

} // namespace Ovygram
