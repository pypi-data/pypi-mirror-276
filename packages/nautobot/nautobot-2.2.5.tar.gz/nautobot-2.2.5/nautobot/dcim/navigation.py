from nautobot.core.apps import (
    NavContext,
    NavGrouping,
    NavItem,
    NavMenuAddButton,
    NavMenuGroup,
    NavMenuItem,
    NavMenuTab,
)

menu_items = (
    NavMenuTab(
        name="Organization",
        weight=100,
        groups=(
            NavMenuGroup(
                name="Locations",
                weight=150,
                items=(
                    NavMenuItem(
                        link="dcim:location_list",
                        name="Locations",
                        weight=100,
                        permissions=[
                            "dcim.view_location",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:location_add",
                                permissions=[
                                    "dcim.add_location",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:locationtype_list",
                        name="Location Types",
                        weight=200,
                        permissions=[
                            "dcim.view_locationtype",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:locationtype_add",
                                permissions=[
                                    "dcim.add_locationtype",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Racks",
                weight=200,
                items=(
                    NavMenuItem(
                        link="dcim:rack_list",
                        name="Racks",
                        weight=100,
                        permissions=[
                            "dcim.view_rack",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:rack_add",
                                permissions=[
                                    "dcim.add_rack",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:rackgroup_list",
                        name="Rack Groups",
                        weight=200,
                        permissions=[
                            "dcim.view_rackgroup",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:rackgroup_add",
                                permissions=[
                                    "dcim.add_rackgroup",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:rackreservation_list",
                        name="Rack Reservations",
                        weight=400,
                        permissions=[
                            "dcim.view_rackreservation",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:rackreservation_add",
                                permissions=[
                                    "dcim.add_rackreservation",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:rack_elevation_list",
                        name="Elevations",
                        weight=500,
                        permissions=[
                            "dcim.view_rack",
                        ],
                        buttons=(),
                    ),
                ),
            ),
        ),
    ),
    NavMenuTab(
        name="Devices",
        weight=200,
        groups=(
            NavMenuGroup(
                name="Devices",
                weight=100,
                items=(
                    NavMenuItem(
                        link="dcim:device_list",
                        name="Devices",
                        weight=100,
                        permissions=[
                            "dcim.view_device",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:device_add",
                                permissions=[
                                    "dcim.add_device",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:virtualchassis_list",
                        name="Virtual Chassis",
                        weight=400,
                        permissions=[
                            "dcim.view_virtualchassis",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:virtualchassis_add",
                                permissions=[
                                    "dcim.add_virtualchassis",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:deviceredundancygroup_list",
                        name="Device Redundancy Groups",
                        weight=500,
                        permissions=[
                            "dcim.view_deviceredundancygroup",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:deviceredundancygroup_add",
                                permissions=[
                                    "dcim.add_deviceredundancygroup",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:interfaceredundancygroup_list",
                        name="Interface Redundancy Groups",
                        weight=600,
                        permissions=[
                            "dcim.view_interfaceredundancygroup",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:interfaceredundancygroup_add",
                                permissions=[
                                    "dcim.add_interfaceredundancygroup",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Device Types",
                weight=200,
                items=(
                    NavMenuItem(
                        link="dcim:devicetype_list",
                        name="Device Types",
                        weight=100,
                        permissions=[
                            "dcim.view_devicetype",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:devicetype_add",
                                permissions=[
                                    "dcim.add_devicetype",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:devicefamily_list",
                        name="Device Families",
                        weight=200,
                        permissions=[
                            "dcim.view_devicefamily",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:devicefamily_add",
                                permissions=[
                                    "dcim.add_devicefamily",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:manufacturer_list",
                        name="Manufacturers",
                        weight=300,
                        permissions=[
                            "dcim.view_manufacturer",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:manufacturer_add",
                                permissions=[
                                    "dcim.add_manufacturer",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Software",
                weight=300,
                items=(
                    NavMenuItem(
                        link="dcim:platform_list",
                        name="Platforms",
                        weight=100,
                        permissions=[
                            "dcim.view_platform",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:platform_add",
                                permissions=[
                                    "dcim.add_platform",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:softwareversion_list",
                        name="Software Versions",
                        weight=200,
                        permissions=[
                            "dcim.view_softwareversion",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:softwareversion_add",
                                permissions=[
                                    "dcim.add_softwareversion",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:softwareimagefile_list",
                        name="Software Image Files",
                        weight=300,
                        permissions=[
                            "dcim.view_softwareimagefile",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:softwareimagefile_add",
                                permissions=[
                                    "dcim.add_softwareimagefile",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Controllers",
                weight=400,
                items=(
                    NavMenuItem(
                        link="dcim:controller_list",
                        name="Controllers",
                        weight=100,
                        permissions=[
                            "dcim.view_controller",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:controller_add",
                                permissions=[
                                    "dcim.add_controller",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:controllermanageddevicegroup_list",
                        name="Managed Device Groups",
                        weight=200,
                        permissions=[
                            "dcim.view_controllermanageddevicegroup",
                        ],
                    ),
                ),
            ),
            NavMenuGroup(
                name="Connections",
                weight=500,
                items=(
                    NavMenuItem(
                        link="dcim:cable_list",
                        name="Cables",
                        weight=100,
                        permissions=[
                            "dcim.view_cable",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:console_connections_list",
                        name="Console Connections",
                        weight=200,
                        permissions=[
                            "dcim.view_consoleport",
                            "dcim.view_consoleserverport",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:power_connections_list",
                        name="Power Connections",
                        weight=300,
                        permissions=[
                            "dcim.view_powerport",
                            "dcim.view_poweroutlet",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:interface_connections_list",
                        name="Interface Connections",
                        weight=400,
                        permissions=[
                            "dcim.view_interface",
                        ],
                        buttons=(),
                    ),
                ),
            ),
            NavMenuGroup(
                name="Device Components",
                weight=600,
                items=(
                    NavMenuItem(
                        link="dcim:interface_list",
                        name="Interfaces",
                        weight=100,
                        permissions=[
                            "dcim.view_interface",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:frontport_list",
                        name="Front Ports",
                        weight=200,
                        permissions=[
                            "dcim.view_frontport",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:rearport_list",
                        name="Rear Ports",
                        weight=300,
                        permissions=[
                            "dcim.view_rearport",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:consoleport_list",
                        name="Console Ports",
                        weight=400,
                        permissions=[
                            "dcim.view_consoleport",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:consoleserverport_list",
                        name="Console Server Ports",
                        weight=500,
                        permissions=[
                            "dcim.view_consoleserverport",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:powerport_list",
                        name="Power Ports",
                        weight=600,
                        permissions=[
                            "dcim.view_powerport",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:poweroutlet_list",
                        name="Power Outlets",
                        weight=700,
                        permissions=[
                            "dcim.view_poweroutlet",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:devicebay_list",
                        name="Device Bays",
                        weight=800,
                        permissions=[
                            "dcim.view_devicebay",
                        ],
                        buttons=(),
                    ),
                    NavMenuItem(
                        link="dcim:inventoryitem_list",
                        name="Inventory Items",
                        weight=900,
                        permissions=[
                            "dcim.view_inventoryitem",
                        ],
                        buttons=(),
                    ),
                ),
            ),
        ),
    ),
    NavMenuTab(
        name="Power",
        weight=600,
        groups=(
            NavMenuGroup(
                name="Power",
                weight=100,
                items=(
                    NavMenuItem(
                        link="dcim:powerfeed_list",
                        name="Power Feeds",
                        permissions=[
                            "dcim.view_powerfeed",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:powerfeed_add",
                                permissions=[
                                    "dcim.add_powerfeed",
                                ],
                            ),
                        ),
                    ),
                    NavMenuItem(
                        link="dcim:powerpanel_list",
                        name="Power Panels",
                        permissions=[
                            "dcim.view_powerpanel",
                        ],
                        buttons=(
                            NavMenuAddButton(
                                link="dcim:powerpanel_add",
                                permissions=[
                                    "dcim.add_powerpanel",
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)


navigation = (
    NavContext(
        name="Inventory",
        groups=(
            NavGrouping(
                name="Devices",
                weight=100,
                items=(
                    NavItem(
                        name="Devices",
                        link="dcim:device_list",
                        weight=100,
                        permissions=["dcim.view_device"],
                    ),
                    NavItem(
                        name="Device Types",
                        weight=200,
                        link="dcim:devicetype_list",
                        permissions=["dcim.view_devicetype"],
                    ),
                    NavItem(
                        link="dcim:platform_list",
                        name="Platforms",
                        weight=300,
                        permissions=[
                            "dcim.view_platform",
                        ],
                    ),
                    NavItem(
                        link="dcim:manufacturer_list",
                        name="Manufacturers",
                        weight=400,
                        permissions=[
                            "dcim.view_manufacturer",
                        ],
                    ),
                    NavItem(
                        link="dcim:virtualchassis_list",
                        name="Virtual Chassis",
                        weight=500,
                        permissions=[
                            "dcim.view_virtualchassis",
                        ],
                    ),
                    NavItem(
                        name="Device Redundancy Groups",
                        weight=600,
                        link="dcim:deviceredundancygroup_list",
                        permissions=["dcim.view_deviceredundancygroup"],
                    ),
                    NavGrouping(
                        name="Connections",
                        weight=700,
                        items=(
                            NavItem(
                                name="Cables",
                                weight=100,
                                link="dcim:cable_list",
                                permissions=["dcim.view_cable"],
                            ),
                            NavItem(
                                name="Console Connections",
                                weight=200,
                                link="dcim:console_connections_list",
                                permissions=[
                                    "dcim.view_consoleport",
                                    "dcim.view_consoleserverport",
                                ],
                            ),
                            NavItem(
                                name="Power Connections",
                                weight=300,
                                link="dcim:power_connections_list",
                                permissions=[
                                    "dcim.view_powerport",
                                    "dcim.view_poweroutlet",
                                ],
                            ),
                            NavItem(
                                name="Interface Connections",
                                weight=400,
                                link="dcim:interface_connections_list",
                                permissions=["dcim.view_interface"],
                            ),
                        ),
                    ),
                    NavGrouping(
                        name="Components",
                        weight=800,
                        items=(
                            NavItem(
                                name="Interfaces",
                                weight=100,
                                link="dcim:interface_list",
                                permissions=["dcim.view_interface"],
                            ),
                            NavItem(
                                name="Front Ports",
                                weight=200,
                                link="dcim:frontport_list",
                                permissions=["dcim.view_frontport"],
                            ),
                            NavItem(
                                name="Rear Ports",
                                weight=300,
                                link="dcim:rearport_list",
                                permissions=["dcim.view_rearport"],
                            ),
                            NavItem(
                                name="Console Ports",
                                weight=400,
                                link="dcim:consoleport_list",
                                permissions=["dcim.view_consoleport"],
                            ),
                            NavItem(
                                name="Console Server Ports",
                                weight=500,
                                link="dcim:consoleserverport_list",
                                permissions=["dcim.view_consoleserverport"],
                            ),
                            NavItem(
                                name="Power Ports",
                                weight=600,
                                link="dcim:powerport_list",
                                permissions=["dcim.view_powerport"],
                            ),
                            NavItem(
                                name="Power Outlets",
                                weight=700,
                                link="dcim:poweroutlet_list",
                                permissions=["dcim.view_poweroutlet"],
                            ),
                            NavItem(
                                name="Device Bays",
                                weight=800,
                                link="dcim:devicebay_list",
                                permissions=["dcim.view_devicebay"],
                            ),
                            NavItem(
                                name="Inventory Items",
                                weight=900,
                                link="dcim:inventoryitem_list",
                                permissions=["dcim.view_inventoryitem"],
                            ),
                        ),
                    ),
                    # space reserved for Dynamic Groups item with weight 900
                    NavItem(
                        name="Racks",
                        weight=1000,
                        link="dcim:rack_list",
                        permissions=["dcim.view_rack"],
                    ),
                    NavItem(
                        name="Rack Groups",
                        weight=1100,
                        link="dcim:rackgroup_list",
                        permissions=["dcim.view_rackgroup"],
                    ),
                    NavItem(
                        name="Rack Reservations",
                        weight=1200,
                        link="dcim:rackreservation_list",
                        permissions=["dcim.view_rackreservation"],
                    ),
                    NavItem(
                        name="Rack Elevations",
                        weight=1300,
                        link="dcim:rack_elevation_list",
                        permissions=["dcim.view_rack"],
                    ),
                ),
            ),
            NavGrouping(
                name="Organization",
                weight=200,
                items=(
                    NavItem(
                        link="dcim:location_list",
                        name="Locations",
                        weight=100,
                        permissions=[
                            "dcim.view_location",
                        ],
                    ),
                    NavItem(
                        link="dcim:locationtype_list",
                        name="Location Types",
                        weight=200,
                        permissions=[
                            "dcim.view_locationtype",
                        ],
                    ),
                ),
            ),
            # space reserved for Tenants at weight 300
            # space reserved for Circuits at weight 400
            NavGrouping(
                name="Power",
                weight=500,
                items=(
                    NavItem(
                        name="Power Feeds",
                        link="dcim:powerfeed_list",
                        weight=100,
                        permissions=["dcim.view_powerfeed"],
                    ),
                    NavItem(
                        name="Power Panels",
                        weight=200,
                        link="dcim:powerpanel_list",
                        permissions=["dcim.view_powerpanel"],
                    ),
                ),
            ),
        ),
    ),
)
