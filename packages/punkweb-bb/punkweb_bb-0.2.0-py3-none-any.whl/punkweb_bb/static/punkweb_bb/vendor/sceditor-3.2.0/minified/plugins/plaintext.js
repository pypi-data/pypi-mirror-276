/* SCEditor v3.2.0 | (C) 2017, Sam Clarke | sceditor.com/license */
!function(t){"use strict";var i=t.utils,l=t.dom;t.plugins.plaintext=function(){var n=!0;this.init=function(){var t=this.commands,e=this.opts;e&&e.plaintext&&e.plaintext.addButton&&(n=e.plaintext.enabled,t.pastetext=i.extend(t.pastetext||{},{state:function(){return n?1:0},exec:function(){n=!n}}))},this.signalPasteRaw=function(t){var e;n&&(t.html&&!t.text&&((e=document.createElement("div")).innerHTML=t.html,i.each(e.querySelectorAll("p"),function(t,e){l.convertElement(e,"div")}),i.each(e.querySelectorAll("br"),function(t,e){e.nextSibling&&l.isInline(e.nextSibling,!0)||e.parentNode.removeChild(e)}),document.body.appendChild(e),t.text=e.innerText,document.body.removeChild(e)),t.html=null)}}}(sceditor);