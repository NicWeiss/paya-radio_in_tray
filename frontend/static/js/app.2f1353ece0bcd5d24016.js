webpackJsonp([1],{"0hzV":function(t,e){t.exports="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMTE2IDI5NiAyNCAyNCI+PHBhdGggZD0iTTEyMCAyOThoNnYyMGgtNnptMTAgMGg2djIwaC02eiIvPjwvc3ZnPg=="},HUwH:function(t,e){t.exports="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MiIgaGVpZ2h0PSI1MiI+PHBhdGggZD0iTTM2IDI4VjE3SDE5Yy0xLjEgMC0yIC45LTIgMiAwIC41LjIuOS41IDEuMy0uNi4zLTEgMS0xIDEuN3MuMyAxLjMuOCAxLjZjLS44LjMtMS4zIDEtMS4zIDEuOSAwIC44LjQgMS40IDEgMS44LS42LjMtMSAxLTEgMS44IDAgMS4xLjkgMiAyIDJoNWMtLjUgMS41LTEgMy40LTEgNC41IDAgMy4zIDIuNSAzLjUgMi41IDMuNS44IDAgMS41LS4zIDEuNS0xdi0xLjVjMC0xLjQgNi04LjYgNy41LTguNUwzNiAyOHoiIGZpbGw9IiMyMjIiLz48L3N2Zz4="},NHnr:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=r("7+uW"),n=r("NYxO"),s=(r("m3Wc"),{render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]}),i=r("VU/8")({name:"App"},s,!1,null,null,null).exports,c=r("/ocq"),u=r("Xxa5"),o=r.n(u),l=r("exGp"),M=r.n(l),p=r("//Fk"),d=r.n(p),g=r("Gu7T"),v=r.n(g),L={setSession:function(t){localStorage.setItem("session",t)},getSession:function(){return localStorage.getItem("session")},isAuthenticated:function(){return!!localStorage.getItem("session")},invalidateSession:function(){localStorage.setItem("session","")}},y=r("VU/8")(L,null,!1,null,null,null).exports,m={get:function(){for(var t=arguments.length,e=Array(t),r=0;r<t;r++)e[r]=arguments[r];return this.doRequest.apply(this,["get"].concat(v()(e)))},put:function(){for(var t=arguments.length,e=Array(t),r=0;r<t;r++)e[r]=arguments[r];return this.doRequest.apply(this,["put"].concat(v()(e)))},post:function(){for(var t=arguments.length,e=Array(t),r=0;r<t;r++)e[r]=arguments[r];return this.doRequest.apply(this,["post"].concat(v()(e)))},delete:function(){for(var t=arguments.length,e=Array(t),r=0;r<t;r++)e[r]=arguments[r];return this.doRequest.apply(this,["delete"].concat(v()(e)))},doRequest:function(t,e){var r={method:t,url:"http://127.0.0.1:7778/api"+e,headers:{"Content-Type":"application/json; charset=UTF-8"},data:arguments.length>2&&void 0!==arguments[2]?arguments[2]:null,json:!0};return y.isAuthenticated()&&(r.headers.session=y.getSession()),axios.defaults.headers.post["Access-Control-Allow-Origin"]="*",axios.defaults.headers.post["Access-Control-Allow-Headers"]="*",new d.a(function(t,e){axios(r).then(function(e){t(e.data)}).catch(function(t){"TOKEN EXPIRED"===t.data&&(console.log("asdas"),y.invalidateSession(),window.location.replace("/")),e(t)})}.bind(this))}},w=r("VU/8")(m,null,!1,null,null,null).exports,x={name:"Login",data:function(){return{login:"",password:""}},methods:{check:function(){var t=this;return M()(o.a.mark(function e(){var r;return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return r=null,e.prev=1,e.next=4,w.get("/client");case 4:r=e.sent,y.setSession(r.token),e.next=13;break;case 8:return e.prev=8,e.t0=e.catch(1),console.log("error: ",e.t0),y.invalidateSession(),e.abrupt("return");case 13:console.log(r),t.$router.push("/");case 15:case"end":return e.stop()}},e,t,[[1,8]])}))()},logIn:function(){var t=this;return M()(o.a.mark(function e(){var r;return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return r=null,e.prev=1,e.next=4,w.post("/auth?user="+t.login+"&password="+t.password);case 4:r=e.sent,y.setSession(r.token),e.next=13;break;case 8:return e.prev=8,e.t0=e.catch(1),console.log("error: ",e.t0),y.invalidateSession(),e.abrupt("return");case 13:console.log(r),t.$router.push("/");case 15:case"end":return e.stop()}},e,t,[[1,8]])}))()}},created:function(){this.check()}},j={render:function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"container"},[r("form",{staticClass:"login-form"},[r("div",{staticClass:"form-group mb-3"},[r("label",{attrs:{for:"exampleInputEmail1"}},[t._v("Email address")]),t._v(" "),r("input",{directives:[{name:"model",rawName:"v-model",value:t.login,expression:"login"}],staticClass:"form-control",attrs:{type:"email",id:"exampleInputEmail1","aria-describedby":"emailHelp",placeholder:"Enter email"},domProps:{value:t.login},on:{input:function(e){e.target.composing||(t.login=e.target.value)}}}),t._v(" "),r("small",{staticClass:"form-text text-muted",attrs:{id:"emailHelp"}},[t._v("We'll never share your email with anyone else.")])]),t._v(" "),r("div",{staticClass:"form-group mb-4"},[r("label",{attrs:{for:"exampleInputPassword1"}},[t._v("Password")]),t._v(" "),r("input",{directives:[{name:"model",rawName:"v-model",value:t.password,expression:"password"}],staticClass:"form-control",attrs:{type:"password",id:"exampleInputPassword1",placeholder:"Password"},domProps:{value:t.password},on:{input:function(e){e.target.composing||(t.password=e.target.value)}}})]),t._v(" "),r("button",{staticClass:"btn btn-primary",attrs:{type:"submit"},on:{click:function(e){return e.preventDefault(),t.logIn(e)}}},[t._v("\n      Submit\n    ")])])])},staticRenderFns:[]},h=r("VU/8")(x,j,!1,null,null,null).exports,N={name:"Player",components:{},methods:{check:function(){var t=this;return M()(o.a.mark(function e(){var r;return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return r=null,e.prev=1,e.next=4,w.get("/client");case 4:r=e.sent,y.setSession(r.token),e.next=14;break;case 8:return e.prev=8,e.t0=e.catch(1),console.log("error: ",e.t0),y.invalidateSession(),t.$router.push("/login"),e.abrupt("return");case 14:case"end":return e.stop()}},e,t,[[1,8]])}))()},dislike:function(){var t=this;return M()(o.a.mark(function e(){return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,w.post("/dislike");case 3:e.next=8;break;case 5:return e.prev=5,e.t0=e.catch(0),e.abrupt("return");case 8:t.get_track(!0);case 9:case"end":return e.stop()}},e,t,[[0,5]])}))()},pause:function(){var t=this;return M()(o.a.mark(function e(){return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,w.post("/pause");case 3:e.next=8;break;case 5:return e.prev=5,e.t0=e.catch(0),e.abrupt("return");case 8:"Paused"==t.state?t.state="Playing":t.state="Paused";case 9:case"end":return e.stop()}},e,t,[[0,5]])}))()},play:function(){var t=this;return M()(o.a.mark(function e(){return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,w.post("/play");case 3:e.next=8;break;case 5:return e.prev=5,e.t0=e.catch(0),e.abrupt("return");case 8:t.state="Playing",t.get_track();case 10:case"end":return e.stop()}},e,t,[[0,5]])}))()},like:function(){var t=this;return M()(o.a.mark(function e(){return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,w.post("/like");case 3:e.next=8;break;case 5:return e.prev=5,e.t0=e.catch(0),e.abrupt("return");case 8:t.get_track();case 9:case"end":return e.stop()}},e,t,[[0,5]])}))()},next:function(){var t=this;return M()(o.a.mark(function e(){return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,w.post("/next");case 3:e.next=8;break;case 5:return e.prev=5,e.t0=e.catch(0),e.abrupt("return");case 8:t.get_track(!0);case 9:case"end":return e.stop()}},e,t,[[0,5]])}))()},get_track:function(){var t=this,e=arguments.length>0&&void 0!==arguments[0]&&arguments[0];return M()(o.a.mark(function r(){var a;return o.a.wrap(function(r){for(;;)switch(r.prev=r.next){case 0:return a=null,r.prev=1,r.next=4,w.get("/track");case 4:a=r.sent,r.next=10;break;case 7:return r.prev=7,r.t0=r.catch(1),r.abrupt("return");case 10:t.track=a.track,t.cover="data:image/png;base64, "+t.track.cover,e&&(t.playPercent=0);case 13:case"end":return r.stop()}},r,t,[[1,7]])}))()},history:function(){var t=this;return M()(o.a.mark(function e(){var r;return o.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return r=null,t.prev=1,t.next=4,w.get("/history");case 4:r=t.sent,t.next=10;break;case 7:return t.prev=7,t.t0=t.catch(1),t.abrupt("return");case 10:console.log(r);case 11:case"end":return t.stop()}},e,t,[[1,7]])}))()},get_player:function(){var t=this;return M()(o.a.mark(function e(){var r;return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return r=null,e.prev=1,e.next=4,w.get("/player_state");case 4:r=e.sent,e.next=10;break;case 7:return e.prev=7,e.t0=e.catch(1),e.abrupt("return");case 10:t.player=r.player_state,t.duration=t.player.track_duration,t.playInkrement=.5/(t.duration/100*.001),t.playPercent=Number((t.player.current_time*(100/t.player.track_duration)).toFixed(2)),t.state=t.player.state,t.track&&t.track.id==t.player.playing_track_id||t.get_track();case 16:case"end":return e.stop()}},e,t,[[1,7]])}))()},inkrement_progressbar:function(){var t=this;return M()(o.a.mark(function e(){var r,a;return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:if("Playing"==t.state){e.next=2;break}return e.abrupt("return");case 2:if(t.playPercent=Number((Number(t.playPercent)+Number(t.playInkrement)).toFixed(2)),!(t.playPercent>100.2)){e.next=16;break}r=!1,a=t.track.id;case 6:if(0!=r){e.next=13;break}return e.next=9,t.get_track();case 9:a!=t.track.id&&(r=!0),setTimeout(function(){},500),e.next=6;break;case 13:return e.next=15,t.get_player();case 15:t.playPercent=0;case 16:case"end":return e.stop()}},e,t)}))()}},created:function(){var t=this;this.playPercent=0,this.state="",this.cover="",this.check(),this.get_track(),this.get_player();setInterval(function(){return t.get_player()},15e3),setInterval(function(){return t.inkrement_progressbar()},500)},data:function(){return{track:this.track,state:this.state,cover:this.cover,playPercent:this.playPercent}}},I={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"player"},[t._m(0),t._v(" "),t.track?a("div",[a("div",{staticClass:"player-body"},[a("div",{staticClass:"cover-section"},[a("img",{staticClass:"background-cover",attrs:{src:t.cover}}),t._v(" "),a("div",{staticClass:"cover-wrapper"},[a("img",{staticClass:"cover",attrs:{src:t.cover}})])]),t._v(" "),a("div",{staticClass:"control-section"},[a("div",{staticClass:"track-info"},[a("div",{staticClass:"title"},[t._v(t._s(t.track.title))]),t._v(" "),a("div",{staticClass:"artists"},[t._v(t._s(t.track.artists.join(", ")))])]),t._v(" "),a("div",{staticClass:"track-control"},[a("progress",{staticClass:"progress",attrs:{id:"file",max:"100"},domProps:{value:t.playPercent}}),t._v(" "),a("div",{staticClass:"controls"},[a("button",{staticClass:"btn btn-secondary btn-circle",on:{click:t.history}},[a("img",{attrs:{src:r("VPAs")}})]),t._v(" "),a("div",[a("button",{staticClass:"btn btn-circle",class:t.track.is_disliked?"btn-primary-selected":"btn-primary",on:{click:t.dislike}},[a("img",{staticClass:"svg-from-yandex svg-big",attrs:{src:r("HUwH")}})]),t._v(" "),"Playing"==t.state?a("button",{staticClass:"btn btn-primary btn-circle-big",on:{click:t.pause}},[a("img",{staticClass:"svg-big",attrs:{src:r("0hzV")}})]):a("button",{staticClass:"btn btn-primary btn-circle-big",on:{click:t.play}},[a("img",{staticClass:"svg-big",attrs:{src:r("dYrp")}})]),t._v(" "),a("button",{staticClass:"btn btn-circle",class:t.track.is_liked?"btn-primary-selected":"btn-primary",on:{click:t.like}},[a("img",{staticClass:"svg-from-yandex svg-big",attrs:{src:r("fCfL")}})])]),t._v(" "),a("button",{staticClass:"btn btn-primary btn-circle",on:{click:t.next}},[a("img",{attrs:{src:r("dZat")}})])])])])])]):t._e()])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"header"},[e("div",{staticClass:"station"},[this._v("On your wave")])])}]};var f=r("VU/8")(N,I,!1,function(t){r("tFdc")},null,null).exports,C={render:function(){var t=this.$createElement;return(this._self._c||t)("div",[this._v("404: Страница не найдена")])},staticRenderFns:[]};r("VU/8")({data:function(){return{}}},C,!1,null,null,null).exports;a.a.use(c.a);var z=new c.a({mode:"history",routes:[{path:"/login",name:"Login",component:h,meta:{onlyGuest:!0}},{path:"/",name:"Player",component:f,meta:{requiresAuth:!0}},{path:"*",redirect:"/login"}]});z.beforeEach(function(t,e,r){if(t.matched.some(function(t){return t.meta.onlyGuest})&&y.isAuthenticated())r("/");else{if(t.matched.some(function(t){return t.meta.requiresAuth})){if(y.isAuthenticated())return void r();r("/login")}r()}});var b=z;a.a.config.productionTip=!1,a.a.use(n.a);var D=new n.a.Store({state:{test:0},mutations:{setTest:function(t,e){t.test=e}},getters:{getTest:function(t){return t.test}}});new a.a({el:"#app",router:b,store:D,components:{App:i},template:"<App/>"})},VPAs:function(t,e){t.exports="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gU3ZnIFZlY3RvciBJY29ucyA6IGh0dHA6Ly93d3cub25saW5ld2ViZm9udHMuY29tL2ljb24gLS0+DQo8IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPg0KPHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IiB2aWV3Qm94PSIwIDAgMTAwMCAxMDAwIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCAxMDAwIDEwMDAiIHhtbDpzcGFjZT0icHJlc2VydmUiPg0KPG1ldGFkYXRhPiBTdmcgVmVjdG9yIEljb25zIDogaHR0cDovL3d3dy5vbmxpbmV3ZWJmb250cy5jb20vaWNvbiA8L21ldGFkYXRhPg0KPGc+PGc+PGc+PHBhdGggZD0iTTUwMCwxMEMyMjkuNCwxMCwxMCwyMjkuNCwxMCw1MDBjMCwyNzAuNiwyMTkuNCw0OTAsNDkwLDQ5MGMyNzAuNiwwLDQ5MC0yMTkuNCw0OTAtNDkwQzk5MCwyMjkuNCw3NzAuNiwxMCw1MDAsMTB6IE01MDAsOTEzLjRDMjcxLjcsOTEzLjQsODYuNiw3MjguMyw4Ni42LDUwMFMyNzEuNyw4Ni42LDUwMCw4Ni42UzkxMy40LDI3MS43LDkxMy40LDUwMFM3MjguMyw5MTMuNCw1MDAsOTEzLjR6Ii8+PHBhdGggZD0iTTMxNi4zLDU5MS45Yy0xNi45LDAtMzAuNiwxMy43LTMwLjYsMzAuNnMxMy43LDMwLjYsMzAuNiwzMC42czMwLjYtMTMuNywzMC42LTMwLjZTMzMzLjIsNTkxLjksMzE2LjMsNTkxLjl6Ii8+PHBhdGggZD0iTTMxNi4zLDQ2OS40Yy0xNi45LDAtMzAuNiwxMy43LTMwLjYsMzAuNnMxMy43LDMwLjYsMzAuNiwzMC42czMwLjYtMTMuNywzMC42LTMwLjZTMzMzLjIsNDY5LjQsMzE2LjMsNDY5LjR6Ii8+PHBhdGggZD0iTTMxNi4zLDM0Ni45Yy0xNi45LDAtMzAuNiwxMy43LTMwLjYsMzAuNnMxMy43LDMwLjYsMzAuNiwzMC42czMwLjYtMTMuNywzMC42LTMwLjZTMzMzLjIsMzQ2LjksMzE2LjMsMzQ2Ljl6Ii8+PHBhdGggZD0iTTcxNC40LDM2Mi4yYzAtOC41LTYuOC0xNS4zLTE1LjMtMTUuM0g0MjMuNGMtOC41LDAtMTUuMyw2LjgtMTUuMywxNS4zdjMwLjZjMCw4LjUsNi44LDE1LjMsMTUuMywxNS4zaDI3NS42YzguNSwwLDE1LjMtNi44LDE1LjMtMTUuM1YzNjIuMnoiLz48cGF0aCBkPSJNNzE0LjQsNDg0LjdjMC04LjUtNi44LTE1LjMtMTUuMy0xNS4zSDQyMy40Yy04LjUsMC0xNS4zLDYuOC0xNS4zLDE1LjN2MzAuNmMwLDguNSw2LjgsMTUuMywxNS4zLDE1LjNoMjc1LjZjOC41LDAsMTUuMy02LjgsMTUuMy0xNS4zVjQ4NC43eiIvPjxwYXRoIGQ9Ik03MTQuNCw2MDcuMmMwLTguNS02LjgtMTUuMy0xNS4zLTE1LjNINDIzLjRjLTguNSwwLTE1LjMsNi44LTE1LjMsMTUuM3YzMC42YzAsOC41LDYuOCwxNS4zLDE1LjMsMTUuM2gyNzUuNmM4LjUsMCwxNS4zLTYuOCwxNS4zLTE1LjNWNjA3LjJ6Ii8+PC9nPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48Zz48L2c+PGc+PC9nPjxnPjwvZz48L2c+DQo8L3N2Zz4="},dYrp:function(t,e){t.exports="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHBhdGggZmlsbD0iIzAxMDEwMSIgZD0iTTQgMTQuMzI3TDE0Ljk2IDggNCAxLjY3MnoiLz48L3N2Zz4="},dZat:function(t,e){t.exports="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCI+PHBhdGggZD0iTTE5IDEwLjg4OUwzIDJ2MjBsMTYtOC44ODlWMjJoMlYyaC0ydjguODg5eiIgZmlsbD0iIzAwMCIvPjwvc3ZnPg=="},fCfL:function(t,e){t.exports="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MiIgaGVpZ2h0PSI1MiI+PHBhdGggZD0iTTM2IDI2LjVjMC0uOC0uNC0xLjQtMS0xLjguNi0uMyAxLTEgMS0xLjggMC0xLjEtLjktMi0yLTJoLTVjLjUtMS41IDEtMy40IDEtNC41IDAtMy4zLTIuNS0zLjUtMi41LTMuNS0uOCAwLTEuNS4zLTEuNSAxdjEuNWMwIDEuNC01LjUgOC42LTcgOC41aC0zdjExaDE3YzEuMSAwIDItLjkgMi0yIDAtLjUtLjItLjktLjUtMS4zLjYtLjMgMS0xIDEtMS43cy0uMy0xLjMtLjgtMS42Yy43LS4yIDEuMy0uOSAxLjMtMS44eiIgZmlsbD0iIzIyMiIvPjwvc3ZnPg=="},m3Wc:function(t,e){},tFdc:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.2f1353ece0bcd5d24016.js.map