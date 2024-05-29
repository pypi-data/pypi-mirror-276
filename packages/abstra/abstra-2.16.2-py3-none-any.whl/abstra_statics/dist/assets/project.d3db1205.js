var h=Object.defineProperty;var l=(r,t,e)=>t in r?h(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e;var o=(r,t,e)=>(l(r,typeof t!="symbol"?t+"":t,e),e);import{C as n}from"./router.dd631582.js";import{A as y}from"./record.3c5b5204.js";import"./outputWidgets.e5f9ffc6.js";(function(){try{var r=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(r._sentryDebugIds=r._sentryDebugIds||{},r._sentryDebugIds[t]="13e1aaa6-706f-4593-8559-15dbd8610351",r._sentryDebugIdIdentifier="sentry-dbid-13e1aaa6-706f-4593-8559-15dbd8610351")}catch{}})();class g extends Error{constructor(){super("Subdomain already in use")}}class m{constructor(){o(this,"urlPath","projects")}async create({name:t,organizationId:e}){return n.post(`organizations/${e}/${this.urlPath}`,{name:t})}async delete(t){await n.delete(`/${this.urlPath}/${t}`)}async duplicate(t){return await new Promise(e=>setTimeout(e,5e3)),n.post(`/${this.urlPath}/${t}/duplicate`,{})}async list(t){return n.get(`organizations/${t}/${this.urlPath}`)}async get(t){return n.get(`${this.urlPath}/${t}`)}async update(t,e){const a=await n.patch(`${this.urlPath}/${t}`,e);if("error"in a&&a.error==="subdomain-already-in-use")throw new g;if("error"in a)throw new Error("Unknown error");return a}async checkSubdomain(t,e){return n.get(`${this.urlPath}/${t}/check-subdomain/${e}`)}async getStatus(t){return n.get(`${this.urlPath}/${t}/deploy-status`)}async executeQuery(t,e,a){return n.post(`projects/${t}/execute`,{query:e,params:a})}}const s=new m;class i{constructor(t){o(this,"record");this.record=y.create(s,t)}static formatSubdomain(t){const a=t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,""),c=/[a-z0-9]+/g,u=a.matchAll(c);return Array.from(u).map(d=>d[0]).join("-")}static async list(t){return(await s.list(t)).map(a=>new i(a))}static async create(t){const e=await s.create(t);return new i(e)}static async get(t){const e=await s.get(t);return new i(e)}static async getStatus(t){return await s.getStatus(t)}async delete(){await s.delete(this.id)}async duplicate(){const t=await s.duplicate(this.id);return new i(t)}static async executeQuery(t,e,a){return s.executeQuery(t,e,a)}async save(){return this.record.save()}resetChanges(){this.record.resetChanges()}hasChanges(){return this.record.hasChanges()}get id(){return this.record.get("id")}get name(){return this.record.get("name")}set name(t){this.record.set("name",t)}get organizationId(){return this.record.get("organizationId")}get subdomain(){return this.record.get("subdomain")}set subdomain(t){this.record.set("subdomain",t)}async checkSubdomain(){return await s.checkSubdomain(this.id,this.subdomain)}getUrl(t=""){const e=t.startsWith("/")?t.slice(1):t;return`https://${this.subdomain}.abstra.app/${e}`}static async rename(t,e){await s.update(t,{name:e})}}export{i as P};
//# sourceMappingURL=project.d3db1205.js.map
