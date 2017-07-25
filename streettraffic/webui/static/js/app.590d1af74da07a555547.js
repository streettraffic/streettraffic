webpackJsonp([6],{100:function(t,e,n){function i(t){n(88)}var a=n(8)(n(77),n(107),i,null,null);t.exports=a.exports},101:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-parallax",{staticClass:"elevation-12",attrs:{src:"https://raw.githubusercontent.com/vuetifyjs/docs/master/static/doc-images/parallax/material.jpg"}},[n("v-layout",{attrs:{column:"","align-center":"","justify-center":""}},[n("h1",{staticClass:"white--text"},[t._v("Histraffic.io")]),t._v(" "),n("h4",{staticClass:"white--text"},[t._v("Use historic traffic to plan traveling!")]),t._v(" "),n("div",{staticClass:"mt-5"},[n("v-btn",{staticClass:"green lighten-2",attrs:{dark:"",large:"",router:"",to:"/Main"}},[t._v("Get Started")])],1)])],1)},staticRenderFns:[]}},102:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("label",[n("span",{domProps:{textContent:t._s(t.label)}}),t._v(" "),n("input",{ref:"input",class:t.className,attrs:{type:"text",placeholder:t.placeholder}})])},staticRenderFns:[]}},103:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"vue-map-container"},[n("div",{ref:"vue-map",staticClass:"vue-map"}),t._v(" "),n("div",{staticClass:"vue-map-hidden"},[t._t("default")],2),t._v(" "),t._t("visible")],2)},staticRenderFns:[]}},104:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("div",{ref:"flyaway"},[t._t("default",[n("div",{domProps:{innerHTML:t._s(t.content)}})])],2)])},staticRenderFns:[]}},105:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-app",[n("v-navigation-drawer",{attrs:{persistent:"","enable-resize-watcher":"",dark:"","mini-variant":t.mini},on:{"update:miniVariant":function(e){t.mini=e}},model:{value:t.drawer,callback:function(e){t.drawer=e},expression:"drawer"}},[n("v-list",t._l(t.items,function(e,i){return n("v-list-item",{key:i},[n("v-list-tile",{attrs:{value:"true",router:"",to:e.routerAddress,ripple:""}},[n("v-list-tile-action",[n("v-icon",{attrs:{light:""},domProps:{innerHTML:t._s(e.icon)}})],1),t._v(" "),n("v-list-tile-content",[n("v-list-tile-title",{domProps:{textContent:t._s(e.title)}})],1)],1)],1)}))],1),t._v(" "),n("v-toolbar",{attrs:{light:""}},[n("v-toolbar-side-icon",{attrs:{light:""},nativeOn:{click:function(e){e.stopPropagation(),t.drawer=!t.drawer}}}),t._v(" "),n("v-toolbar-title",{domProps:{textContent:t._s(t.title)}}),t._v(" "),n("v-spacer")],1),t._v(" "),n("main",[n("v-container",{attrs:{fluid:""}},[n("transition",{attrs:{name:"slide",mode:"out-in"}},[n("router-view")],1)],1)],1),t._v(" "),n("v-footer",[n("span",[t._v("© 2017")])])],1)},staticRenderFns:[]}},106:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-app",[n("transition",{attrs:{name:"slide",mode:"out-in"}},[n("router-view")],1)],1)},staticRenderFns:[]}},107:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"vue-street-view-pano-container"},[n("div",{ref:"vue-street-view-pano",staticClass:"vue-street-view-pano"}),t._v(" "),t._t("default")],2)},staticRenderFns:[]}},108:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement;return(t._self._c||e)("input",{ref:"input",attrs:{type:"text",placeholder:t.placeholder},domProps:{value:t.value}})},staticRenderFns:[]}},44:function(t,e,n){"use strict";n.d(e,"b",function(){return i}),n.d(e,"a",function(){return a});var i="GET_HISTORIC_BATCH",a="SET_WS_CONNECTION_STATUS"},54:function(t,e,n){"use strict";var i=n(24),a=n(109),r=n(95),o=n.n(r),s=n(94),c=n.n(s);i.a.use(a.a);var u=function(){return{component:n.e(1).then(n.bind(null,165))}},l=function(){return{component:n.e(3).then(n.bind(null,163))}},d=function(){return{component:n.e(4).then(n.bind(null,166))}},f=function(){return{component:n.e(0).then(n.bind(null,167))}},p=function(){return{component:n.e(2).then(n.bind(null,164))}},v=new a.a({routes:[{path:"/",name:"Landing",component:c.a,meta:{title:"Histraffic Landing"}},{path:"/Main",component:o.a,meta:{title:"Histraffic Main"},children:[{path:"",name:"Home",component:u,meta:{title:"Histraffic Home"}},{path:"Analytics",name:"Analytics",component:l,meta:{title:"Histraffic Analytics"}},{path:"RouteLab",name:"RouteLab",component:f,meta:{title:"Histraffic RouteLab"}},{path:"Polygon",name:"Polygon",component:d,meta:{title:"Histraffic Polygon"}},{path:"CaseStudy",name:"CaseStudy",component:p,meta:{title:"Histraffic CaseStudy"}}]}]});v.beforeEach(function(t,e,n){document.title=t.meta.title,n()}),e.a=v},55:function(t,e,n){"use strict";var i,a=n(79),r=n.n(a),o=n(24),s=n(27),c=n(160),u=(n.n(c),n(69)),l=n(44);o.a.use(s.a);var d={ws_connection_status:!1,ws_address:"ws://localhost:8765/",ws:null,historic_batch:["A","B","C"]},f=(i={},r()(i,l.a,function(t,e){t.ws=e,t.ws_connection_status=!0}),r()(i,l.b,function(t,e){t.historic_batch=e}),i);e.a=new s.a.Store({state:d,mutations:f,actions:u,strict:!0})},56:function(t,e){},57:function(t,e,n){function i(t){n(87)}var a=n(8)(n(70),n(106),i,null,null);t.exports=a.exports},68:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n(24),a=n(58),r=n.n(a),o=n(27),s=n(45),c=(n.n(s),n(57)),u=n.n(c),l=n(54),d=n(55),f=n(56);n.n(f);i.a.use(s,{load:{key:"AIzaSyAucd0sk7vH1NjQyh3b2kN8qYKhdu4S1Ss",libraries:"places"}}),i.a.use(r.a),i.a.use(o.a),i.a.config.productionTip=!1,new i.a({el:"#app",router:l.a,store:d.a,template:"<App/>",components:{App:u.a}})},69:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),n.d(e,"setWsConnection",function(){return o}),n.d(e,"getHistoricBatch",function(){return s});var i=n(61),a=n.n(i),r=n(44),o=function(t){var e=t.commit,n=t.state,i=t.dispatch,a=new WebSocket(n.ws_address);a.onopen=function(){e(r.a,a),i("getHistoricBatch")},a.onclose=function(){alert("Opps, something went wrong, you have disconnected from the server. Try to refresh")}},s=function(t){var e=t.commit,n=t.state;n.ws.send(a()(["getHistoricBatch"])),n.ws.onmessage=function(t){e(r.b,JSON.parse(t.data))}}},70:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={created:function(){this.$store.dispatch("setWsConnection")}}},71:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={name:"Landing",data:function(){return{center:{lat:33.7601,lng:-84.37429},map_geojson:null,dialog:!1}},methods:{},created:function(){},mounted:function(){}}},72:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={name:"Main",data:function(){return{drawer:!0,mini:!1,items:[{icon:"home",title:"Home",routerAddress:"/Main"},{icon:"insert_chart",title:"Analytics",routerAddress:"/Main/Analytics"},{icon:"create",title:"Polygon",routerAddress:"/Main/Polygon"},{icon:"build",title:"RouteLab",routerAddress:"/Main/RouteLab"},{icon:"build",title:"CaseStudy",routerAddress:"/Main/CaseStudy"}],miniVariant:!1,title:"Histraffic"}},mounted:function(){}}},85:function(t,e){},86:function(t,e){},87:function(t,e){},88:function(t,e){},94:function(t,e,n){var i=n(8)(n(71),n(101),null,null,null);t.exports=i.exports},95:function(t,e,n){function i(t){n(86)}var a=n(8)(n(72),n(105),i,null,null);t.exports=a.exports},96:function(t,e,n){var i=n(8)(n(73),n(108),null,null,null);t.exports=i.exports},97:function(t,e,n){var i=n(8)(n(74),n(104),null,null,null);t.exports=i.exports},98:function(t,e,n){function i(t){n(85)}var a=n(8)(n(75),n(103),i,null,null);t.exports=a.exports},99:function(t,e,n){var i=n(8)(n(76),n(102),null,null,null);t.exports=i.exports}},[68]);
//# sourceMappingURL=app.590d1af74da07a555547.js.map