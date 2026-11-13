#pragma once

#include <QtCore/QString>
#include <functional>

// The application supplies these through its PCH. The standalone Qt harness
// compiles the production dialog without pulling in the whole Telegram UI.
template <typename Signature>
using Fn = std::function<Signature>;
inline QString operator""_q(const char16_t *text, size_t size) {
	return QString::fromUtf16(text, qsizetype(size));
}
