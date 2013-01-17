import QtQuick 1.0
import "widgets"

Item {
    id: window

    width: 640;
    height: 480;

    MouseArea {
        anchors.fill: parent
        onClicked: window.focus = false;
    }

    Rectangle {
        id: sim
        anchors {left: toolbox.right; top: parent.top; bottom: parent.bottom; right: parent.right}
        color: "#000000"
    }

    SystemPalette { id: activePalette }

    Rectangle {
        id: toolbox

        width: 120
        color: "#121212";
        anchors { left: parent.left; top: parent.top; bottom: parent.bottom }

        Column {
            anchors.centerIn: parent
            spacing: 8

            Text { color: "#cfcfcf"; text: "FireSim" }

            Button {
                text: "Add Fixture"
                onClicked: {
                    var fixCmp = Qt.createComponent("fixture_strand.qml");
                    if (fixCmp.status == Component.Ready) {
                        fixCmp.createObject(sim);
                    }
                }
            }
        }
    }
}