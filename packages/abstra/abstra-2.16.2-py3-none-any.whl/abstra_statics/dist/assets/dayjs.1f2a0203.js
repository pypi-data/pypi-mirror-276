import{Y as a,d as I,b5 as O,bq as E,r as N,f as _,W as i,V as B,aB as u,aA as U}from"./outputWidgets.e5f9ffc6.js";import{c as H,e as R,f as V,r as W,d as q}from"./index.92c9f46d.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},p=new Error().stack;p&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[p]="09f48a58-c87c-438e-afa7-a15ca6ef78ac",t._sentryDebugIdIdentifier="sentry-dbid-09f48a58-c87c-438e-afa7-a15ca6ef78ac")}catch{}})();const T=()=>({format:String,showNow:u(),showHour:u(),showMinute:u(),showSecond:u(),use12Hours:u(),hourStep:Number,minuteStep:Number,secondStep:Number,hideDisabledOptions:u(),popupClassName:String,status:U()});function G(t){const p=H(t,a(a({},T()),{order:{type:Boolean,default:!0}})),{TimePicker:x,RangePicker:S}=p,D=I({name:"ATimePicker",inheritAttrs:!1,props:a(a(a(a({},R()),V()),T()),{addon:{type:Function}}),slots:Object,setup(f,g){let{slots:c,expose:C,emit:o,attrs:h}=g;const r=f,s=O();E(!(c.addon||r.addon),"TimePicker","`addon` is deprecated. Please use `v-slot:renderExtraFooter` instead.");const d=N();C({focus:()=>{var n;(n=d.value)===null||n===void 0||n.focus()},blur:()=>{var n;(n=d.value)===null||n===void 0||n.blur()}});const k=(n,F)=>{o("update:value",n),o("change",n,F),s.onFieldChange()},P=n=>{o("update:open",n),o("openChange",n)},b=n=>{o("focus",n)},v=n=>{o("blur",n),s.onFieldBlur()},y=n=>{o("ok",n)};return()=>{const{id:n=s.id.value}=r;return _(x,i(i(i({},h),B(r,["onUpdate:value","onUpdate:open"])),{},{id:n,dropdownClassName:r.popupClassName,mode:void 0,ref:d,renderExtraFooter:r.addon||c.addon||r.renderExtraFooter||c.renderExtraFooter,onChange:k,onOpenChange:P,onFocus:b,onBlur:v,onOk:y}),c)}}}),j=I({name:"ATimeRangePicker",inheritAttrs:!1,props:a(a(a(a({},R()),W()),T()),{order:{type:Boolean,default:!0}}),slots:Object,setup(f,g){let{slots:c,expose:C,emit:o,attrs:h}=g;const r=f,s=N(),d=O();C({focus:()=>{var e;(e=s.value)===null||e===void 0||e.focus()},blur:()=>{var e;(e=s.value)===null||e===void 0||e.blur()}});const k=(e,l)=>{o("update:value",e),o("change",e,l),d.onFieldChange()},P=e=>{o("update:open",e),o("openChange",e)},b=e=>{o("focus",e)},v=e=>{o("blur",e),d.onFieldBlur()},y=(e,l)=>{o("panelChange",e,l)},n=e=>{o("ok",e)},F=(e,l,A)=>{o("calendarChange",e,l,A)};return()=>{const{id:e=d.id.value}=r;return _(S,i(i(i({},h),B(r,["onUpdate:open","onUpdate:value"])),{},{id:e,dropdownClassName:r.popupClassName,picker:"time",mode:void 0,ref:s,onChange:k,onOpenChange:P,onFocus:b,onBlur:v,onPanelChange:y,onOk:n,onCalendarChange:F}),c)}}});return{TimePicker:D,TimeRangePicker:j}}const{TimePicker:m,TimeRangePicker:w}=G(q),$=a(m,{TimePicker:m,TimeRangePicker:w,install:t=>(t.component(m.name,m),t.component(w.name,w),t)});export{$ as T,w as a};
//# sourceMappingURL=dayjs.1f2a0203.js.map
