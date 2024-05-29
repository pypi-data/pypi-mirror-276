var g=Object.defineProperty;var l=(s,t,e)=>t in s?g(s,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):s[t]=e;var a=(s,t,e)=>(l(s,typeof t!="symbol"?t+"":t,e),e);import{x as h,y as d,B as b}from"./outputWidgets.e5f9ffc6.js";import{P as o}from"./pubsub.75396d00.js";(function(){try{var s=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(s._sentryDebugIds=s._sentryDebugIds||{},s._sentryDebugIds[t]="8d8af1d9-0fd7-47bb-9235-83b97402a980",s._sentryDebugIdIdentifier="sentry-dbid-8d8af1d9-0fd7-47bb-9235-83b97402a980")}catch{}})();class n{constructor(t){a(this,"initialState");a(this,"pubsub");a(this,"_changes");this.initialState=t,this.pubsub=new o,this._changes=d({})}static from(t){return h(new n(t))}get changes(){return this._changes.value}get(t){var e;return(e=this.changes[t])!=null?e:this.initialState[t]}set(t,e){this._changes.value={...this.changes,[t]:e}}hasChanges(t){return t?t in this.changes:Object.keys(this.changes).length>0}hasChangesDeep(t){return t in this.changes&&!b.exports.isEqual(this.initialState[t],this.changes[t])}get state(){return{...this.initialState,...this.changes}}resetChanges(){const t={...this.changes};this._changes.value={},this.pubsub.publish("update",t)}onUpdate(t){this.pubsub.subscribe("update",t)}commit(){this.initialState=this.state,this._changes.value={}}toDTO(){return{...this.state,...this._changes.value}}update(t){this._changes.value={...this.changes,...t}}}class u extends n{constructor(e,i){super(i);a(this,"api");this.api=e}static create(e,i){return h(new u(e,i))}getInitialState(e){return this.initialState[e]}updateInitialState(e,i){this.initialState[e]=i,delete this._changes.value[e]}async save(e){if(Object.keys(this.changes).length===0||e&&!(e in this.changes))return;if(e){const r={[e]:this.changes[e]},c=await this.api.update(this.initialState.id,r);this.initialState={...this.initialState,...c},delete this._changes.value[e];return}this.initialState=await this.api.update(this.initialState.id,this.changes);const i={...this.changes};this._changes.value={},this.pubsub.publish("update",i)}}export{u as A,n as E};
//# sourceMappingURL=record.3c5b5204.js.map
