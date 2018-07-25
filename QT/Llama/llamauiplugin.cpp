#include "llamaui.h"
#include "llamauiplugin.h"

#include <QtPlugin>

LlamaUIPlugin::LlamaUIPlugin(QObject *parent)
    : QObject(parent)
{
    m_initialized = false;
}

void LlamaUIPlugin::initialize(QDesignerFormEditorInterface * /* core */)
{
    if (m_initialized)
        return;

    // Add extension registrations, etc. here

    m_initialized = true;
}

bool LlamaUIPlugin::isInitialized() const
{
    return m_initialized;
}

QWidget *LlamaUIPlugin::createWidget(QWidget *parent)
{
    return new LlamaUI(parent);
}

QString LlamaUIPlugin::name() const
{
    return QLatin1String("LlamaUI");
}

QString LlamaUIPlugin::group() const
{
    return QLatin1String("");
}

QIcon LlamaUIPlugin::icon() const
{
    return QIcon();
}

QString LlamaUIPlugin::toolTip() const
{
    return QLatin1String("");
}

QString LlamaUIPlugin::whatsThis() const
{
    return QLatin1String("");
}

bool LlamaUIPlugin::isContainer() const
{
    return false;
}

QString LlamaUIPlugin::domXml() const
{
    return QLatin1String("<widget class=\"LlamaUI\" name=\"llamaUI\">\n</widget>\n");
}

QString LlamaUIPlugin::includeFile() const
{
    return QLatin1String("llamaui.h");
}
#if QT_VERSION < 0x050000
Q_EXPORT_PLUGIN2(llamauiplugin, LlamaUIPlugin)
#endif // QT_VERSION < 0x050000
