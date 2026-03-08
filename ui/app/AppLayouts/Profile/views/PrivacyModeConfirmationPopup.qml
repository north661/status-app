import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import StatusQ.Components
import StatusQ.Controls
import StatusQ.Core
import StatusQ.Core.Theme
import StatusQ.Popups

StatusModal {
    id: root

    required property bool currentlyEnabled

    signal confirmed(bool enable)
    signal cancelled()

    width: 480
    height: 320

    header.title: root.currentlyEnabled
        ? qsTr("Disable Privacy Mode")
        : qsTr("Enable Privacy Mode")

    contentItem: ColumnLayout {
        spacing: 16

        StatusBaseText {
            Layout.fillWidth: true
            Layout.leftMargin: 16
            Layout.rightMargin: 16
            wrapMode: Text.WordWrap
            text: root.currentlyEnabled
                ? qsTr("Re-enabling third-party services will restore access to features like token prices, swap, and WalletConnect. Your wallet addresses may be shared with external providers.")
                : qsTr("Enabling Privacy Mode will disable all third-party integrations including token prices, swap providers, WalletConnect, and GIF search. No data will be sent to external services.")
        }

        StatusBaseText {
            Layout.fillWidth: true
            Layout.leftMargin: 16
            Layout.rightMargin: 16
            font.pixelSize: Theme.additionalTextSize
            color: Theme.palette.baseColor1
            wrapMode: Text.WordWrap
            text: qsTr("You can change this at any time in Settings → Privacy & Security.")
        }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            Layout.rightMargin: 16
            Layout.bottomMargin: 16
            spacing: 12

            StatusFlatButton {
                text: qsTr("Cancel")
                onClicked: root.cancelled()
            }

            StatusButton {
                text: root.currentlyEnabled
                    ? qsTr("Disable Privacy Mode")
                    : qsTr("Enable Privacy Mode")
                type: root.currentlyEnabled ? StatusButton.Type.Warning : StatusButton.Type.Primary
                onClicked: root.confirmed(!root.currentlyEnabled)
            }
        }
    }
}
