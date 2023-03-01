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
    "resident_management.menu_approve_account_resident" : "perm_approve_resident_user",

    "apartment_project.menu_blockhouse" : "perm_read_block_house",
    "apartment_project.menu_building" : "perm_read_building",
    "apartment_project.menu_building_floors" : "perm_read_floor",
    "apartment_project.menu_building_house" : "perm_read_apartment",

    "apartment_service_support.menu_banners_root" : "perm_read_advertisement",
    "apartment_service_support.menu_banners_list" : "perm_read_advertisement",
    "apartment_service_support.menu_banners_approve" : "perm_approve_advertisement",

    "apartment_service_support.menu_notification_root" : "perm_read_notification",
    "apartment_service_support.menu_notification_list" : "perm_read_notification",
    "apartment_service_support.menu_notification_approve" : "perm_approve_notification",

    "apartment_service_support.menu_news_root" : "perm_read_news",
    "apartment_service_support.menu_news_list" : "perm_read_news",
    "apartment_service_support.menu_news_approve" : "perm_approve_news",

    "apartment_service_support.menu_utilities_root" : "perm_read_utilities",
    "apartment_service_support.menu_utilities_list" : "perm_read_utilities",
    "apartment_service_support.menu_utilities_approve" : "perm_approve_utilities",

    "apartment_service_support.menu_resident_handbook_root" : "perm_read_handbook",
    "apartment_service_support.menu_resident_handbook_list" : "perm_read_handbook",
    "apartment_service_support.menu_resident_handbook_approve" : "perm_approve_handbook",

    "apartment_service_support.menu_access_card_root" : "perm_read_access_card",
    "apartment_service_support.menu_access_card_list" : "perm_read_access_card",
    "apartment_service_support.menu_access_card_approve" : "perm_approve_access_card",

    "apartment_service_support.menu_utilities_root" : "perm_read_utilities",
    "apartment_service_support.menu_utilities_list" : "perm_read_utilities",
    "apartment_service_support.menu_utilities_approve" : "perm_approve_utilities",

    "apartment_service_support.menu_complain_root" : "perm_read_complain",
    "apartment_service_support.menu_complain_list" : "perm_read_complain",
    "apartment_service_support.menu_complain_approve" : "perm_approve_complain",

    "apartment_service_support.menu_register_delivery_root" : "perm_read_delivery",
    "apartment_service_support.menu_register_delivery_list" : "perm_read_delivery",
    "apartment_service_support.menu_register_delivery_approve" : "perm_approve_delivery",

    "apartment_service_support.menu_resident_handbook_root" : "perm_read_handbook",
    "apartment_service_support.menu_resident_handbook_list" : "perm_read_handbook",
    "apartment_service_support.menu_resident_handbook_approve" : "perm_approve_handbook",

    "apartment_service_support.menu_vehicle_card_root" : "perm_read_vehicle",
    "apartment_service_support.menu_vehicle_card_list" : "perm_read_vehicle",
    "apartment_service_support.menu_vehicle_card_approve" : "perm_approve_vehicle",
}
const get_perm =  (perm) => rpc.query({
         model: 'res.users',
         method: 'check_perm_user',
         args: [perm],
    })
export const menuService = {
    dependencies: ["action", "router"],
    async start(env) {
        const fetchLoadMenus = makeFetchLoadMenus();
        const menusData = await fetchLoadMenus();

        let newMenusData = {}
//        const requests = Object.keys(defineMenuWithPerm).map(menuId=> {
//            var currentMenu = Object.keys(menusData).filter(menuKey=> menusData[menuKey].xmlid == menuId)
//            if(currentMenu && currentMenu.length > 0) {
//                var id = parseInt(currentMenu[0])
//                return get_perm(menusData[id].xmlid)
//            }
//        })
//        Promise.all(requests)
//        .then(result=>{
//            result.forEach(res=>{
//            })
//            if(result != undefined){
//               Object.keys(defineMenuWithPerm).forEach(menuId=>{
//                    var currentMenu = Object.keys(menusData).filter(menuKey=> menusData[menuKey].xmlid == menuId)
//                    if(currentMenu && currentMenu.length>0){
//                         var id = parseInt(currentMenu[0])
//                        menusData[id].invisible = !result
//                    }
//               })
//               Object.keys(menusData).forEach(menuId=>{
//                    if(menusData[menuId].children && menusData[menuId].children.length>0){
//                        var count_visible = 0
//                        var currentMenu = menusData[menuId]
//                        currentMenu.children.forEach(id=>{
//                            var a = newMenusData[id]
//                            if(menusData[id] && menusData[id].invisible) count_visible = count_visible + 1
//                        })
//                        if(count_visible == currentMenu.children.length) menusData[menuId].invisible = true
//                    }
//                })
//            }
//        })
        for (const menuId of Object.keys(menusData)){
           let checkMyMenu = Object.keys(defineMenuWithPerm).includes(menusData[menuId].xmlid)
           if(checkMyMenu){
               let check_perm = await get_perm(defineMenuWithPerm[menusData[menuId].xmlid])
               console.log(menusData[menuId].name + "------------" + defineMenuWithPerm[menusData[menuId].xmlid] + "----" + check_perm)
               menusData[menuId].invisible = !check_perm
           }
           newMenusData[menuId]=menusData[menuId]
        }
//        Object.keys(newMenusData).forEach(menuId=>{
//                if(newMenusData[menuId].children && newMenusData[menuId].children.length>0){
//                    var count_visible = 0
//                    var currentMenu = newMenusData[menuId]
//                    currentMenu.children.forEach(id=>{
//                        var a = newMenusData[id]
//                        if(newMenusData[id] && newMenusData[id].invisible) count_visible = count_visible + 1
//                    })
//                    if(count_visible == currentMenu.children.length) newMenusData[menuId].invisible = true
//                }
//        })

        return makeMenus(env, menusData, fetchLoadMenus);
    },
};

registry.category("services").add("menu", menuService);
