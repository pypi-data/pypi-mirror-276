function breadcrumb(a,c,b){a.innerHTML="";if(typeof c==="undefined"){a.style["height"]=0;}else{if(c.length==0){a.style["height"]=0;}else{a.style["height"]=b.height+"px";var d=document.createTextNode(b.delimiter);a.appendChild(d);c.forEach(function(d,g){if(typeof d.type!=='undefined'){if(d.type=="dots"){var f=document.createTextNode("... ");a.appendChild(f);}}else{if(d.selected){var e=document.createElement("span");e.innerHTML=d.text;}else{var e=document.createElement("a");e.setAttribute('href',d.url);e.innerHTML=d.text;}Object.keys(b.style).forEach(function(a){e.style[a]=b.style[a];});if(d.selected){Object.keys(b.style_selected).forEach(function(a){e.style[a]=b.style_selected[a];});}a.appendChild(e);}var f=document.createTextNode(b.delimiter);if(g<c.length-1){a.appendChild(f);}});}}}