






html = '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <title>SUNY at Geneseo Employment Opportunities | Search Jobs</title>
      <!-- Original Portal -->
      <meta http-equiv="content-type" content="text/html; charset=utf-8" />
<script type="text/javascript">window.NREUM||(NREUM={});NREUM.info={"beacon":"bam.nr-data.net","errorBeacon":"bam.nr-data.net","licenseKey":"9de8d44d4a","applicationID":"958191","transactionName":"IAxfREQOCl4DQkpBDRAXWF5REklBA1EXUgo=","queueTime":0,"applicationTime":496,"agent":""}</script>
<script type="text/javascript">(window.NREUM||(NREUM={})).loader_config={xpid:"XQQDUkVaDQsBXVA="};window.NREUM||(NREUM={}),__nr_require=function(t,n,e){function r(e){if(!n[e]){var o=n[e]={exports:{}};t[e][0].call(o.exports,function(n){var o=t[e][1][n];return r(o||n)},o,o.exports)}return n[e].exports}if("function"==typeof __nr_require)return __nr_require;for(var o=0;o<e.length;o++)r(e[o]);return r}({1:[function(t,n,e){function r(t){try{s.console&&console.log(t)}catch(n){}}var o,i=t("ee"),a=t(18),s={};try{o=localStorage.getItem("__nr_flags").split(","),console&&"function"==typeof console.log&&(s.console=!0,o.indexOf("dev")!==-1&&(s.dev=!0),o.indexOf("nr_dev")!==-1&&(s.nrDev=!0))}catch(c){}s.nrDev&&i.on("internal-error",function(t){r(t.stack)}),s.dev&&i.on("fn-err",function(t,n,e){r(e.stack)}),s.dev&&(r("NR AGENT IN DEVELOPMENT MODE"),r("flags: "+a(s,function(t,n){return t}).join(", ")))},{}],2:[function(t,n,e){function r(t,n,e,r,s){try{p?p-=1:o(s||new UncaughtException(t,n,e),!0)}catch(f){try{i("ierr",[f,c.now(),!0])}catch(d){}}return"function"==typeof u&&u.apply(this,a(arguments))}function UncaughtException(t,n,e){this.message=t||"Uncaught error with no additional information",this.sourceURL=n,this.line=e}function o(t,n){var e=n?null:c.now();i("err",[t,e])}var i=t("handle"),a=t(19),s=t("ee"),c=t("loader"),f=t("gos"),u=window.onerror,d=!1,l="nr@seenError",p=0;c.features.err=!0,t(1),window.onerror=r;try{throw new Error}catch(h){"stack"in h&&(t(8),t(7),"addEventListener"in window&&t(5),c.xhrWrappable&&t(9),d=!0)}s.on("fn-start",function(t,n,e){d&&(p+=1)}),s.on("fn-err",function(t,n,e){d&&!e[l]&&(f(e,l,function(){return!0}),this.thrown=!0,o(e))}),s.on("fn-end",function(){d&&!this.thrown&&p>0&&(p-=1)}),s.on("internal-error",function(t){i("ierr",[t,c.now(),!0])})},{}],3:[function(t,n,e){t("loader").features.ins=!0},{}],4:[function(t,n,e){function r(t){}if(window.performance&&window.performance.timing&&window.performance.getEntriesByType){var o=t("ee"),i=t("handle"),a=t(8),s=t(7),c="learResourceTimings",f="addEventListener",u="resourcetimingbufferfull",d="bstResource",l="resource",p="-start",h="-end",m="fn"+p,w="fn"+h,v="bstTimer",y="pushState",g=t("loader");g.features.stn=!0,t(6);var x=NREUM.o.EV;o.on(m,function(t,n){var e=t[0];e instanceof x&&(this.bstStart=g.now())}),o.on(w,function(t,n){var e=t[0];e instanceof x&&i("bst",[e,n,this.bstStart,g.now()])}),a.on(m,function(t,n,e){this.bstStart=g.now(),this.bstType=e}),a.on(w,function(t,n){i(v,[n,this.bstStart,g.now(),this.bstType])}),s.on(m,function(){this.bstStart=g.now()}),s.on(w,function(t,n){i(v,[n,this.bstStart,g.now(),"requestAnimationFrame"])}),o.on(y+p,function(t){this.time=g.now(),this.startPath=location.pathname+location.hash}),o.on(y+h,function(t){i("bstHist",[location.pathname+location.hash,this.startPath,this.time])}),f in window.performance&&(window.performance["c"+c]?window.performance[f](u,function(t){i(d,[window.performance.getEntriesByType(l)]),window.performance["c"+c]()},!1):window.performance[f]("webkit"+u,function(t){i(d,[window.performance.getEntriesByType(l)]),window.performance["webkitC"+c]()},!1)),document[f]("scroll",r,{passive:!0}),document[f]("keypress",r,!1),document[f]("click",r,!1)}},{}],5:[function(t,n,e){function r(t){for(var n=t;n&&!n.hasOwnProperty(u);)n=Object.getPrototypeOf(n);n&&o(n)}function o(t){s.inPlace(t,[u,d],"-",i)}function i(t,n){return t[1]}var a=t("ee").get("events"),s=t(21)(a,!0),c=t("gos"),f=XMLHttpRequest,u="addEventListener",d="removeEventListener";n.exports=a,"getPrototypeOf"in Object?(r(document),r(window),r(f.prototype)):f.prototype.hasOwnProperty(u)&&(o(window),o(f.prototype)),a.on(u+"-start",function(t,n){var e=t[1],r=c(e,"nr@wrapped",function(){function t(){if("function"==typeof e.handleEvent)return e.handleEvent.apply(e,arguments)}var n={object:t,"function":e}[typeof e];return n?s(n,"fn-",null,n.name||"anonymous"):e});this.wrapped=t[1]=r}),a.on(d+"-start",function(t){t[1]=this.wrapped||t[1]})},{}],6:[function(t,n,e){var r=t("ee").get("history"),o=t(21)(r);n.exports=r;var i=window.history&&window.history.constructor&&window.history.constructor.prototype,a=window.history;i&&i.pushState&&i.replaceState&&(a=i),o.inPlace(a,["pushState","replaceState"],"-")},{}],7:[function(t,n,e){var r=t("ee").get("raf"),o=t(21)(r),i="equestAnimationFrame";n.exports=r,o.inPlace(window,["r"+i,"mozR"+i,"webkitR"+i,"msR"+i],"raf-"),r.on("raf-start",function(t){t[0]=o(t[0],"fn-")})},{}],8:[function(t,n,e){function r(t,n,e){t[0]=a(t[0],"fn-",null,e)}function o(t,n,e){this.method=e,this.timerDuration=isNaN(t[1])?0:+t[1],t[0]=a(t[0],"fn-",this,e)}var i=t("ee").get("timer"),a=t(21)(i),s="setTimeout",c="setInterval",f="clearTimeout",u="-start",d="-";n.exports=i,a.inPlace(window,[s,"setImmediate"],s+d),a.inPlace(window,[c],c+d),a.inPlace(window,[f,"clearImmediate"],f+d),i.on(c+u,r),i.on(s+u,o)},{}],9:[function(t,n,e){function r(t,n){d.inPlace(n,["onreadystatechange"],"fn-",s)}function o(){var t=this,n=u.context(t);t.readyState>3&&!n.resolved&&(n.resolved=!0,u.emit("xhr-resolved",[],t)),d.inPlace(t,y,"fn-",s)}function i(t){g.push(t),h&&(b?b.then(a):w?w(a):(E=-E,R.data=E))}function a(){for(var t=0;t<g.length;t++)r([],g[t]);g.length&&(g=[])}function s(t,n){return n}function c(t,n){for(var e in t)n[e]=t[e];return n}t(5);var f=t("ee"),u=f.get("xhr"),d=t(21)(u),l=NREUM.o,p=l.XHR,h=l.MO,m=l.PR,w=l.SI,v="readystatechange",y=["onload","onerror","onabort","onloadstart","onloadend","onprogress","ontimeout"],g=[];n.exports=u;var x=window.XMLHttpRequest=function(t){var n=new p(t);try{u.emit("new-xhr",[n],n),n.addEventListener(v,o,!1)}catch(e){try{u.emit("internal-error",[e])}catch(r){}}return n};if(c(p,x),x.prototype=p.prototype,d.inPlace(x.prototype,["open","send"],"-xhr-",s),u.on("send-xhr-start",function(t,n){r(t,n),i(n)}),u.on("open-xhr-start",r),h){var b=m&&m.resolve();if(!w&&!m){var E=1,R=document.createTextNode(E);new h(a).observe(R,{characterData:!0})}}else f.on("fn-end",function(t){t[0]&&t[0].type===v||a()})},{}],10:[function(t,n,e){function r(){var t=window.NREUM,n=t.info.accountID||null,e=t.info.agentID||null,r=t.info.trustKey||null,i="btoa"in window&&"function"==typeof window.btoa;if(!n||!e||!i)return null;var a={v:[0,1],d:{ty:"Browser",ac:n,ap:e,id:o.generateCatId(),tr:o.generateCatId(),ti:Date.now()}};return r&&n!==r&&(a.d.tk=r),btoa(JSON.stringify(a))}var o=t(16);n.exports={generateTraceHeader:r}},{}],11:[function(t,n,e){function r(t){var n=this.params,e=this.metrics;if(!this.ended){this.ended=!0;for(var r=0;r<p;r++)t.removeEventListener(l[r],this.listener,!1);n.aborted||(e.duration=s.now()-this.startTime,this.loadCaptureCalled||4!==t.readyState?null==n.status&&(n.status=0):a(this,t),e.cbTime=this.cbTime,d.emit("xhr-done",[t],t),c("xhr",[n,e,this.startTime]))}}function o(t,n){var e=t.responseType;if("json"===e&&null!==n)return n;var r="arraybuffer"===e||"blob"===e||"json"===e?t.response:t.responseText;return w(r)}function i(t,n){var e=f(n),r=t.params;r.host=e.hostname+":"+e.port,r.pathname=e.pathname,t.sameOrigin=e.sameOrigin}function a(t,n){t.params.status=n.status;var e=o(n,t.lastSize);if(e&&(t.metrics.rxSize=e),t.sameOrigin){var r=n.getResponseHeader("X-NewRelic-App-Data");r&&(t.params.cat=r.split(", ").pop())}t.loadCaptureCalled=!0}var s=t("loader");if(s.xhrWrappable){var c=t("handle"),f=t(12),u=t(10).generateTraceHeader,d=t("ee"),l=["load","error","abort","timeout"],p=l.length,h=t("id"),m=t(15),w=t(14),v=window.XMLHttpRequest;s.features.xhr=!0,t(9),d.on("new-xhr",function(t){var n=this;n.totalCbs=0,n.called=0,n.cbTime=0,n.end=r,n.ended=!1,n.xhrGuids={},n.lastSize=null,n.loadCaptureCalled=!1,t.addEventListener("load",function(e){a(n,t)},!1),m&&(m>34||m<10)||window.opera||t.addEventListener("progress",function(t){n.lastSize=t.loaded},!1)}),d.on("open-xhr-start",function(t){this.params={method:t[0]},i(this,t[1]),this.metrics={}}),d.on("open-xhr-end",function(t,n){"loader_config"in NREUM&&"xpid"in NREUM.loader_config&&this.sameOrigin&&n.setRequestHeader("X-NewRelic-ID",NREUM.loader_config.xpid);var e=!1;if("init"in NREUM&&"distributed_tracing"in NREUM.init&&(e=!!NREUM.init.distributed_tracing.enabled),e&&this.sameOrigin){var r=u();r&&n.setRequestHeader("newrelic",r)}}),d.on("send-xhr-start",function(t,n){var e=this.metrics,r=t[0],o=this;if(e&&r){var i=w(r);i&&(e.txSize=i)}this.startTime=s.now(),this.listener=function(t){try{"abort"!==t.type||o.loadCaptureCalled||(o.params.aborted=!0),("load"!==t.type||o.called===o.totalCbs&&(o.onloadCalled||"function"!=typeof n.onload))&&o.end(n)}catch(e){try{d.emit("internal-error",[e])}catch(r){}}};for(var a=0;a<p;a++)n.addEventListener(l[a],this.listener,!1)}),d.on("xhr-cb-time",function(t,n,e){this.cbTime+=t,n?this.onloadCalled=!0:this.called+=1,this.called!==this.totalCbs||!this.onloadCalled&&"function"==typeof e.onload||this.end(e)}),d.on("xhr-load-added",function(t,n){var e=""+h(t)+!!n;this.xhrGuids&&!this.xhrGuids[e]&&(this.xhrGuids[e]=!0,this.totalCbs+=1)}),d.on("xhr-load-removed",function(t,n){var e=""+h(t)+!!n;this.xhrGuids&&this.xhrGuids[e]&&(delete this.xhrGuids[e],this.totalCbs-=1)}),d.on("addEventListener-end",function(t,n){n instanceof v&&"load"===t[0]&&d.emit("xhr-load-added",[t[1],t[2]],n)}),d.on("removeEventListener-end",function(t,n){n instanceof v&&"load"===t[0]&&d.emit("xhr-load-removed",[t[1],t[2]],n)}),d.on("fn-start",function(t,n,e){n instanceof v&&("onload"===e&&(this.onload=!0),("load"===(t[0]&&t[0].type)||this.onload)&&(this.xhrCbStart=s.now()))}),d.on("fn-end",function(t,n){this.xhrCbStart&&d.emit("xhr-cb-time",[s.now()-this.xhrCbStart,this.onload,n],n)})}},{}],12:[function(t,n,e){n.exports=function(t){var n=document.createElement("a"),e=window.location,r={};n.href=t,r.port=n.port;var o=n.href.split("://");!r.port&&o[1]&&(r.port=o[1].split("/")[0].split("@").pop().split(":")[1]),r.port&&"0"!==r.port||(r.port="https"===o[0]?"443":"80"),r.hostname=n.hostname||e.hostname,r.pathname=n.pathname,r.protocol=o[0],"/"!==r.pathname.charAt(0)&&(r.pathname="/"+r.pathname);var i=!n.protocol||":"===n.protocol||n.protocol===e.protocol,a=n.hostname===document.domain&&n.port===e.port;return r.sameOrigin=i&&(!n.hostname||a),r}},{}],13:[function(t,n,e){function r(){}function o(t,n,e){return function(){return i(t,[f.now()].concat(s(arguments)),n?null:this,e),n?void 0:this}}var i=t("handle"),a=t(18),s=t(19),c=t("ee").get("tracer"),f=t("loader"),u=NREUM;"undefined"==typeof window.newrelic&&(newrelic=u);var d=["setPageViewName","setCustomAttribute","setErrorHandler","finished","addToTrace","inlineHit","addRelease"],l="api-",p=l+"ixn-";a(d,function(t,n){u[n]=o(l+n,!0,"api")}),u.addPageAction=o(l+"addPageAction",!0),u.setCurrentRouteName=o(l+"routeName",!0),n.exports=newrelic,u.interaction=function(){return(new r).get()};var h=r.prototype={createTracer:function(t,n){var e={},r=this,o="function"==typeof n;return i(p+"tracer",[f.now(),t,e],r),function(){if(c.emit((o?"":"no-")+"fn-start",[f.now(),r,o],e),o)try{return n.apply(this,arguments)}catch(t){throw c.emit("fn-err",[arguments,this,t],e),t}finally{c.emit("fn-end",[f.now()],e)}}}};a("actionText,setName,setAttribute,save,ignore,onEnd,getContext,end,get".split(","),function(t,n){h[n]=o(p+n)}),newrelic.noticeError=function(t,n){"string"==typeof t&&(t=new Error(t)),i("err",[t,f.now(),!1,n])}},{}],14:[function(t,n,e){n.exports=function(t){if("string"==typeof t&&t.length)return t.length;if("object"==typeof t){if("undefined"!=typeof ArrayBuffer&&t instanceof ArrayBuffer&&t.byteLength)return t.byteLength;if("undefined"!=typeof Blob&&t instanceof Blob&&t.size)return t.size;if(!("undefined"!=typeof FormData&&t instanceof FormData))try{return JSON.stringify(t).length}catch(n){return}}}},{}],15:[function(t,n,e){var r=0,o=navigator.userAgent.match(/Firefox[\/\s](\d+\.\d+)/);o&&(r=+o[1]),n.exports=r},{}],16:[function(t,n,e){function r(){function t(){return n?15&n[e++]:16*Math.random()|0}var n=null,e=0,r=window.crypto||window.msCrypto;r&&r.getRandomValues&&(n=r.getRandomValues(new Uint8Array(31)));for(var o,i="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",a="",s=0;s<i.length;s++)o=i[s],"x"===o?a+=t().toString(16):"y"===o?(o=3&t()|8,a+=o.toString(16)):a+=o;return a}function o(){function t(){return n?15&n[e++]:16*Math.random()|0}var n=null,e=0,r=window.crypto||window.msCrypto;r&&r.getRandomValues&&Uint8Array&&(n=r.getRandomValues(new Uint8Array(31)));for(var o=[],i=0;i<16;i++)o.push(t().toString(16));return o.join("")}n.exports={generateUuid:r,generateCatId:o}},{}],17:[function(t,n,e){function r(t,n){if(!o)return!1;if(t!==o)return!1;if(!n)return!0;if(!i)return!1;for(var e=i.split("."),r=n.split("."),a=0;a<r.length;a++)if(r[a]!==e[a])return!1;return!0}var o=null,i=null,a=/Version\/(\S+)\s+Safari/;if(navigator.userAgent){var s=navigator.userAgent,c=s.match(a);c&&s.indexOf("Chrome")===-1&&s.indexOf("Chromium")===-1&&(o="Safari",i=c[1])}n.exports={agent:o,version:i,match:r}},{}],18:[function(t,n,e){function r(t,n){var e=[],r="",i=0;for(r in t)o.call(t,r)&&(e[i]=n(r,t[r]),i+=1);return e}var o=Object.prototype.hasOwnProperty;n.exports=r},{}],19:[function(t,n,e){function r(t,n,e){n||(n=0),"undefined"==typeof e&&(e=t?t.length:0);for(var r=-1,o=e-n||0,i=Array(o<0?0:o);++r<o;)i[r]=t[n+r];return i}n.exports=r},{}],20:[function(t,n,e){n.exports={exists:"undefined"!=typeof window.performance&&window.performance.timing&&"undefined"!=typeof window.performance.timing.navigationStart}},{}],21:[function(t,n,e){function r(t){return!(t&&t instanceof Function&&t.apply&&!t[a])}var o=t("ee"),i=t(19),a="nr@original",s=Object.prototype.hasOwnProperty,c=!1;n.exports=function(t,n){function e(t,n,e,o){function nrWrapper(){var r,a,s,c;try{a=this,r=i(arguments),s="function"==typeof e?e(r,a):e||{}}catch(f){l([f,"",[r,a,o],s])}u(n+"start",[r,a,o],s);try{return c=t.apply(a,r)}catch(d){throw u(n+"err",[r,a,d],s),d}finally{u(n+"end",[r,a,c],s)}}return r(t)?t:(n||(n=""),nrWrapper[a]=t,d(t,nrWrapper),nrWrapper)}function f(t,n,o,i){o||(o="");var a,s,c,f="-"===o.charAt(0);for(c=0;c<n.length;c++)s=n[c],a=t[s],r(a)||(t[s]=e(a,f?s+o:o,i,s))}function u(e,r,o){if(!c||n){var i=c;c=!0;try{t.emit(e,r,o,n)}catch(a){l([a,e,r,o])}c=i}}function d(t,n){if(Object.defineProperty&&Object.keys)try{var e=Object.keys(t);return e.forEach(function(e){Object.defineProperty(n,e,{get:function(){return t[e]},set:function(n){return t[e]=n,n}})}),n}catch(r){l([r])}for(var o in t)s.call(t,o)&&(n[o]=t[o]);return n}function l(n){try{t.emit("internal-error",n)}catch(e){}}return t||(t=o),e.inPlace=f,e.flag=a,e}},{}],ee:[function(t,n,e){function r(){}function o(t){function n(t){return t&&t instanceof r?t:t?c(t,s,i):i()}function e(e,r,o,i){if(!l.aborted||i){t&&t(e,r,o);for(var a=n(o),s=m(e),c=s.length,f=0;f<c;f++)s[f].apply(a,r);var d=u[g[e]];return d&&d.push([x,e,r,a]),a}}function p(t,n){y[t]=m(t).concat(n)}function h(t,n){var e=y[t];if(e)for(var r=0;r<e.length;r++)e[r]===n&&e.splice(r,1)}function m(t){return y[t]||[]}function w(t){return d[t]=d[t]||o(e)}function v(t,n){f(t,function(t,e){n=n||"feature",g[e]=n,n in u||(u[n]=[])})}var y={},g={},x={on:p,addEventListener:p,removeEventListener:h,emit:e,get:w,listeners:m,context:n,buffer:v,abort:a,aborted:!1};return x}function i(){return new r}function a(){(u.api||u.feature)&&(l.aborted=!0,u=l.backlog={})}var s="nr@context",c=t("gos"),f=t(18),u={},d={},l=n.exports=o();l.backlog=u},{}],gos:[function(t,n,e){function r(t,n,e){if(o.call(t,n))return t[n];var r=e();if(Object.defineProperty&&Object.keys)try{return Object.defineProperty(t,n,{value:r,writable:!0,enumerable:!1}),r}catch(i){}return t[n]=r,r}var o=Object.prototype.hasOwnProperty;n.exports=r},{}],handle:[function(t,n,e){function r(t,n,e,r){o.buffer([t],r),o.emit(t,n,e)}var o=t("ee").get("handle");n.exports=r,r.ee=o},{}],id:[function(t,n,e){function r(t){var n=typeof t;return!t||"object"!==n&&"function"!==n?-1:t===window?0:a(t,i,function(){return o++})}var o=1,i="nr@id",a=t("gos");n.exports=r},{}],loader:[function(t,n,e){function r(){if(!E++){var t=b.info=NREUM.info,n=p.getElementsByTagName("script")[0];if(setTimeout(u.abort,3e4),!(t&&t.licenseKey&&t.applicationID&&n))return u.abort();f(g,function(n,e){t[n]||(t[n]=e)}),c("mark",["onload",a()+b.offset],null,"api");var e=p.createElement("script");e.src="https://"+t.agent,n.parentNode.insertBefore(e,n)}}function o(){"complete"===p.readyState&&i()}function i(){c("mark",["domContent",a()+b.offset],null,"api")}function a(){return R.exists&&performance.now?Math.round(performance.now()):(s=Math.max((new Date).getTime(),s))-b.offset}var s=(new Date).getTime(),c=t("handle"),f=t(18),u=t("ee"),d=t(17),l=window,p=l.document,h="addEventListener",m="attachEvent",w=l.XMLHttpRequest,v=w&&w.prototype;NREUM.o={ST:setTimeout,SI:l.setImmediate,CT:clearTimeout,XHR:w,REQ:l.Request,EV:l.Event,PR:l.Promise,MO:l.MutationObserver};var y=""+location,g={beacon:"bam.nr-data.net",errorBeacon:"bam.nr-data.net",agent:"js-agent.newrelic.com/nr-1130.min.js"},x=w&&v&&v[h]&&!/CriOS/.test(navigator.userAgent),b=n.exports={offset:s,now:a,origin:y,features:{},xhrWrappable:x,userAgent:d};t(13),p[h]?(p[h]("DOMContentLoaded",i,!1),l[h]("load",r,!1)):(p[m]("onreadystatechange",o),l[m]("onload",r)),c("mark",["firstbyte",s],null,"api");var E=0,R=t(20)},{}]},{},["loader",2,11,4,3]);</script>
<meta content="width=device-width, initial-scale=1" name="viewport">

