import{f as o,eK as p,d as b,b as y,c as m,w as r,u as i,au as d,eJ as c,m as g,bI as v,cC as _}from"./outputWidgets.e5f9ffc6.js";import{a as f}from"./Base.d0d329e2.js";import{A as P}from"./index.2570caf9.js";(function(){try{var a=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(a._sentryDebugIds=a._sentryDebugIds||{},a._sentryDebugIds[t]="719db195-3efe-416e-9694-9d549b4cb6db",a._sentryDebugIdIdentifier="sentry-dbid-719db195-3efe-416e-9694-9d549b4cb6db")}catch{}})();var w={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm144.1 454.9L437.7 677.8a8.02 8.02 0 01-12.7-6.5V353.7a8 8 0 0112.7-6.5L656.1 506a7.9 7.9 0 010 12.9z"}}]},name:"play-circle",theme:"filled"};const C=w;function u(a){for(var t=1;t<arguments.length;t++){var e=arguments[t]!=null?Object(arguments[t]):{},l=Object.keys(e);typeof Object.getOwnPropertySymbols=="function"&&(l=l.concat(Object.getOwnPropertySymbols(e).filter(function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),l.forEach(function(n){h(a,n,e[n])})}return a}function h(a,t,e){return t in a?Object.defineProperty(a,t,{value:e,enumerable:!0,configurable:!0,writable:!0}):a[t]=e,a}var s=function(t,e){var l=u({},t,e.attrs);return o(p,u({},l,{icon:C}),null)};s.displayName="PlayCircleFilled";s.inheritAttrs=!1;const O=s,D=b({__name:"RunButton",props:{loading:{type:Boolean},disabled:{}},emits:["click","save"],setup(a,{emit:t}){return(e,l)=>(y(),m(i(_),{open:e.disabled?void 0:!1,placement:"bottom"},{content:r(()=>[o(i(P),{vertical:"",gap:"small"},{default:r(()=>[o(i(f),{style:{"font-size":"16px"}},{default:r(()=>{var n;return[d(c((n=e.disabled)==null?void 0:n.title),1)]}),_:1}),o(i(f),null,{default:r(()=>{var n;return[d(c((n=e.disabled)==null?void 0:n.message),1)]}),_:1})]),_:1})]),default:r(()=>[o(i(v),{style:{width:"100%"},loading:e.loading,icon:g(i(O)),disabled:!!e.disabled,size:"large",type:"primary",onClick:l[0]||(l[0]=n=>t("click"))},{default:r(()=>[d(" Run ")]),_:1},8,["loading","icon","disabled"])]),_:1},8,["open"]))}});export{D as _};
//# sourceMappingURL=RunButton.vue_vue_type_script_setup_true_lang.919f85ec.js.map
