import{a as g}from"./asyncComputed.2210bd1a.js";import{d as y,eG as _,o as w,u as e,b as f,c as b,ey as x,f as a,w as o,au as l,bI as I,e as h,eJ as C}from"./outputWidgets.e5f9ffc6.js";import{c as p}from"./router.dd631582.js";import"./index.889e1616.js";import{O as k}from"./organization.5e74a4d5.js";import{L as v}from"./LoadingContainer.907690df.js";import{A}from"./Title.f988141d.js";import{A as B}from"./index.2570caf9.js";import{A as D}from"./index.bcb82cdd.js";import{C as N}from"./Card.a9237487.js";import"./Form.b45c0335.js";import"./hasIn.54609e4a.js";import"./popupNotifcation.9671db62.js";import"./record.3c5b5204.js";import"./pubsub.75396d00.js";import"./Base.d0d329e2.js";import"./TabPane.b891a337.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},n=new Error().stack;n&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[n]="716c39f1-7ff8-4a07-8ec4-fc2efc8d1266",t._sentryDebugIdIdentifier="sentry-dbid-716c39f1-7ff8-4a07-8ec4-fc2efc8d1266")}catch{}})();const z={key:1},M={style:{display:"flex","justify-content":"flex-start","font-size":"24px"}},Y=y({__name:"Billing",setup(t){const r=_().params.organizationId,{loading:c,result:m}=g(()=>k.get(r));w(()=>{location.search.includes("upgrade")&&p.showNewMessage("I want to upgrade my plan")});const u=()=>p.showNewMessage("I want to upgrade my plan");return(V,j)=>e(c)?(f(),b(v,{key:0})):(f(),x("div",z,[a(e(B),{justify:"space-between",align:"center"},{default:o(()=>[a(e(A),{level:3},{default:o(()=>[l("Current plan")]),_:1})]),_:1}),a(e(D),{style:{"margin-top":"0"}}),a(e(N),{style:{width:"300px"},title:"Plan"},{extra:o(()=>[a(e(I),{onClick:u},{default:o(()=>[l("Upgrade")]),_:1})]),default:o(()=>{var s,i,d;return[h("div",M,C((d=(i=(s=e(m))==null?void 0:s.billingMetadata)==null?void 0:i.plan)!=null?d:"No active plan"),1)]}),_:1})]))}});export{Y as default};
//# sourceMappingURL=Billing.7a779575.js.map
