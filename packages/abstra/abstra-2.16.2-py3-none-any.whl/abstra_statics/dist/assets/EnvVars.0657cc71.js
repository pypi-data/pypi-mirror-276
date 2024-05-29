var x=Object.defineProperty;var A=(r,e,t)=>e in r?x(r,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):r[e]=t;var w=(r,e,t)=>(A(r,typeof e!="symbol"?e+"":e,t),t);import{C as j}from"./CrudView.542c4e4e.js";import{a as D}from"./asyncComputed.2210bd1a.js";import{G as P}from"./PhPencil.vue.155bd1a7.js";import{d as _,eG as G,r as E,D as U,b as k,ey as F,f as u,u as l,w as d,aG as N,eS as B,c as S,au as T,eJ as J,ct as K,eA as O}from"./outputWidgets.e5f9ffc6.js";import{C as c}from"./router.dd631582.js";import"./index.889e1616.js";import{A as R,F as q}from"./Form.b45c0335.js";import{A as z}from"./Text.e6c27a3b.js";import{M as H}from"./Modal.e18542c5.js";import"./DocsButton.vue_vue_type_script_setup_true_lang.670b5628.js";import"./BookOutlined.7d01e6a5.js";import"./url.c11ddd9f.js";import"./Paragraph.1cbc8077.js";import"./Base.d0d329e2.js";import"./index.2570caf9.js";import"./Title.f988141d.js";import"./index.f056a823.js";import"./popupNotifcation.9671db62.js";import"./record.3c5b5204.js";import"./pubsub.75396d00.js";import"./hasIn.54609e4a.js";(function(){try{var r=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(r._sentryDebugIds=r._sentryDebugIds||{},r._sentryDebugIds[e]="367b6d8f-38f7-4c4b-a5d4-7b06383643c7",r._sentryDebugIdIdentifier="sentry-dbid-367b6d8f-38f7-4c4b-a5d4-7b06383643c7")}catch{}})();class L{constructor(){w(this,"urlPath","env-vars")}async create(e){return c.post(`projects/${e.projectId}/${this.urlPath}`,{name:e.name,value:e.value})}async delete(e,t){await c.delete(`projects/${e}/${this.urlPath}/${t}`)}async update(e,t,a){await c.patch(`projects/${e}/${this.urlPath}/${t}`,{value:a})}async list(e){return c.get(`projects/${e}/${this.urlPath}`)}async get(e){return c.get(`${this.urlPath}/${e}`)}}const p=new L;class i{constructor(e,t){this.projectId=e,this.dto=t}static async list(e){return(await p.list(e)).map(a=>new i(e,a))}static async create(e,t,a){const m=await p.create({projectId:e,name:t,value:a});return new i(e,m)}static async get(e,t){const a=await p.get(t);return new i(e,a)}get key(){return this.dto.name}async delete(){await p.delete(this.projectId,this.key)}async update(e){await p.update(this.projectId,this.key,e)}}const ve=_({__name:"EnvVars",setup(r){const t=G().params.projectId,a=E({type:"idle"}),{loading:m,result:y,refetch:f}=D(()=>i.list(t)),g=[{label:"Variable name",key:"key"},{label:"Variable value",key:"value",type:"multiline-text"}];async function h({key:s,value:n}){await i.create(t,s,n),f()}function $(s){a.value={type:"update-value",key:s.key,newValue:""}}async function v(s){var n;if(a.value.type==="update-value"&&s){const{key:o,newValue:V}=a.value,b=(n=y.value)==null?void 0:n.find(I=>I.key===o);b&&await b.update(V)}a.value={type:"idle"}}const C=U(()=>{var s,n;return{columns:[{name:"Key"},{name:"",align:"right"}],rows:(n=(s=y.value)==null?void 0:s.map(o=>({key:o.key,cells:[{type:"text",text:o.key},{type:"actions",actions:[{icon:B,label:"Delete",async onClick(){await o.delete(),f()},dangerous:!0},{icon:P,label:"Update value",onClick(){$(o)}}]}]})))!=null?n:[]}});return(s,n)=>(k(),F(N,null,[u(j,{"entity-name":"Env var",loading:l(m),title:"Environment Variables",description:"Set environment variables for your project.","empty-title":"No environment variables set",table:C.value,"create-button-text":"Add Environment Variable",fields:g,onCreate:h},null,8,["loading","table"]),u(l(H),{open:a.value.type==="update-value",title:"Update value",onCancel:n[1]||(n[1]=o=>v(!1)),onOk:n[2]||(n[2]=o=>v(!0))},{default:d(()=>[a.value.type==="update-value"?(k(),S(l(q),{key:0,layout:"vertical"},{default:d(()=>[u(l(R),null,{default:d(()=>[u(l(z),null,{default:d(()=>[T(J(a.value.key),1)]),_:1}),u(l(K),{value:a.value.newValue,"onUpdate:value":n[0]||(n[0]=o=>a.value.newValue=o)},null,8,["value"])]),_:1})]),_:1})):O("",!0)]),_:1},8,["open"])],64))}});export{ve as default};
//# sourceMappingURL=EnvVars.0657cc71.js.map