<link href="/stylesheets/cached/all.css?1561655372" media="screen" rel="stylesheet" type="text/css" />
<link href="/stylesheets/bootstrap.css?1561655372" media="screen" rel="stylesheet" type="text/css" />
<link href="/stylesheets/application-responsive.css?1561655372" media="screen" rel="stylesheet" type="text/css" />
<link href="//cdnjs.cloudflare.com/ajax/libs/font-awesome/3.2.1/css/font-awesome.min.css" media="screen" rel="stylesheet" type="text/css" />
<link href="//fonts.googleapis.com/css?family=Lobster+Two&amp;text=%26" media="screen" rel="stylesheet" type="text/css" />
<link href="//fonts.googleapis.com/css?family=Open+Sans:400,600,700,300" media="screen" rel="stylesheet" type="text/css" />
<link href="https://pa-hrsuite-production.s3.amazonaws.com/2345-responsive.css" media="screen" rel="stylesheet" type="text/css" />
<meta content="authenticity_token" name="csrf-param" />
<meta content="LZkrxrkFwk2IEGCb7eUxFCbWrUA7xRMFuZx2SRrBTPg=" name="csrf-token" />

  <link href="https://pa-hrsuite-production.s3.amazonaws.com/2345/docs/38616.css" media="screen" rel="stylesheet" type="text/css" />

      <link href="http://jobs.geneseo.edu/postings/all_jobs" rel="alternate" title="All Jobs Atom Feed" type="application/atom+xml" />
  </head>
  <body id="postings_search">
      <!-- Original Portal -->
      <div id="wrapperDiv" class="container">
        <div id="skipToMainContent">
          <a href="#content_inner" class="sr-only sr-only-focusable">Skip to Main Content</a>
        </div>
        <div id="mainBodyDiv">
          <div id="header">
            <div class='wrapper'>
  <div class='header-inner container'>
    <div class='row'>
      <div class='col-xs-12 col-sm-6 col-md-3'>
        <a class='text-hide' href='/' title='Home'>
          <img alt='alternate_text_here' src=https://pa-hrsuite-production.s3.amazonaws.com/2345/docs/62303.jpg class=img-responsive>
        </a>
      </div>
      <div class='col-md-9 visible-md visible-lg'>
        <!--header rightside-->
        <h1 class='header-text'>Employment Opportunities</h1>
      </div>
    </div>
  </div>
