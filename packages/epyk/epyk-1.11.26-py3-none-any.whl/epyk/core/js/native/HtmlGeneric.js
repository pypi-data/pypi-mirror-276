function htmlGeneric(c,a,b){if(b.templateMode=='loading'){a=b.templateLoading(a);}else if(b.templateMode=='error'){a=b.templateError(a);}else if(typeof b.template!=='undefined'&&a){a=b.template(a);}c.innerHTML=a;}