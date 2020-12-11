
import dbus

class BridgeManager:
    def __init__(self, dbusClient, UUID="fbc70397-2986-4ad7-b99c-64d2d00654b9", uid="bluetoothbridge", interfaceName="pan0", ip="111.111.111.1", ctrl=24):
        self.uuid = UUID
        self.uid = uid
        self.bus = dbusClient
        self.interfaceName = interfaceName
        self.ip = ip
        self.ctrl = ctrl

    def isBridgeExists(self):
        for conn in self.getConnections():
            if(conn["uuid"] == self.uuid):
                return True
        return False

    def getConnections(self):
        proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
        conns = []
        for conn in settings.ListConnections():
            con_proxy = self.bus.get_object("org.freedesktop.NetworkManager", conn)
            settings_connection = dbus.Interface(
                    con_proxy, "org.freedesktop.NetworkManager.Settings.Connection"
            )
            sett = settings_connection.GetSettings()
            uuid = sett["connection"]["uuid"]
            conns.append({"uuid": uuid, "path": conn, "settings": sett})
        return conns
    
    def addBridge(self):
        s_con = dbus.Dictionary({
            'type': 'bridge',
            'uuid': self.uuid,
            'id': self.uid,
            "interface-name": self.interfaceName
        })

        bridge = dbus.Dictionary({
            'stp': dbus.Boolean(False)
        })

        addr1 = dbus.Dictionary(
            {"address": self.ip, "prefix": dbus.UInt32(self.ctrl)})
        s_ip4 = dbus.Dictionary({
            'method': 'shared',
            "address-data": dbus.Array([addr1], signature=dbus.Signature("a{sv}")),
            "gateway": self.ip

        })

        s_ip6 = dbus.Dictionary({'method': 'ignore'})

        con = dbus.Dictionary({
            'connection': s_con,
            "bridge": bridge,
            'ipv4': s_ip4,
            'ipv6': s_ip6,
        })

        proxy = self.bus.get_object(
            "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
        settings = dbus.Interface(
            proxy, "org.freedesktop.NetworkManager.Settings")
        settings.AddConnection(con)




def main():
    dbusClient = dbus.SystemBus()
    manager = BridgeManager(dbusClient)
    if not manager.isBridgeExists():
        print("Adding bridge to NetworkManager")
        manager.addBridge()
    else:
        print("Bridge already exists")

if __name__ == "__main__":
    main()