</div>

          </div>
          <div id="contentWrapper">
            <div id="nav" class="navBG">
  <div class="navbar navbar-default" role="navigation">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
    </div>
    <div class="collapse navbar-collapse navbar-ex1-collapse">
      <ul id="navLinks" class="nav navbar-nav">
  <li class="list-group-item"><a href="/">Home</a></li>
  <li class="list-group-item"><a href="/postings/search">Search Jobs</a></li>
      <li class="list-group-item"><a href="/interest_cards">Job Alerts</a></li>
    <li class="list-group-item"><a href="/user/new">Create Account</a></li>
    <li class="list-group-item"><a href="/login">Log In</a></li>
  <li class="list-group-item"><a href="https://help.powerschool.com/t5/PeopleAdmin-Applicant-Support/tkb-p/PeopleAdmin-Applicant-Support-Knowledge" class="help" target="_blank">Help</a></li>
</ul>

      <ul id="customnav">
      </ul>
    </div>
  </div>
</div>

            <div id="content" class="mainContent">
              <div id="content_inner">



<h2 class='pad-left'>
  Search  Postings <span class='smaller muted'>(54)</span>
    <a href="/postings/all_jobs.atom" target="_blank"><img alt="All Jobs Atom Feed" src="/images/feed.png?1561655372" title="All Jobs Atom Feed" /></a>
