"use strict";var BugDispatch={options:{minDelay:500,maxDelay:1e4,minBugs:2,maxBugs:20,minSpeed:5,maxSpeed:10,maxLargeTurnDeg:150,maxSmallTurnDeg:10,maxWiggleDeg:5,imageSprite:"static/bug/fly-sprite.png",bugWidth:13,bugHeight:14,num_frames:5,zoom:10,canFly:!0,canDie:!0,numDeathTypes:3,monitorMouseMovement:!1,eventDistanceToBug:40,minTimeBetweenMultipy:1e3,mouseOver:"random"},initialize:function(a){if(this.options=mergeOptions(this.options,a),this.options.minBugs>this.options.maxBugs&&(this.options.minBugs=this.options.maxBugs),this.modes=["multiply","nothing"],this.options.canFly&&this.modes.push("fly","flyoff"),this.options.canDie&&this.modes.push("die"),-1==this.modes.indexOf(this.options.mouseOver)&&(this.options.mouseOver="random"),this.transform=null,this.transforms={Moz:function(a){this.bug.style.MozTransform=a},webkit:function(a){this.bug.style.webkitTransform=a},O:function(a){this.bug.style.OTransform=a},ms:function(a){this.bug.style.msTransform=a},Khtml:function(a){this.bug.style.KhtmlTransform=a},w3c:function(a){this.bug.style.transform=a}},"transform"in document.documentElement.style)this.transform=this.transforms.w3c;else{var b=["Moz","webkit","O","ms","Khtml"],c=0;for(c=0;c<b.length;c++)if(b[c]+"Transform"in document.documentElement.style){this.transform=this.transforms[b[c]];break}}if(this.transform){this.bugs=[];var d="multiply"===this.options.mouseOver?this.options.minBugs:this.random(this.options.minBugs,this.options.maxBugs,!0),c=0,e=this;for(c=0;c<d;c++){var a=JSON.parse(JSON.stringify(this.options)),f=SpawnBug();a.wingsOpen=!this.options.canFly||Math.random()>.5,a.walkSpeed=this.random(this.options.minSpeed,this.options.maxSpeed),f.initialize(this.transform,a),this.bugs.push(f)}for(this.spawnDelay=[],c=0;c<d;c++){var g=this.random(this.options.minDelay,this.options.maxDelay,!0),h=this.bugs[c];this.spawnDelay[c]=setTimeout(function(a){return function(){e.options.canFly?a.flyIn():a.walkIn()}}(h),g),e.add_events_to_bug(h)}this.options.monitorMouseMovement&&(window.onmousemove=function(){e.check_if_mouse_close_to_bug()})}},stop:function(){for(var a=0;a<this.bugs.length;a++)this.spawnDelay[a]&&clearTimeout(this.spawnDelay[a]),this.bugs[a].stop()},end:function(){for(var a=0;a<this.bugs.length;a++)this.spawnDelay[a]&&clearTimeout(this.spawnDelay[a]),this.bugs[a].stop(),this.bugs[a].remove()},reset:function(){this.stop();for(var a=0;a<this.bugs.length;a++)this.bugs[a].reset(),this.bugs[a].walkIn()},killAll:function(){for(var a=0;a<this.bugs.length;a++)this.spawnDelay[a]&&clearTimeout(this.spawnDelay[a]),this.bugs[a].die()},add_events_to_bug:function(a){var b=this;a.bug&&(a.bug.addEventListener?a.bug.addEventListener("mouseover",function(c){b.on_bug(a)}):a.bug.attachEvent&&a.bug.attachEvent("onmouseover",function(c){b.on_bug(a)}))},check_if_mouse_close_to_bug:function(a){if(a=a||window.event){var b=0,c=0;a.client&&a.client.x?(b=a.client.x,c=a.client.y):a.clientX?(b=a.clientX,c=a.clientY):a.page&&a.page.x?(b=a.page.x-(document.body.scrollLeft+document.documentElement.scrollLeft),c=a.page.y-(document.body.scrollTop+document.documentElement.scrollTop)):a.pageX&&(b=a.pageX-(document.body.scrollLeft+document.documentElement.scrollLeft),c=a.pageY-(document.body.scrollTop+document.documentElement.scrollTop));var d=this.bugs.length,e=0;for(e=0;e<d;e++){var f=this.bugs[e].getPos();f&&Math.abs(f.top-c)+Math.abs(f.left-b)<this.options.eventDistanceToBug&&!this.bugs[e].flyperiodical&&this.near_bug(this.bugs[e])}}},near_bug:function(a){this.on_bug(a)},on_bug:function(a){if(a.alive){var b=this.options.mouseOver;if("random"===b&&(b=this.modes[this.random(0,this.modes.length-1,!0)]),"fly"===b)a.stop(),a.flyRand();else{if("nothing"===b)return;if("flyoff"===b)a.stop(),a.flyOff();else if("die"===b)a.die();else if("multiply"===b&&!this.multiplyDelay&&this.bugs.length<this.options.maxBugs){var c=SpawnBug(),d=JSON.parse(JSON.stringify(this.options)),e=a.getPos(),f=this;d.wingsOpen=!this.options.canFly||Math.random()>.5,d.walkSpeed=this.random(this.options.minSpeed,this.options.maxSpeed),c.initialize(this.transform,d),c.drawBug(e.top,e.left),d.canFly?(c.flyRand(),a.flyRand()):(c.go(),a.go()),this.bugs.push(c),this.multiplyDelay=!0,setTimeout(function(){f.add_events_to_bug(c),f.multiplyDelay=!1},this.options.minTimeBetweenMultipy)}}}},random:function(a,b,c){if(a==b)return c?Math.round(a):a;var d=a-.5+Math.random()*(b-a+1);return d>b?d=b:d<a&&(d=a),c?Math.round(d):d}},BugController=function(){this.initialize.apply(this,arguments)};BugController.prototype=BugDispatch;var SpiderController=function(){var a={imageSprite:"static/bug/spider-sprite.png",bugWidth:69,bugHeight:90,num_frames:7,canFly:!1,canDie:!0,numDeathTypes:2,zoom:6,minDelay:200,maxDelay:3e3,minSpeed:6,maxSpeed:13,minBugs:3,maxBugs:10};this.options=mergeOptions(this.options,a),this.initialize.apply(this,arguments)};SpiderController.prototype=BugDispatch;var Bug={options:{wingsOpen:!1,walkSpeed:2,flySpeed:40,edge_resistance:50,zoom:10},initialize:function(a,b){this.options=mergeOptions(this.options,b),this.NEAR_TOP_EDGE=1,this.NEAR_BOTTOM_EDGE=2,this.NEAR_LEFT_EDGE=4,this.NEAR_RIGHT_EDGE=8,this.directions={},this.directions[this.NEAR_TOP_EDGE]=270,this.directions[this.NEAR_BOTTOM_EDGE]=90,this.directions[this.NEAR_LEFT_EDGE]=0,this.directions[this.NEAR_RIGHT_EDGE]=180,this.directions[this.NEAR_TOP_EDGE+this.NEAR_LEFT_EDGE]=315,this.directions[this.NEAR_TOP_EDGE+this.NEAR_RIGHT_EDGE]=225,this.directions[this.NEAR_BOTTOM_EDGE+this.NEAR_LEFT_EDGE]=45,this.directions[this.NEAR_BOTTOM_EDGE+this.NEAR_RIGHT_EDGE]=135,this.angle_deg=0,this.angle_rad=0,this.large_turn_angle_deg=0,this.near_edge=!1,this.edge_test_counter=10,this.small_turn_counter=0,this.large_turn_counter=0,this.fly_counter=0,this.toggle_stationary_counter=50*Math.random(),this.zoom=this.random(this.options.zoom,10)/10,this.stationary=!1,this.bug=null,this.active=!0,this.wingsOpen=this.options.wingsOpen,this.transform=a,this.walkIndex=0,this.flyIndex=0,this.alive=!0,this.twitchTimer=null,this.rad2deg_k=180/Math.PI,this.deg2rad_k=Math.PI/180,this.makeBug(),this.angle_rad=this.deg2rad(this.angle_deg),this.angle_deg=this.random(0,360,!0)},go:function(){if(this.transform){this.drawBug();var a=this;this.animating=!0,this.going=requestAnimFrame(function(b){a.animate(b)})}},stop:function(){this.animating=!1,this.going&&(clearTimeout(this.going),this.going=null),this.flyperiodical&&(clearTimeout(this.flyperiodical),this.flyperiodical=null),this.twitchTimer&&(clearTimeout(this.twitchTimer),this.twitchTimer=null)},remove:function(){this.active=!1,this.inserted&&this.bug.parentNode&&(this.bug.parentNode.removeChild(this.bug),this.inserted=!1)},reset:function(){this.alive=!0,this.active=!0,this.bug.style.bottom="",this.bug.style.top=0,this.bug.style.left=0},animate:function(a){if(this.animating&&this.alive&&this.active){var b=this;this.going=requestAnimFrame(function(a){b.animate(a)}),"_lastTimestamp"in this||(this._lastTimestamp=a);var c=a-this._lastTimestamp;if(!(c<40||(c>200&&(c=200),this._lastTimestamp=a,--this.toggle_stationary_counter<=0&&this.toggleStationary(),this.stationary))){if(--this.edge_test_counter<=0&&this.bug_near_window_edge()&&(this.angle_deg%=360,this.angle_deg<0&&(this.angle_deg+=360),Math.abs(this.directions[this.near_edge]-this.angle_deg)>15)){var d=this.directions[this.near_edge]-this.angle_deg,e=360-this.angle_deg+this.directions[this.near_edge];this.large_turn_angle_deg=Math.abs(d)<Math.abs(e)?d:e,this.edge_test_counter=10,this.large_turn_counter=100,this.small_turn_counter=30}if(--this.large_turn_counter<=0&&(this.large_turn_angle_deg=this.random(1,this.options.maxLargeTurnDeg,!0),this.next_large_turn()),--this.small_turn_counter<=0)this.angle_deg+=this.random(1,this.options.maxSmallTurnDeg),this.next_small_turn();else{var f=this.random(1,this.options.maxWiggleDeg,!0);(this.large_turn_angle_deg>0&&f<0||this.large_turn_angle_deg<0&&f>0)&&(f=-f),this.large_turn_angle_deg-=f,this.angle_deg+=f}this.angle_rad=this.deg2rad(this.angle_deg);var g=Math.cos(this.angle_rad)*this.options.walkSpeed*(c/100),h=-Math.sin(this.angle_rad)*this.options.walkSpeed*(c/100);this.moveBug(this.bug.left+g,this.bug.top+h,90-this.angle_deg),this.walkFrame()}}},makeBug:function(){if(!this.bug&&this.active){var a=this.wingsOpen?"0":"-"+this.options.bugHeight+"px",b=document.createElement("div");b.className="bug",b.style.background="transparent url("+this.options.imageSprite+") no-repeat 0 "+a,b.style.width=this.options.bugWidth+"px",b.style.height=this.options.bugHeight+"px",b.style.position="fixed",b.style.top=0,b.style.left=0,b.style.zIndex="9999999",this.bug=b,this.setPos()}},setPos:function(a,b){this.bug.top=a||this.random(this.options.edge_resistance,document.documentElement.clientHeight-this.options.edge_resistance),this.bug.left=b||this.random(this.options.edge_resistance,document.documentElement.clientWidth-this.options.edge_resistance),this.moveBug(this.bug.left,this.bug.top,90-this.angle_deg)},moveBug:function(a,b,c){this.bug.left=a,this.bug.top=b;var d="translate("+parseInt(a)+"px,"+parseInt(b)+"px)";c&&(d+=" rotate("+c+"deg)"),d+=" scale("+this.zoom+")",this.transform(d)},drawBug:function(a,b){this.bug||this.makeBug(),this.bug&&(a&&b?this.setPos(a,b):this.setPos(this.bug.top,this.bug.left),this.inserted||(this.inserted=!0,document.body.appendChild(this.bug)))},toggleStationary:function(){this.stationary=!this.stationary,this.next_stationary();var a=this.wingsOpen?"0":"-"+this.options.bugHeight+"px";this.stationary?this.bug.style.backgroundPosition="0 "+a:this.bug.style.backgroundPosition="-"+this.options.bugWidth+"px "+a},walkFrame:function(){var a=this.walkIndex*this.options.bugWidth*-1+"px",b=this.wingsOpen?"0":"-"+this.options.bugHeight+"px";this.bug.style.backgroundPosition=a+" "+b,++this.walkIndex>=this.options.num_frames&&(this.walkIndex=0)},fly:function(a){var b=this.bug.top,c=this.bug.left,d=c-a.left,e=b-a.top,f=Math.atan(e/d);if(Math.abs(d)+Math.abs(e)<50&&(this.bug.style.backgroundPosition=-2*this.options.bugWidth+"px -"+2*this.options.bugHeight+"px"),Math.abs(d)+Math.abs(e)<30&&(this.bug.style.backgroundPosition=-1*this.options.bugWidth+"px -"+2*this.options.bugHeight+"px"),Math.abs(d)+Math.abs(e)<10)return this.bug.style.backgroundPosition="0 0",this.stop(),void this.go();var g=Math.cos(f)*this.options.flySpeed,h=Math.sin(f)*this.options.flySpeed;(c>a.left&&g>0||c>a.left&&g<0)&&(g*=-1,Math.abs(d)<Math.abs(g)&&(g/=4)),(b<a.top&&h<0||b>a.top&&h>0)&&(h*=-1,Math.abs(e)<Math.abs(h)&&(h/=4)),this.moveBug(c+g,b+h)},flyRand:function(){this.stop();var a={};a.top=this.random(this.options.edge_resistance,document.documentElement.clientHeight-this.options.edge_resistance),a.left=this.random(this.options.edge_resistance,document.documentElement.clientWidth-this.options.edge_resistance),this.startFlying(a)},startFlying:function(a){var b=this.bug.top,c=this.bug.left,d=a.left-c,e=a.top-b;this.bug.left=a.left,this.bug.top=a.top,this.angle_rad=Math.atan(e/d),this.angle_deg=this.rad2deg(this.angle_rad),this.angle_deg=d>0?90+this.angle_deg:270+this.angle_deg,this.moveBug(c,b,this.angle_deg);var f=this;this.flyperiodical=setInterval(function(){f.fly(a)},10)},flyIn:function(){if(this.bug||this.makeBug(),this.bug){this.stop();var a=Math.round(4*Math.random()-.5),b=document,c=b.documentElement,d=b.getElementsByTagName("body")[0],e=window.innerWidth||c.clientWidth||d.clientWidth,f=window.innerHeight||c.clientHeight||d.clientHeight;a>3&&(a=3),a<0&&(a=0);var g={};0===a?(g.top=-2*this.options.bugHeight,g.left=Math.random()*e):1===a?(g.top=Math.random()*f,g.left=e+2*this.options.bugWidth):2===a?(g.top=f+2*this.options.bugHeight,g.left=Math.random()*e):(g.top=Math.random()*f,g.left=-3*this.options.bugWidth);var i=this.wingsOpen?"0":"-"+this.options.bugHeight+"px";this.bug.style.backgroundPosition=-3*this.options.bugWidth+"px "+i,this.bug.top=g.top,this.bug.left=g.left,this.drawBug();var j={};j.top=this.random(this.options.edge_resistance,document.documentElement.clientHeight-this.options.edge_resistance),j.left=this.random(this.options.edge_resistance,document.documentElement.clientWidth-this.options.edge_resistance),this.startFlying(j)}},walkIn:function(){if(this.bug||this.makeBug(),this.bug){this.stop();var a=Math.round(4*Math.random()-.5),b=document,c=b.documentElement,d=b.getElementsByTagName("body")[0],e=window.innerWidth||c.clientWidth||d.clientWidth,f=window.innerHeight||c.clientHeight||d.clientHeight;a>3&&(a=3),a<0&&(a=0);var g={};0===a?(g.top=-1.3*this.options.bugHeight,g.left=Math.random()*e):1===a?(g.top=Math.random()*f,g.left=e+.3*this.options.bugWidth):2===a?(g.top=f+.3*this.options.bugHeight,g.left=Math.random()*e):(g.top=Math.random()*f,g.left=-1.3*this.options.bugWidth);var i=this.wingsOpen?"0":"-"+this.options.bugHeight+"px";this.bug.style.backgroundPosition=-3*this.options.bugWidth+"px "+i,this.bug.top=g.top,this.bug.left=g.left,this.drawBug(),this.go()}},flyOff:function(){this.stop();var a=this.random(0,3),b={},c=document,d=c.documentElement,e=c.getElementsByTagName("body")[0],f=window.innerWidth||d.clientWidth||e.clientWidth,g=window.innerHeight||d.clientHeight||e.clientHeight;0===a?(b.top=-200,b.left=Math.random()*f):1===a?(b.top=Math.random()*g,b.left=f+200):2===a?(b.top=g+200,b.left=Math.random()*f):(b.top=Math.random()*g,b.left=-200),this.startFlying(b)},die:function(){this.stop();var a=this.random(0,this.options.numDeathTypes-1);this.alive=!1,this.drop(a)},drop:function(a){var b=this.bug.top,c=document,d=c.documentElement,e=c.getElementsByTagName("body")[0],f=window.innerHeight||d.clientHeight||e.clientHeight,f=f-this.options.bugHeight,g=this.random(0,20,!0),i=(Date.now(),this);this.dropTimer=requestAnimFrame(function(c){i._lastTimestamp=c,i.dropping(c,b,f,g,a)})},dropping:function(a,b,c,d,e){var f=a-this._lastTimestamp,g=f*f*.002,h=b+g,i=this;if(h>=c){h=c,clearTimeout(this.dropTimer),this.angle_deg=0,this.angle_rad=this.deg2rad(this.angle_deg),this.transform("rotate("+(90-this.angle_deg)+"deg) scale("+this.zoom+")"),this.bug.style.top=null;var j=(this.options.bugWidth*this.zoom-this.options.bugHeight*this.zoom)/2,k=this.options.bugHeight/2*(1-this.zoom);return this.bug.style.bottom=Math.ceil(j-k)+"px",this.bug.style.left=this.bug.left+"px",this.bug.style.backgroundPosition="-"+2*e*this.options.bugWidth+"px 100%",void this.twitch(e)}this.dropTimer=requestAnimFrame(function(a){i.dropping(a,b,c,d,e)}),f<20||(this.angle_deg=(this.angle_deg+d)%360,this.angle_rad=this.deg2rad(this.angle_deg),this.moveBug(this.bug.left,h,this.angle_deg))},twitch:function(a,b){b||(b=0);var c=this;0!==a&&1!==a||(c.twitchTimer=setTimeout(function(){c.bug.style.backgroundPosition="-"+(2*a+b%2)*c.options.bugWidth+"px 100%",c.twitchTimer=setTimeout(function(){b++,c.bug.style.backgroundPosition="-"+(2*a+b%2)*c.options.bugWidth+"px 100%",c.twitch(a,++b)},c.random(300,800))},this.random(1e3,1e4)))},rad2deg:function(a){return a*this.rad2deg_k},deg2rad:function(a){return a*this.deg2rad_k},random:function(a,b,c){if(a==b)return a;var d=Math.round(a-.5+Math.random()*(b-a+1));return c?Math.random()>.5?d:-d:d},next_small_turn:function(){this.small_turn_counter=Math.round(10*Math.random())},next_large_turn:function(){this.large_turn_counter=Math.round(40*Math.random())},next_stationary:function(){this.toggle_stationary_counter=this.random(50,300)},bug_near_window_edge:function(){return this.near_edge=0,this.bug.top<this.options.edge_resistance?this.near_edge|=this.NEAR_TOP_EDGE:this.bug.top>document.documentElement.clientHeight-this.options.edge_resistance&&(this.near_edge|=this.NEAR_BOTTOM_EDGE),this.bug.left<this.options.edge_resistance?this.near_edge|=this.NEAR_LEFT_EDGE:this.bug.left>document.documentElement.clientWidth-this.options.edge_resistance&&(this.near_edge|=this.NEAR_RIGHT_EDGE),this.near_edge},getPos:function(){return this.inserted&&this.bug&&this.bug.style?{top:parseInt(this.bug.top,10),left:parseInt(this.bug.left,10)}:null}},SpawnBug=function(){var b,a={};for(b in Bug)Bug.hasOwnProperty(b)&&(a[b]=Bug[b]);return a},mergeOptions=function(a,b,c){void 0===c&&(c=!0);var d=c?cloneOf(a):a;for(var e in b)b.hasOwnProperty(e)&&(d[e]=b[e]);return d},cloneOf=function(a){if(null==a||"object"!=typeof a)return a;var b=a.constructor();for(var c in a)a.hasOwnProperty(c)&&(b[c]=cloneOf(a[c]));return b};window.requestAnimFrame=function(){return window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimationFrame||function(a,b){window.setTimeout(a,1e3/60)}}();