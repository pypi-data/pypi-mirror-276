var c=Object.defineProperty;var d=(r,t,e)=>t in r?c(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e;var n=(r,t,e)=>(d(r,typeof t!="symbol"?t+"":t,e),e);import{A as g}from"./record.3c5b5204.js";import"./outputWidgets.e5f9ffc6.js";(function(){try{var r=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(r._sentryDebugIds=r._sentryDebugIds||{},r._sentryDebugIds[t]="d9e27eff-8259-4560-88c9-1ad885598909",r._sentryDebugIdIdentifier="sentry-dbid-d9e27eff-8259-4560-88c9-1ad885598909")}catch{}})();class u{async list(){return await(await fetch("/_editor/api/forms")).json()}async create(t,e,s){return await(await fetch("/_editor/api/forms",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title:t,file:e,position:s})})).json()}async get(t){return await(await fetch(`/_editor/api/forms/${t}`)).json()}async update(t,e){return await(await fetch(`/_editor/api/forms/${t}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})).json()}async delete(t,e){const s=e?"?remove_file=true":"",o=`/_editor/api/forms/${t}`+s;await fetch(o,{method:"DELETE",headers:{"Content-Type":"application/json"}})}async duplicate(t){return await(await fetch(`/_editor/api/forms/${t}/duplicate`,{method:"POST"})).json()}}const a=new u;class i{constructor(t){n(this,"record");this.record=g.create(a,t)}static async list(){return(await a.list()).map(e=>new i(e))}static async create(t,e,s){const o=await a.create(t,e,s);return new i(o)}static async get(t){const e=await a.get(t);return new i(e)}get id(){return this.record.get("id")}get type(){return"form"}get allowRestart(){return this.record.get("allow_restart")}set allowRestart(t){this.record.set("allow_restart",t)}get file(){return this.record.get("file")}set file(t){this.record.set("file",t)}get autoStart(){return this.record.get("auto_start")}set autoStart(t){this.record.set("auto_start",t)}get endMessage(){return this.record.get("end_message")}set endMessage(t){this.record.set("end_message",t)}get errorMessage(){return this.record.get("error_message")}set errorMessage(t){this.record.set("error_message",t)}get path(){return this.record.get("path")}set path(t){this.record.set("path",t)}get restartButtonText(){return this.record.get("restart_button_text")}set restartButtonText(t){this.record.set("restart_button_text",t)}get startButtonText(){return this.record.get("start_button_text")}set startButtonText(t){this.record.set("start_button_text",t)}get startMessage(){return this.record.get("start_message")}set startMessage(t){this.record.set("start_message",t)}get timeoutMessage(){return this.record.get("timeout_message")}set timeoutMessage(t){this.record.set("timeout_message",t)}get notificationTrigger(){return new Proxy(this.record.get("notification_trigger"),{set:(t,e,s)=>(this.record.set("notification_trigger",{...t,[e]:s}),!0)})}set notificationTrigger(t){this.record.set("notification_trigger",t)}get(t){return this.record.get(t)}set(t,e){this.record.set(t,e)}get title(){return this.record.get("title")}set title(t){this.record.set("title",t)}get codeContent(){return this.record.get("code_content")}set codeContent(t){this.record.set("code_content",t)}get welcomeTitle(){return this.record.get("welcome_title")}set welcomeTitle(t){this.record.set("welcome_title",t)}async save(t){await this.record.save(t)}onUpdate(t){this.record.pubsub.subscribe("update",t)}hasChanges(t){return this.record.hasChanges(t)}hasChangesDeep(t){return this.record.hasChangesDeep(t)}getInitialState(t){return this.record.getInitialState(t)}updateInitialState(t,e){this.record.updateInitialState(t,e)}async delete(t){await a.delete(this.id,t)}async duplicate(){const t=await a.duplicate(this.id);return new i(t)}makeRunnerData(t){return{...t.makeRunnerData(),id:this.id,isLocal:!0,path:this.path,title:this.title,runtimeType:"form",autoStart:this.autoStart,endMessage:this.endMessage,errorMessage:this.errorMessage,allowRestart:this.allowRestart,welcomeTitle:this.welcomeTitle,startMessage:this.startMessage,timeoutMessage:this.timeoutMessage,startButtonText:this.startButtonText,restartButtonText:this.restartButtonText}}get position(){const[t,e]=this.record.get("workflow_position");return{x:t,y:e,referential:"world"}}get isInitial(){return this.record.get("is_initial")}static from(t){return new i(t)}}export{i as F};
//# sourceMappingURL=forms.04ebf46b.js.map