</h2>
<p>View all open Postings below, or enter search criteria to narrow your search.</p>
<form accept-charset="UTF-8" action="/postings/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
  <div class='search-main'>
  <div class="container-fluid">
    <div class="row">
      <div class="col-lg-2 col-md-2 col-xs-12">
        <label for="query">Keywords</label>
      </div>
      <div class="col-lg-4 col-md-2 col-xs-12">
        <input id="query" name="query" type="text" />
      </div>
        <div class="col-lg-2 col-md-2 col-xs-12">
          <label for="query_v0_posted_at_date">Posted Within</label>
        </div>
        <div class="col-lg-4 col-md-6 col-xs-12">
          <select id="query_v0_posted_at_date" name="query_v0_posted_at_date"><option value="">Any time period</option>
<option value="day">Last Day</option>
<option value="week">Last Week</option>
<option value="month">Last Month</option></select>
        </div>
    </div>
    <div class='form-row-clear'>
    </div>
  </div>
</div>

  <div class='search-extra'>
  <div class="container-fluid">
      <div class="row">
          <div class="col-lg-2 col-md-3 col-xs-12">
            <label for="435">Job Title</label>
          </div>
          <div class="col-lg-4 col-md-3 col-xs-12">
            <div class='select-wrapper'>
              <input id="435" name="435" type="text" />
            </div>
          </div>
          <div class="col-lg-2 col-md-3 col-xs-12">
            <label for="query_organizational_tier_3_id">Department</label>
          </div>
          <div class="col-lg-4 col-md-3 col-xs-12">
            <div class='select-wrapper'>
              <select class="form-control" id="query_organizational_tier_3_id" multiple="multiple" name="query_organizational_tier_3_id[]"><option value="any">No Selection</option>
