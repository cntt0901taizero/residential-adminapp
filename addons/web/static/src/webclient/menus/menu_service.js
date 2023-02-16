/** @odoo-module **/

import { browser } from "../../core/browser/browser";
import { registry } from "../../core/registry";
import { session } from "@web/session";

const loadMenusUrl = `/web/webclient/load_menus`;
var rpc = require('web.rpc');

function makeFetchLoadMenus() {
    const cacheHashes = session.cache_hashes;
    let loadMenusHash = cacheHashes.load_menus || new Date().getTime().toString();
    return async function fetchLoadMenus(reload) {
        if (reload) {
            loadMenusHash = new Date().getTime().toString();
        } else if (odoo.loadMenusPromise) {
            return odoo.loadMenusPromise;
        }
        const res = await browser.fetch(`${loadMenusUrl}/${loadMenusHash}`);
        if (!res.ok) {
            throw new Error("Error while fetching menus");
        }
        return res.json();
    };
}

function makeMenus(env, menusData, fetchLoadMenus) {
    let currentAppId;
    return {
        getAll() {
            return Object.values(menusData);
        },
        getApps() {
            return this.getMenu("root").children.map((mid) => this.getMenu(mid));
        },
        getMenu(menuID) {
            return menusData[menuID];
        },
        getCurrentApp() {
            if (!currentAppId) {
                return;
            }
            return this.getMenu(currentAppId);
        },
        getMenuAsTree(menuID) {
            const menu = this.getMenu(menuID);
            if (!menu.childrenTree) {
                menu.childrenTree = menu.children.map((mid) => this.getMenuAsTree(mid));
            }
            return menu;
        },
        async selectMenu(menu) {
            menu = typeof menu === "number" ? this.getMenu(menu) : menu;
            if (!menu.actionID) {
                return;
            }
            await env.services.action.doAction(menu.actionID, { clearBreadcrumbs: true });
            this.setCurrentMenu(menu);
        },
        setCurrentMenu(menu) {
            menu = typeof menu === "number" ? this.getMenu(menu) : menu;
            if (menu && menu.appID !== currentAppId) {
                currentAppId = menu.appID;
                env.bus.trigger("MENUS:APP-CHANGED");
                // FIXME: lock API: maybe do something like
                // pushState({menu_id: ...}, { lock: true}); ?
                env.services.router.pushState({ menu_id: menu.id }, { lock: true });
            }
        },
        async reload() {
            if (fetchLoadMenus) {
                menusData = await fetchLoadMenus(true);

                env.bus.trigger("MENUS:APP-CHANGED");
            }
        },
    };
}

const defineMenuWithPerm = {
    "resident_management.menu_account_admin" : "perm_read_admin_user",
    "resident_management.menu_account_resident" : "perm_read_resident_user",
    "resident_management.menu_account_resident" : "perm_read_resident_user",
}
export const menuService = {
    dependencies: ["action", "router"],
    async start(env) {
        const fetchLoadMenus = makeFetchLoadMenus();
        const menusData = await fetchLoadMenus();
        console.log(menusData);
        var newMenusData = {}
        Object.keys(menusData).forEach(async menuId => {
           var checkMyMenu = Object.keys(defineMenuWithPerm).includes(menusData[menuId].xmlid)
           if(checkMyMenu){
               var check_perm = await rpc.query({
                                model: 'res.users',
                                method: 'check_perm_create',
                                args: [defineMenuWithPerm[menusData[menuId].xmlid]],
                            })
               console.log(check_perm + "44444")
               console.log(menusData[menuId].name + "------------" + defineMenuWithPerm[menusData[menuId].xmlid])
               menusData[menuId].invisible = !check_perm
           }
            newMenusData[menuId]=menusData[menuId]
        })
        return makeMenus(env, newMenusData, fetchLoadMenus);
    },
};

registry.category("services").add("menu", menuService);
