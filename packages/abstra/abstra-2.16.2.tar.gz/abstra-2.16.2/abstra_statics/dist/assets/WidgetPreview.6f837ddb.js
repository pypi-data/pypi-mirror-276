import{d as k,r as B,o as W,b as n,c as l,w as p,f as A,au as C,eJ as P,eC as S,f2 as D,u as m,bI as N,f8 as E,E as h,eG as V,eA as g,e as b,ey as c,eH as v,eI as q,aG as w,n as x,p as L}from"./outputWidgets.e5f9ffc6.js";import{S as $}from"./Steps.3108fe7f.js";import{W as F}from"./WidgetsFrame.0d60536e.js";(function(){try{var o=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(o._sentryDebugIds=o._sentryDebugIds||{},o._sentryDebugIds[t]="5cca9eb7-0718-4cb4-8ed3-05fb7f7e411c",o._sentryDebugIdIdentifier="sentry-dbid-5cca9eb7-0718-4cb4-8ed3-05fb7f7e411c")}catch{}})();const K=k({__name:"ActionButton",props:{action:{},displayName:{},disabled:{type:Boolean},loading:{type:Boolean}},emits:["click"],setup(o,{emit:t}){const d=o,u=B(null);return W(()=>{u.value&&d.action.setElement(u.value)}),(r,i)=>(n(),l(m(E),null,{default:p(()=>[A(m(N),{ref_key:"element",ref:u,class:S(["next-button",r.disabled?"disabled":""]),loading:r.loading,disabled:r.disabled,onClick:i[0]||(i[0]=f=>t("click")),onKeydown:i[1]||(i[1]=D(f=>t("click"),["enter"]))},{default:p(()=>[C(P(r.displayName),1)]),_:1},8,["loading","disabled","class"])]),_:1}))}});const G=h(K,[["__scopeId","data-v-e711f126"]]),J={class:"form"},M={class:"form-wrapper"},O={key:0,class:"buttons"},z=k({__name:"WidgetPreview",setup(o){const t=V(),d=B([]);function u(e){return x[e]||L[e]||null}function r(e){try{const s=JSON.parse(e);if(s.component=u(s.type),!s.component)throw new Error(`Widget ${s.type} not found`);return s.component?s:null}catch{return null}}function i(){const e=t.query.widget;return Array.isArray(e)?e.map(r).filter(Boolean):[r(e)]}function f(){return t.query.steps==="true"}function _(){const e=t.query.button;return e?Array.isArray(e)?e:[e]:[]}const y=e=>({name:e,isDefault:!1,isFocused:!1,focusOnButton:()=>{},addKeydownListener:()=>{},setElement:()=>{}});return(e,s)=>(n(),l(F,{"main-color":"#d14056",class:"preview",theme:"#fbfbfb","font-family":"Inter"},{default:p(()=>[f()?(n(),l($,{key:0,"steps-info":{current:2,total:3}})):g("",!0),b("div",J,[b("div",M,[(n(!0),c(w,null,v(i(),(a,I)=>(n(),c("div",{key:I,class:"widget"},[(n(),l(q(a.component),{"user-props":a.userProps,value:a.userProps.value,errors:d.value},null,8,["user-props","value","errors"]))]))),128))]),_().length?(n(),c("div",O,[(n(!0),c(w,null,v(_(),a=>(n(),l(G,{key:a,"display-name":y(a).name,action:y(a)},null,8,["display-name","action"]))),128))])):g("",!0)])]),_:1}))}});const Q=h(z,[["__scopeId","data-v-350e6330"]]);export{Q as default};
//# sourceMappingURL=WidgetPreview.6f837ddb.js.map