<option value="82">Academic Affairs Administra...</option>
<option value="15">Access Opportunity Programs</option>
<option value="16">Accounting Services</option>
<option value="18">Administrative Systems Serv...</option>
<option value="19">Admissions</option>
<option value="20">Affirmative Action</option>
<option value="21">Anthropology</option>
<option value="22">Art History</option>
<option value="23">Art Studio</option>
<option value="24">Biology</option>
<option value="25">Budget Office</option>
<option value="26">Career Development</option>
<option value="27">Center for Community</option>
<option value="28">Center for Integrative Lear...</option>
<option value="29">Central Duplicating Services</option>
<option value="30">Chemistry</option>
<option value="31">College Advancement</option>
<option value="32">Communication</option>
<option value="79">Communications &amp; Marketing</option>
<option value="33">Communicative Disorders &amp; S...</option>
<option value="34">Computer Science</option>
<option value="35">Computing &amp; Information Tec...</option>
<option value="36">English</option>
<option value="37">Enrollment Management</option>
<option value="38">Facilities Services</option>
<option value="17">Finance &amp; Administration</option>
<option value="39">Financial Aid</option>
<option value="40">Geography</option>
<option value="41">Geological Sciences</option>
<option value="42">Grants Management</option>
<option value="44">History</option>
<option value="45">Human Resources &amp; Payroll S...</option>
<option value="46">Institutional Research</option>
<option value="47">Intercollegiate Athletics &amp;...</option>
<option value="48">Intl Student &amp; Scholar Serv...</option>
<option value="49">Languages &amp; Literatures</option>
<option value="50">Mail Services</option>
<option value="51">Mathematics</option>
<option value="52">Milne Library</option>
<option value="53">Music</option>
<option value="54">Office of Disability Services</option>
<option value="80">Office of Diversity and Equity</option>
<option value="55">Office of International Pro...</option>
<option value="56">Office of Sustainability Se...</option>
<option value="57">Office of the Dean of the C...</option>
<option value="58">Office of the President</option>
<option value="59">Office of the Provost</option>
<option value="60">Office of the Registrar</option>
<option value="61">Philosophy</option>
<option value="62">Physics &amp; Astronomy</option>
<option value="63">Pol Science &amp; Intern Relations</option>
<option value="64">Procurement &amp; Property Cont...</option>
<option value="65">Psychology </option>
<option value="66">Residence Life</option>
<option value="67">Scheduling, Events  &amp; Confe...</option>
<option value="68">School of Business</option>
<option value="69">School of Education</option>
<option value="70">Small Business Development ...</option>
<option value="71">Sociology</option>
<option value="72">Sponsored Research</option>
<option value="73">Student &amp; Campus Life</option>
<option value="74">Student Accounts</option>
<option value="75">Student Association</option>
<option value="43">Student Health &amp; Counseling</option>
<option value="83">Student Health and Counseli...</option>
<option value="76">Student Life</option>
<option value="77">Theatre &amp; Dance</option>
<option value="78">University Police</option></select>
            </div>
          </div>
      </div>
      <div class="row">
          <div class="col-lg-2 col-md-3 col-xs-12">
            <label for="query_organizational_tier_2_id">Division</label>
          </div>
          <div class="col-lg-4 col-md-3 col-xs-12">
            <div class='select-wrapper'>
              <select class="form-control" id="query_organizational_tier_2_id" multiple="multiple" name="query_organizational_tier_2_id[]"><option value="any">No Selection</option>
<option value="9">Academic Affairs</option>
<option value="81">Academic Affairs Administra...</option>
<option value="11">College Advancement DIV</option>
<option value="87">Communications &amp; Marketing DIV</option>
<option value="12">Enrollment Management DIV</option>
<option value="10">Finance &amp; Administration</option>
<option value="84">Office of Diversity and Equ...</option>
<option value="13">Office of the President DIV</option>
<option value="14">Student &amp; Campus Life</option></select>
            </div>
          </div>
          <div class="col-lg-2 col-md-3 col-xs-12">
            <label for="query_position_type_id">Position Type</label>
          </div>
          <div class="col-lg-4 col-md-3 col-xs-12">
            <div class='select-wrapper'>
              <select class="form-control" id="query_position_type_id" multiple="multiple" name="query_position_type_id[]"><option value="any">No Selection</option>
<option value="1">Staff</option>
<option value="2">Faculty</option>
<option value="3">Classified </option></select>
            </div>
          </div>
      </div>
  </div>
</div>

  <input class="btn btn-default job-search primary_button_color" name="commit" title="click to search" type="submit" value="Search" />
</form><div class='section-separator'></div>
<div class="pagination"><span class="previous_page disabled"><span class="translation_missing" title="translation missing: en.previous">Previous</span></span> <em class="current">1</em> <a rel="next" href="/postings/search?page=2">2</a> <a class="next_page" rel="next" href="/postings/search?page=2"><span class="translation_missing" title="translation missing: en.next">Next</span></a></div>
<h2 class='no-pad-bottom pad-left'>View Results <span class='smaller muted'>(54)</span></h2>
<div class="row"></div>
<div id='job_list_header_responsive' class="row hidden-xs hidden-sm">
  <div class='job-title col-md-4'>
      &nbsp;
  </div>
  <div class='col-md-8'>
    <div class='col-md-2'></div>
      <div class='col-md-2 col-md-push-0'>
        <a href="/postings/search?sort=225+asc">Posting Number</a>
      </div>
      <div class='col-md-2 col-md-push-0'>
        <a href="/postings/search?sort=226+asc">Department</a>
      </div>
      <div class='col-md-2 col-md-push-0'>
        <a href="/postings/search?sort=434+asc">Postion Type</a>
      </div>
      <div class='col-md-2 col-md-push-0'>
        <a href="/postings/search?sort=622+asc">Job Open Date</a>
      </div>
      <div class='col-md-2 col-md-push-0'>
        <a href="/postings/search?sort=227+asc">Job Close Date</a>
      </div>
  </div>
</div>


<div id="search_results">
      <div class='job-item job-item-posting' data-posting-title="Title IX Graduate Assistant">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2811">Title IX Graduate Assistant</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S163
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Office of Diversity and Equity
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              07/03/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Geneseo’s Title IX Office is committed to providing options, support and assistance to victims/survivors of sexual assault, domestic violence, dating violence, and/or stalking to ensure that they can continue to participate in SUNY Geneseo-wide and campus programs, activities, and employment.  All victims/survivors of these crimes and violations, regardless of race, color, national origin, reli&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2811" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2811" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Maintenance Assistant, SG-09">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2808">Maintenance Assistant, SG-09</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              C222
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Facilities Services
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Classified
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              07/24/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              08/08/2019
          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                HIGHLIGHTS
The SUNY Geneseo Facilities Department is looking for a reliable and dedicated individual to join their team as a Maintenance Assistant. Find out more about our Facilities department!
This position is responsible for tasks in the mechanical, building construction, m&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2808" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2808" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Vice President for College Advancement">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2805">Vice President for College Advancement</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S167
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              College Advancement
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              07/18/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The Vice President for College Advancement reports to the President and is a member of the cabinet, contributing expertise to campus-wide initiatives.
The Vice President for College Advancement position presents an exciting opportunity to provide leadership and capitalize on Geneseo’s tremendous potential in the Advancement area.
The next Vice President will be able to lead the strategy &#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2805" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2805" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Area Coordinator">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2798">Area Coordinator</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S157
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Residence Life
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/07/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The SUNY Geneseo Department of Residence Life, in partnership with our residents, promotes an inclusive living and learning environment that encourages well being and engagement for all students who live on campus.
Residence Life administers selected co-curricular educational and assessment initiatives within the residential experience. Opportunities for student engagement and learning withi&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2798" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2798" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Part-Time Assistant Coach - Men&#x27;s &amp; Women&#x27;s Swimming and Diving">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2797">Part-Time Assistant Coach - Men&#x27;s &amp; Women&#x27;s Swimming and Diving</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S153
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Intercollegiate Athletics &amp; Rec
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              05/08/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The SUNY Geneseo Department of Intercollegiate Athletics and Recreation, part of the Division of Student and Campus Life, seeks qualified candidates for the position of Assistant Coach for Men&#8217;s and Women&#8217;s Swimming and Diving (part-time). This is a pool posting and applicants will be reviewed only when there is a need to fill a position.
WE HAVE AN IMMEDIATE NEED FOR 2019.
This part-tim&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2797" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2797" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Assistant Director of Residence Life for Staff Training and Development">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2795">Assistant Director of Residence Life for Staff Training and Development</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S155
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Residence Life
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/05/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The Assistant Director of Residence Life is one of four leaders in the Department of Residence Life at SUNY Geneseo, a premier public liberal arts college.  A primary focus of the position is the promotion of student and staff learning through the implementation and assessment of department training, development, and cocurricular initiatives.  The Assistant Director provides direct oversight of&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2795" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2795" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Assistant Vice President for Facilities &amp; Planning">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2794">Assistant Vice President for Facilities &amp; Planning</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S158
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Facilities Services
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/10/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The Assistant Vice President for Facilities and Planning reports to the Vice President for Finance &amp; Administration and has direct responsibility for the Departments of Facilities Services, Facilities Planning and Construction, and Environmental Health and Safety. The Assistant Vice President is one of the four members of the Vice President&#8217;s Senior Staff and represents the Vice President with &#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2794" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2794" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Medical Assistant, SG-08">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2791">Medical Assistant, SG-08</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              C220
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Student Health &amp; Counseling
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Classified
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/25/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              08/02/2019
          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                HIGHLIGHTS
SUNY Geneseo is searching for a new team member to join The Health and Counseling Office as a Medical Assistant. The incumbent will interact with students, clinical personnel and all other public entities in a professional and helpful manner.

He or she will be responsible for performing clinical laboratory activities in Student Health and Counseling, at outreach activiti&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2791" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2791" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Lead Programmer Analyst">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2779">Lead Programmer Analyst</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S165
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Computing &amp; Information Technology
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/28/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Computing and Information Technology at SUNY Geneseo seeks to hire a Lead Programmer Analyst to join the Information Systems group. The Lead Programmer Analyst analyzes, designs, constructs, tests, documents, and supports software associated with campus administrative information systems. In addition to custom developed software, the position will be responsible for configuration and integratio&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2779" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2779" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Graduate Assistant">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2777">Graduate Assistant</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S164
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Academic Affairs Administration
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/26/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                This is a pool posting for graduate assistants. Positions may be available in a variety of departments with roles in teaching, administration or coaching.
Appointment may be 50%FTE and work 20 hours a week or 25%FTE and work 10 hours per week. The current stipend (as of 6/12/2019) for a full-time grad assistant working 20 hours is $8427 paid over 20 checks per academic year.
Dependent upon p&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2777" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2777" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Community and College Substance Abuse Prevention Coordinator">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2762">Community and College Substance Abuse Prevention Coordinator</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S161
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Student &amp; Campus Life
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/20/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The Community and College Substance Abuse Prevention Coordinator will be responsible for leading the efforts of the College to implement preventive strategies to reduce illegal and high risk alcohol and other drug consumption.
The Community and College Substance Abuse Prevention Coordinator will lead our Campus Community Coalition in these efforts. In accordance with the recommendations outl&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2762" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2762" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Technology Support Associate">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2760">Technology Support Associate</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S160
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Computing &amp; Information Technology
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/18/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The Technology Support Associate provides technical support to faculty and staff. This involves facilitating the use of technology, problem solving, troubleshooting and maintaining departmental computer hardware, software, and specialized equipment. The Technology Support Associate also provides technical assistance to our community through our HelpDesk. CIT is committed to building a culturall&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2760" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2760" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Learning Spaces Technician">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2755">Learning Spaces Technician</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S159
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Computing &amp; Information Technology
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/11/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                SUNY Geneseo seeks applicants for a Learning Spaces Technician. The Learning Spaces Technician provides support for technology in our academic classrooms. This includes responding to calls from the campus community, troubleshooting equipment problems, and performing upgrades and repairs. The Technician also provides support for in-class web/video conferences and coordinates and assists with rec&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2755" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2755" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Head Women&#x27;s Tennis Coach">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2752">Head Women&#x27;s Tennis Coach</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              S149
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Intercollegiate Athletics &amp; Rec
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Staff
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              04/09/2019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The SUNY Geneseo Department of Intercollegiate Athletics and Recreation, part of the Division of Student and Campus Life, seeks qualified candidates for the position of Head Women’s Tennis Coach.
This part-time, 10-month position will coordinate and oversee all aspects of the highly successful women’s tennis program. The anticipated annual salary range is $12,000 &#8211; $14,000. The selected cand&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2752" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2752" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Mathematics">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2715">Adjunct Lecturer - Mathematics</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F004
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Mathematics
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in Mathematics. Possible courses include:
MATH 112 Precalculus
MATH 221 Calculus I
MATH 222 Calculus II
MATH 213 Applied Calculus (for Business majors)
MATH 242 Elements of Probability and Statistics
MATH 262 Applied Statistics
MATH 140 Mathematical Concepts for Elementary Education I
MATH 141 Mathematical Concepts for Elementary Education II&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2715" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2715" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Communication">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2714">Adjunct Lecturer - Communication</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F024
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Communication
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in Communication. Check the online Undergraduate Bulletin for a complete listing of courses offered by the department.
This is a pool posting.  Applications are accepted on an ongoing basis and remain active for up to two years.  New adjunct lecturers are hired when needed to staff courses.
              </span>
              <span class='job-actions'>
                  <a href="/postings/2714" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2714" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer in Finance">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2713">Adjunct Lecturer in Finance</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F011
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              School of Business
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in Finance. Possible teaching assignments include courses on managerial finance (principles), investments, portfolio management or personal finance. Applicant cover letter should address prior undergraduate teaching experience, including listing all courses in the area of finance that the applicant has previously taught.
This is a pool posting. Applications are ac&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2713" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2713" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer in Economics">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2712">Adjunct Lecturer in Economics</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F013
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              School of Business
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in Economics.  Possible teaching assignments include courses on micro and macro economics, quantitative methods, or econometrics.  Applicant cover letter should address prior undergraduate teaching experience, including listing all courses in the area of economics that the applicant has previously taught.
This is a pool posting.  Applications are accepted on an on&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2712" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2712" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - English">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2711">Adjunct Lecturer - English</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F003
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              English
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in English, writing, or humanities. Possible courses include:
ENGL 101 Topics in Literature
ENGL 201 Foundations of Creative Writing
INTD 105 Critical Writing and Reading
HUMN 220 Western Humanities I
This is a pool posting. Applications are accepted on an ongoing basis and remain active for up to two years. New adjunct lecturers are hired when needed to st&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2711" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2711" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer-Arabic, Chinese, German, Japanese, Italian, Latin, or Russian">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2710">Adjunct Lecturer-Arabic, Chinese, German, Japanese, Italian, Latin, or Russian</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F051
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Languages &amp; Literatures
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              05/06/2016
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in the target language. Possible courses include elementary and intermediate language courses.
This is a pool position. Applications are accepted on an ongoing basis and remain active for up to two years. New adjunct lecturers are hired when needed to staff courses.
              </span>
              <span class='job-actions'>
                  <a href="/postings/2710" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2710" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Psychology">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2709">Adjunct Lecturer - Psychology</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F002
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Psychology
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in Psychology.  Possible courses include:
Psyc 100 Introductory Psychology
Psyc 202 Educational Psychology
Psyc 215 Child Development
Psyc 216 Adolescent Development
Psyc 250 Psychological Statistics
Psyc 251 Behavioral Research Methods
Psyc 260 Abnormal Psychology
This is a pool posting.  Applications are accepted on an ongoing basis and remain active for&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2709" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2709" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Instrumental Music Instructor (Woodwinds)">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2708">Instrumental Music Instructor (Woodwinds)</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F078
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Music
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/28/2017
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                SUNY Geneseo is accepting applications for instrumental music instructors with specialization in one or more of the woodwind instruments, typically flute, clarinet, saxophone, oboe, or bassoon. Duties include teaching lessons to majors and non-majors and coaching a section of the Geneseo Symphony Orchestra and/or of other student ensembles. Playing in rehearsals and performances with the Genese&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2708" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2708" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Instrumental Music Instructor (Strings)">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2707">Instrumental Music Instructor (Strings)</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F105
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Music
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              06/13/2018
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                SUNY Geneseo is accepting applications for instrumental music instructors with specialization in one or more of the orchestral string instruments, typically violin, viola, cello, or double bass. Duties include teaching lessons to majors and non-majors and coaching a section of the Geneseo Symphony Orchestra and/or of other student ensembles.
This is a pool posting. Applications are accepte&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2707" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2707" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Early Childhood Education">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2706">Adjunct Lecturer - Early Childhood Education</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F046
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              School of Education
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              07/15/2016
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                The Ella Cline Shear School of Education is accepting applications for the position of Adjunct Lecturer for an adjunct teaching position in Early Childhood Education. SUNY Geneseo’s undergraduate teacher education program in Early Childhood-Childhood has a strong focus on the learner and experiential learning. We seek applications from individuals with a masters degree or above in Early Childho&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2706" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2706" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Special Education">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2705">Adjunct Lecturer - Special Education</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F044
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              School of Education
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              07/13/2016
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Adjunct Lecturer in Education – Special Education
The Ella Cline Shear School of Education is accepting applications for the position of Adjunct Lecturer in Special Education. SUNY Geneseo’s undergraduate teacher education programs aim to develop candidates with a strong preparation in inclusive education as well as in specialized instructional settings.  The successful candidate(s) must show &#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2705" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2705" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Art History">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2704">Adjunct Lecturer - Art History</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F032
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Art History
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              03/15/2016
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach introductory level survey courses in Art History, including large enrollment sections.  Possible courses include:
Survey of Western European Art
Survey of Asian Art
And others
This is a pool posting.  Applications are accepted on an ongoing basis and remain active for up to two years.  New adjunct lecturers are hired when needed to staff courses.
              </span>
              <span class='job-actions'>
                  <a href="/postings/2704" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2704" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Geological Sciences">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2703">Adjunct Lecturer - Geological Sciences</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F008
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Geological Sciences
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in Geological Sciences. Possible courses include:
GSCI 120/121: Our Geologic Environment and Lab
GSCI 140/141: Environmental Science
GSCI 200: Environmental Geology
GSCI 331: Geomorphology
This is a pool posting. Applications are accepted on an ongoing basis and remain active for up to two years. New adjunct lecturers are hired when needed to staff courses.
              </span>
              <span class='job-actions'>
                  <a href="/postings/2703" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2703" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Chemistry">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2702">Adjunct Lecturer - Chemistry</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F019
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Chemistry
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach undergraduate courses in Chemistry.  Possible courses include:
•	Chem 116/118:   Chemistry I and II
•	Chem 203/204:   Principles of Chemistry I and II
•	Chem 211/213:   Organic Chemistry I and II
•	Chem 223/224:   Principles of Organic Chemistry I and II
•	Chem 119: General Chemistry Lab
•	Chem 216:  Organic  Chemistry Lab
This is a pool posting.  Applications are accepted on&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2702" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2702" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - History">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2700">Adjunct Lecturer - History</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F005
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              History
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach introductory undergraduate courses in History.  Possible courses include:
HIST 105 Western Civilization to 1600
HIST 106 Western Civilization 1600-Present
HIST 112 World History I
HIST 113 World History II
HIST 150 US History to Reconstruction
HIST 151 US History since Reconstruction
Other 100- and 200-level history courses based on instructor&#8217;s expertise.
This is a pool pos&#8230;
              </span>
              <span class='job-actions'>
                  <a href="/postings/2700" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2700" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>
    <div class='job-item job-item-posting' data-posting-title="Adjunct Lecturer - Business Communications">
  <div class='container-fluid'>
    <div class='row'>
      <div class='col-md-4 col-xs-12 job-title job-title-text-wrap'>
        <h3>
            <a href="/postings/2699">Adjunct Lecturer - Business Communications</a>
        </h3>
      </div>
      <div class='col-md-8 col-xs-12 '>
        <div class='col-md-2 col-xs-12'></div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              F054
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Communication
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              Faculty
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>
              11/02/2016
          </div>
          <div class='col-md-2 col-xs-12 job-title job-title-text-wrap col-md-push-0'>

          </div>
      </div>
    </div>

    <div class='row'>
      <div class='col-md-12 col-xs-12'>
            <div class='details'>
              <span class='job-description'>
                Teach required course for undergraduate School of Business students, INTD 205 Business Communications.
This course involves teaching both oral presentation skills and professional writing skills.
This is a pool posting. Applications are accepted on an ongoing basis and remain active for up to two years. New adjunct lecturers are hired when needed to staff courses.
              </span>
              <span class='job-actions'>
                  <a href="/postings/2699" class="btn primary_button_color">View Details</a>
                    <a href="/bookmarks?posting_id=2699" class="btn tertiary_button_color" data-method="post" rel="nofollow">Bookmark</a>
              </span>
            </div>
        </div>
      </div>
    </div>
  </div>

</div>

<div class="pagination"><span class="previous_page disabled"><span class="translation_missing" title="translation missing: en.previous">Previous</span></span> <em class="current">1</em> <a rel="next" href="/postings/search?page=2">2</a> <a class="next_page" rel="next" href="/postings/search?page=2"><span class="translation_missing" title="translation missing: en.next">Next</span></a></div>

                <div class='clearfix'></div>
              </div>
              <div class='clearfix'></div>
            </div>
          </div>
          <div id="footer" class="mainContent">
            <div class="container-fluid">
  <div class="row">
    <div class="col-lg-4 col-sm-4"><style>

.secondary_button_color {
color: #fff
}
</style></div>
    <div class="col-lg-4 col-sm-4"></div>
    <div class="col-lg-4 col-sm-4"></div>
  </div>
</div>

          </div>
        </div>
      </div>
    <form accept-charset="UTF-8" action="/session/check_timeout_callback" id="check_session_timeout" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="LZkrxrkFwk2IEGCb7eUxFCbWrUA7xRMFuZx2SRrBTPg=" /></div>
</form>
    <script type="text/javascript">
  var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
  document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
  try {
    var pageTracker = _gat._getTracker("UA-102598300-1");
    pageTracker._trackPageview();
  } catch(err) {}
</script>

<script type="text/javascript">
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
    ga('create', 'UA-52617323-2', 'auto', 'paTracker');
    ga('paTracker.set', 'dimension1', 'jobs.geneseo.edu');
    ga('paTracker.send', 'pageview');

</script>



    <script src="/javascripts/cached/all.js?1561655372" type="text/javascript"></script>
      <script src="/javascripts/bootstrap.min.js?1561655372" type="text/javascript"></script>

    <!-- no push timestamp -->
  </body>
</html>
'''




from bs4 import BeautifulSoup





soup = BeautifulSoup(html, 'html5lib')



# Find pagination class elems
for i in soup.find_all(class_='pagination'):

    # Find anchor tags
    for ii in i.find_all('a'):

        # Find next page url
        if ii.text.lower() == 'next':
            print(ii.text, '\n', ii.get('href'), '\n\n')
























