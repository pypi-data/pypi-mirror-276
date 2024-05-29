/**
 * SCEditor SVG monocons plugin
 * http://www.sceditor.com/
 *
 * Copyright (C) 2017, Sam Clarke (samclarke.com)
 *
 * SCEditor is licensed under the MIT license:
 *	http://www.opensource.org/licenses/mit-license.php
 *
 * @author Sam Clarke
 */
(function (document, sceditor) {
	'use strict';

	var dom = sceditor.dom;

	/* eslint max-len: off*/
	var icons = {
		'bold': '<text x="50%" y="50%" text-anchor="middle" dy=".5ex" font-family="Dejavu Sans, Helvetica, Arial, sans-serif" font-size="15" font-weight="bold">B</text>',
		'bulletlist': '<path d="M6 2h9v2H6zm0 5h9v2H6zm0 5h9v2H6z"/><circle cx="3" cy="3" r="1.75"/><circle cx="3" cy="8" r="1.75"/><circle cx="3" cy="13" r="1.75"/>',
		'center': '<path d="M1 1h14v2H1zm2 4h10v2H3zM1 9h14v2H1zm2 4h10v2H3z"/>',
		'code': '<path d="M7 6L4 9l3 3v-1.5L5.5 9 7 7.5zm2 0v1.5L10.5 9 9 10.5V12l3-3zM2.406 1A.517.517 0 0 0 2 1.5v13c0 .262.238.5.5.5h11a.52.52 0 0 0 .5-.5V4.375c.002-.102-.13-.193-.156-.219l-3-3A.506.506 0 0 0 10.5 1zM3 2h7v2.5c0 .262.238.5.5.5H13v9H3zm8 .688L12.313 4H11z"/>',
		'color': '<text x="50%" y="8" text-anchor="middle" dy=".5ex" font-family="Dejavu Sans, Helvetica, Arial, sans-serif" font-size="13" font-weight="bold">A</text><path class="sce-color" d="M2 13h12v2H2z"/>',
		'copy': '<path d="M6.404 5.002a.5.5 0 0 0-.406.5v10a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V8.596a.492.492 0 0 0 0-.094.662.662 0 0 0 0-.063v-.063l-.031-.063v-.031a.557.557 0 0 0-.094-.094l-.031-.031-2.875-2.844a.498.498 0 0 0-.125-.156.5.5 0 0 0-.344-.156h-5a.59.59 0 0 0-.094.001c-.239.046.031-.003 0 0zm.594 1h4v2.5a.5.5 0 0 0 .5.5h2.5v6h-7v-9zm5 .687l1.313 1.313h-1.313V6.689zM1.406.002a.517.517 0 0 0-.406.5v10c0 .262.238.5.5.5H7V6l3-.063V3.596a.492.492 0 0 0 0-.094.331.331 0 0 0 0-.063v-.063c-.009-.021-.02-.041-.031-.062v-.031a.597.597 0 0 0-.094-.094l-.031-.031L6.969.314a.484.484 0 0 0-.125-.156A.506.506 0 0 0 6.5.002h-5a.492.492 0 0 0-.094 0c-.229.044.032-.003 0 0zm.594 1h4v2.5c0 .262.238.5.5.5H9v1.029L7 5 6 6v4l-4 .002v-9zm5 .687l1.313 1.313H7V1.689z"/>',
		'cut': '<path d="M3 .5c0 2.936 3.774 7.73 3.938 7.938l-1.813 2.844A2.46 2.46 0 0 0 4 11c-1.375 0-2.5 1.125-2.5 2.5S2.625 16 4 16s2.5-1.125 2.5-2.5c0-.444-.138-.856-.344-1.22L8 9.845l1.844 2.438A2.473 2.473 0 0 0 9.5 13.5c0 1.375 1.125 2.5 2.5 2.5s2.5-1.125 2.5-2.5S13.375 11 12 11a2.46 2.46 0 0 0-1.125.28L9.062 8.439C9.226 8.232 13 3.437 13 .5h-1L8 6.78 4 .5H3zM4 12c.834 0 1.5.666 1.5 1.5S4.834 15 4 15s-1.5-.666-1.5-1.5S3.166 12 4 12zm8 0c.834 0 1.5.666 1.5 1.5S12.834 15 12 15s-1.5-.666-1.5-1.5.666-1.5 1.5-1.5z"/>',
		'date': '<path d="M8.1 7v1h2.7v1H8.094v3H11.7v-1H9v-1h2.7V7zM4.5 7v1h.8v3h-.8v1h2.7v-1h-.9V7zM.9 1v14h14.4V1h-1.8v2h-2.7V1H5.4v2H2.7V1zm.9 4h12.6v9H1.8z"/>',
		'email': '<path d="M1 4.5v8c0 .262.238.5.5.5h13a.52.52 0 0 0 .5-.5V4.594C15 4 15 4 14.5 4H1.563C1 4 1 4 1 4.5zM2 5h12v7H2V5zm-.187-.906l-.625.812 6.5 5 .312.219.313-.219 6.5-5-.625-.813L8 8.844l-6.187-4.75z"/>',
		'emoticon': '<path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm0 1a6 6 0 1 1 0 12A6 6 0 0 1 8 2zM6 5c-.546 0-1 .454-1 1s.454 1 1 1 1-.454 1-1-.454-1-1-1zm4 0c-.547 0-1 .454-1 1s.453 1 1 1c.547 0 1-.454 1-1s-.453-1-1-1zM4.5 9.5s-.002.652.469 1.281C5.44 11.409 6.389 12 8 12c1.611 0 2.561-.591 3.031-1.219.47-.629.469-1.281.469-1.281h-1s-.002.314-.281.688c-.279.374-.83.813-2.219.813-1.389 0-1.94-.44-2.219-.813C5.502 9.814 5.5 9.5 5.5 9.5z"/>',
		'font': '<path d="M7.953 9.75h-4.06l-.395 1.141c-.132.381-.254.752-.368 1.109H.7c.391-1.119.762-2.154 1.113-3.105a104.642 104.642 0 0 1 2.024-5.079 52.23 52.23 0 0 1 1.016-2.212h2.218a80.63 80.63 0 0 1 2.011 4.605c.337.84.105.338.458 1.288s-1.455 2.63-1.587 2.253zM5.912 3.959c-.052.151-.129.357-.229.616-.1.26-.215.56-.343.901-.129.341-.273.716-.431 1.125-.159.409-.32.839-.484 1.288h2.972c-.159-.45-.312-.882-.461-1.292a46.81 46.81 0 0 0-.425-1.127c-.135-.34-.252-.641-.354-.9-.1-.26-.182-.463-.245-.611zm6.949 10.042a36.325 36.325 0 0 0-.35-1.037l-.371-1.063H8.352l-.368 1.064A41.69 41.69 0 0 0 7.64 14H5.373c.365-1.045.711-2.01 1.039-2.896.328-.886.648-1.723.962-2.506.313-.786.623-1.53.927-2.235.305-.705.62-1.393.948-2.065h2.069c.318.672.634 1.36.941 2.065.311.705.621 1.449.936 2.235.314.783.636 1.619.964 2.506.327.888.676 1.853 1.041 2.896l-2.339.001zm-2.625-7.504c-.049.141-.118.333-.213.576-.094.242-.2.521-.319.84-.121.317-.254.668-.402 1.051-.147.382-.299.783-.45 1.201h2.772c-.147-.42-.291-.822-.433-1.205a43.073 43.073 0 0 0-.396-1.053c-.125-.317-.233-.598-.33-.84a13.884 13.884 0 0 0-.229-.57z"/>',
		'format': '<path d="M10.5 2v1.5H12c.235 0 .401-.009.5 0 .008.088 0 .279 0 .5v2H14V3.437c0-.237-.01-.409-.031-.593-.022-.185-.067-.42-.25-.594s-.407-.2-.594-.219A5.693 5.693 0 0 0 12.5 2zm0-2L7.187 2.5 10.5 5zm.5 5.187L13.5 8.5 16 5.187zm-.958-.339h-2.03l-3.234 8.456c-.154.392-.336.994-.854 1.022v.518h2.744v-.518c-.644-.168-.658-.462-.434-1.036l.784-2.086h3.43l.854 2.086c.238.574.308.924-.406 1.036v.518h3.276v-.518c-.434-.056-.546-.364-.686-.728l-3.444-8.75M7.424 10l1.26-3.318L10 10H7.424M4.912.975h-1.63L.686 7.764c-.124.314-.27.798-.686.82V9h2.203v-.416c-.517-.135-.528-.37-.348-.832l.629-1.674h2.754l.685 1.674c.192.461.248.742-.325.832V9c1.73.137 1.837-.002 2.079-1L4.912.975M2.81 5.11l1.012-2.664L4.878 5.11H2.81"/>',
		'grip': '<path d="M14.656 5.156l-10 10 .688.688 10-10-.688-.688zm0 3l-7 7 .688.688 7-7-.688-.688zm0 3l-4 4 .688.688 4-4-.688-.688z"/>',
		'horizontalrule': '<path d="M2 2v1h12V2H2zm0 2v1h9V4H2zm0 2v1h12V6H2zm0 2v2h12V8H2z"/>',
		'image': '<path d="M.5 2.5v11h15v-11H.5zm1 1h13v9h-13v-9z"/><circle cx="4" cy="6" r="1.25"/><path d="M1 11h14v2H1z"/><path d="M5 12l2-4 2 4z"/><path d="M7 12l4-7 4 7z"/>',
		'indent': '<path d="M1 1h14v2H1zm5 4h9v2H6zm0 4h9v2H6zm-5 4h14v2H1zm4-5L1 5v6z"/>',
		'italic': '<text x="50%" y="50%" text-anchor="middle" dy=".5ex" font-family="Dejavu Sans, Helvetica, Arial, sans-serif" font-weight="bold" font-size="15" font-style="italic">i</text>',
		'justify': '<path d="M1 1h14v2H1zm0 4h14v2H1zm0 4h14v2H1zm0 4h14v2H1z"/>',
		'left': '<path d="M1 1h14v2H1zm0 4h10v2H1zm0 4h14v2H1zm0 4h10v2H1z"/>',
		'link': '<path d="M2 4c-.625 0-1.009.438-1.188.75s-.269.63-.344.969c-.15.677-.219 1.476-.219 2.28s.068 1.605.219 2.282c.075.339.165.625.344.938s.563.78 1.188.78h4v-2H2.469c-.022-.065-.042-.06-.063-.155-.1-.447-.156-1.15-.156-1.844s.057-1.396.156-1.844c.02-.088.042-.092.063-.156H6V4H2zm8 0v2h3.531c.021.064.043.068.063.156.1.448.156 1.149.156 1.844s-.057 1.396-.156 1.844c-.021.096-.041.09-.063.156H10v2h4c.625 0 1.009-.47 1.188-.781s.269-.6.344-.938c.15-.678.219-1.476.219-2.281s-.068-1.604-.219-2.281c-.075-.34-.165-.656-.344-.97S14.625 4 14 4h-4zM5.719 7c-.523.074-.949.602-.875 1.125S5.477 9.074 6 9h4c.528.01 1-.472 1-1s-.472-1.007-1-1H6a.593.593 0 0 0-.188 0h-.093z"/>',
		'ltr': '<path d="M10.313 1.937c-.98 0-1.752.284-2.344.813-.592.529-.906 1.228-.906 2.094 0 .811.275 1.467.781 1.969.506.497 1.227.792 2.156.906V14h2V3h1v11h1V1.939zM2 4v8l4-4z"/>',
		'maximize': '<path d="M2 7l1.75-1.75-2-2L0 5V0h5L3.25 1.75l2 2L7 2v5H2zm9 9l1.75-1.75-2-2L9 14V9h5l-1.75 1.75 2 2L16 11v5h-5zm-6 0l-1.75-1.75 2-2L7 14V9H2l1.75 1.75-2 2L0 11v5h5zm6-16l1.75 1.75-2 2L9 2v5h5l-1.75-1.75 2-2L16 5V0h-5z"/>',
		'orderedlist': '<path d="M6 2h9v2H6zm0 5h9v2H6zm0 5h9v2H6zm-2.799.846q.392.1.594.352.205.25.205.636 0 .576-.441.877-.441.298-1.287.298-.298 0-.599-.05-.298-.046-.591-.142v-.77q.28.14.555.212.277.07.545.07.396 0 .607-.137.212-.138.212-.394 0-.265-.218-.4-.215-.137-.638-.137h-.4v-.644h.421q.376 0 .56-.116.185-.12.185-.36 0-.224-.18-.346-.178-.122-.505-.122-.242 0-.488.055-.246.054-.49.16v-.731q.295-.083.586-.125.29-.041.57-.041.756 0 1.13.249.375.246.375.744 0 .34-.179.558-.179.215-.529.304zm-.905-3.609H4v.734H1.186v-.734L2.599 7.99q.19-.172.28-.335.091-.163.091-.34 0-.272-.184-.438-.182-.166-.485-.166-.234 0-.511.101-.278.099-.594.296v-.851q.337-.112.667-.169.329-.06.645-.06.696 0 1.08.307.386.306.386.853 0 .317-.163.592-.164.272-.688.731l-.827.726zM1.228 4.276h.903V1.714l-.927.19V1.21l.922-.191h.971v3.258H4v.706H1.228v-.706z"/>',
		'outdent': '<path d="M1 1h14v2H1zm0 4h9v2H1zm0 4h9v2H1zm0 4h14v2H1zm10-5l4-3v6z"/>',
		'paste': '<path d="M4.406 0A.5.5 0 0 0 4 .5V1H1.5a.5.5 0 0 0-.5.5v10a.5.5 0 0 0 .5.5H6v2.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V7.594a.492.492 0 0 0 0-.094.436.436 0 0 0 0-.125.916.916 0 0 0-.031-.063v-.031a.749.749 0 0 0-.063-.063.749.749 0 0 0-.063-.063l-2.875-2.844a.498.498 0 0 0-.125-.156A.498.498 0 0 0 11.5 4H10V1.5a.5.5 0 0 0-.5-.5H7V.5a.5.5 0 0 0-.5-.5h-2a.492.492 0 0 0-.094 0c-.239.045.032-.003 0 0zM2 2h1v.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5V2h1v2H6.5a.64.64 0 0 0-.062 0 .493.493 0 0 0-.094.031.474.474 0 0 0-.125.063l-.031.031-.031.031a.916.916 0 0 0-.063.031.47.47 0 0 0-.031.094l-.031.031A.506.506 0 0 0 6 4.5V11H2V2zm5 3h4v2.5a.5.5 0 0 0 .5.5H14v6H7v-2.406a.492.492 0 0 0 0-.094V5zm5 .688L13.313 7H12V5.688zM4.406 0A.5.5 0 0 0 4 .5V1H1.5a.5.5 0 0 0-.5.5v10a.5.5 0 0 0 .5.5h5a.5.5 0 0 0 .5-.5V5h2.5a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5H7V.5a.5.5 0 0 0-.5-.5h-2a.492.492 0 0 0-.094 0c-.239.045.032-.003 0 0zM2 2h1v.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5V2h1v2H6.5a.5.5 0 0 0-.5.5V11H2V2zm4.406 2A.5.5 0 0 0 6 4.5v10a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V7.594a.492.492 0 0 0 0-.094.331.331 0 0 0 0-.063v-.063a.916.916 0 0 0-.031-.063V7.28a.523.523 0 0 0-.094-.094l-.031-.031-2.875-2.844a.498.498 0 0 0-.125-.156A.503.503 0 0 0 11.5 4h-5a.492.492 0 0 0-.094 0c-.239.045.032-.003 0 0zM7 5h4v2.5a.5.5 0 0 0 .5.5H14v6H7V5zm5 .688L13.313 7H12V5.688zM8 12h5v1H8v-1zm0-2h5v1H8v-1zm0-2h5v1H8V8zm0-2h3v1H8V6z"/>',
		'pastetext': '<path d="M4.406 0A.5.5 0 0 0 4 .5V1H1.5a.5.5 0 0 0-.5.5v10a.5.5 0 0 0 .5.5H6v2.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V7.594a.492.492 0 0 0 0-.094.436.436 0 0 0 0-.125.916.916 0 0 0-.031-.063v-.031a.749.749 0 0 0-.063-.063.749.749 0 0 0-.063-.063l-2.875-2.844a.498.498 0 0 0-.125-.156A.498.498 0 0 0 11.5 4H10V1.5a.5.5 0 0 0-.5-.5H7V.5a.5.5 0 0 0-.5-.5h-2a.492.492 0 0 0-.094 0zM2 2h1v.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5V2h1v2H6.5a.64.64 0 0 0-.062 0 .493.493 0 0 0-.094.031.474.474 0 0 0-.125.063l-.031.031-.031.031a.916.916 0 0 0-.063.031.47.47 0 0 0-.031.094l-.031.031A.506.506 0 0 0 6 4.5V11H2V2zm5 3h4v2.5a.5.5 0 0 0 .5.5H14v6H7v-2.406a.492.492 0 0 0 0-.094V5zm5 .688L13.313 7H12V5.688zM4.406 0A.5.5 0 0 0 4 .5V1H1.5a.5.5 0 0 0-.5.5v10a.5.5 0 0 0 .5.5h5a.5.5 0 0 0 .5-.5V5h2.5a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5H7V.5a.5.5 0 0 0-.5-.5h-2a.492.492 0 0 0-.094 0zM2 2h1v.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5V2h1v2H6.5a.5.5 0 0 0-.5.5V11H2V2zm4.406 2A.5.5 0 0 0 6 4.5v10a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5V7.594a.492.492 0 0 0 0-.094.331.331 0 0 0 0-.063v-.062a.916.916 0 0 0-.031-.063v-.031a.523.523 0 0 0-.094-.094l-.031-.031-2.875-2.844a.498.498 0 0 0-.125-.156A.5.5 0 0 0 11.5 4h-5a.492.492 0 0 0-.094 0zM7 5h4v2.5a.5.5 0 0 0 .5.5H14v6H7V5zm5 .688L13.313 7H12V5.688z"/>',
		'print': '<path d="M4 1v3H1v8h2V6h10v6h2V4h-3V1zm1 1h6v2H5zM4 7v8h8V7zm1 1h6v6H5zm1 1v1h4V9zm0 2v1h4v-1z"/>',
		'quote': '<path d="M8 2.013c-1.998 0-3.818.382-5.188 1.125S.499 5.054.499 6.513c0 1.237.926 2.345 2.281 3.156s3.197 1.344 5.219 1.344c.344 0 .563.019.906 0l5.875 2.938c.377.18.854-.32.656-.688l-1.813-3.656c1.242-.79 1.875-2.014 1.875-3.094 0-1.46-.943-2.632-2.313-3.375S9.998 2.013 8 2.013z"/>',
		'redo': '<path d="M9 7l5-5v5z"/><path d="M9.553 2.205c1 .268 1.932.796 2.69 1.553l.706.707-1.414 1.414-.707-.707a3.995 3.995 0 0 0-3.863-1.035 3.995 3.995 0 0 0-2.828 2.828 3.995 3.995 0 0 0 1.035 3.863l.707.707-1.414 1.414-.707-.707a6.003 6.003 0 0 1-1.553-5.795 6.003 6.003 0 0 1 7.348-4.242z"/>',
		'removeformat': '<path d="M8.781 2l-.125.125L3.781 7l-.125.125-3 3-.313.313.25.344 3 4 .156.219h2.47l.125-.156 3-3 .313-.313 4.688-4.688.313-.313-.25-.344-3-4-.156-.188H8.781zm.407 1h.594l-4 4h-.594l4-4zm1.75.25l2.406 3.188-4.281 4.28-2.406-3.187 4.281-4.281z"/>',
		'right': '<path d="M1 1h14v2H1zm4 4h10v2H5zM1 9h14v2H1zm4 4h10v2H5z"/>',
		'rtl': '<path d="M5.344 2.001c-.98 0-1.783.284-2.375.813-.592.529-.875 1.227-.875 2.093 0 .811.244 1.467.75 1.969.506.497 1.227.792 2.156.906V14h2V3.001L8 3v11h1V2zM14 4l-4 4 4 4z"/>',
		'size': '<path d="M12.5.656L10 4h5L12.5.656zM4.594 4.5a49.476 49.476 0 0 0-.875 1.906c-.277.65-.581 1.334-.875 2.063-.286.729-.572 1.52-.875 2.344S1.338 12.53 1 13.5h2.094c.095-.313.2-.64.313-.97.121-.328.262-.64.375-.968h3.5c.113.329.231.64.344.969.121.329.217.656.313.969h2.188c-.338-.971-.666-1.864-.969-2.688s-.611-1.615-.906-2.344a56.045 56.045 0 0 0-.844-2.063c-.286-.66-.581-1.282-.875-1.906H4.594zM10 6l2.5 3.313L15 6h-5zm-4.5.53c.052.13.132.307.219.532.086.225.2.486.313.78.121.296.245.614.375.97s.268.734.406 1.125H4.25c.139-.391.245-.77.375-1.125.139-.355.293-.674.406-.97s.194-.555.281-.78c.087-.224.145-.401.188-.531z"/>',
		'source': '<path d="M4.937 3.939L1 8.499l3.937 4.564L6 12 3 8.499 6 5zm6.126 0L10 5.002l3 3.503-3 3.497 1.063 1.063L15 8.505z"/>',
		'strike': '<text x="50%" y="50%" text-anchor="middle" dy=".5ex" font-family="Dejavu Sans, Helvetica, Arial, sans-serif" font-size="15" font-weight="bold">S</text><path d="M1 7v1h14V7H1z"/>',
		'subscript': '<path d="M11 10v1h3v1h-3v3h4v-1h-3v-1h3v-3zM1 3l3 5-3 5h2l3-5H4l3 5h2L6 8l3-5H7L4 8h2L3 3z"/>',
		'superscript': '<path d="M11 1v1h3v1h-3v3h4V5h-3V4h3V1zM1 3l3 5-3 5h2l3-5H4l3 5h2L6 8l3-5H7L4 8h2L3 3z"/>',
		'table': '<path d="M1 2h14v2H1zm0 2v10h14V4H1zm1 1h3.5v2H2V5zm4.5 0h3v2h-3V5zm4 0H14v2h-3.5V5zM2 8h3.5v2H2V8zm4.5 0h3v2h-3V8zm4 0H14v2h-3.5V8zM2 11h3.5v2H2v-2zm4.5 0h3v2h-3v-2zm4 0H14v2h-3.5v-2z"/>',
		'time': '<path d="M8 0C3 0 0 4 0 8s3 8 8 8 8-4 8-8-3-8-8-8zm0 2c3.461 0 6 2.539 6 6s-2.539 6-6 6c-3.46 0-6-2.539-6-6s2.54-6 6-6zM7 3v6l2.5 2L11 9.5 9 8V3z"/>',
		'underline': '<text x="50%" y="50%" text-anchor="middle" dy=".5ex" font-family="Dejavu Sans, Helvetica, Arial, sans-serif" font-weight="bold" font-size="15" text-decoration="underline">U</text>',
		'undo': '<path d="M2 7h5L2 2z"/><path d="M6.447 2.205c-1 .268-1.932.796-2.69 1.553l-.706.707 1.414 1.414.707-.707a3.995 3.995 0 0 1 3.863-1.035 3.995 3.995 0 0 1 2.828 2.828 3.995 3.995 0 0 1-1.035 3.863l-.707.707 1.414 1.414.707-.707a6.003 6.003 0 0 0 1.553-5.795 6.003 6.003 0 0 0-7.348-4.242z"/>',
		'unlink': '<path d="M2 4c-.625 0-1.009.438-1.188.75s-.269.63-.344.969c-.15.677-.219 1.476-.219 2.28s.068 1.605.219 2.282c.075.339.165.625.344.938s.563.78 1.188.78h4v-2H2.469c-.022-.065-.042-.06-.063-.155-.1-.447-.156-1.15-.156-1.844s.057-1.396.156-1.844c.02-.088.042-.092.063-.156H6V4H2zm8 0v2h3.531c.021.064.043.068.063.156.1.448.156 1.149.156 1.844s-.057 1.396-.156 1.844c-.021.095-.041.09-.063.156H10v2h4c.625 0 1.009-.47 1.188-.781s.269-.6.344-.938c.15-.678.219-1.476.219-2.281s-.068-1.604-.219-2.281c-.075-.34-.165-.656-.344-.97S14.625 4 14 4h-4z"/>',
		'youtube': '<path d="M2 2C1 2 0 3 0 4v8c0 1 1 2 2 2h12c1 0 2-1 2-2V4c0-1-1-2-2-2H2zm4 3l6 3-6 3V5z"/>'
	};

	sceditor.icons.monocons = function () {
		var nodes = {};
		var colorPath;

		return {
			create: function (command) {
				if (command in icons) {
					nodes[command] = sceditor.dom.parseHTML(
						'<svg xmlns="http://www.w3.org/2000/svg" ' +
							'viewbox="0 0 16 16" unselectable="on">' +
								icons[command] +
						'</svg>'
					).firstChild;

					if (command === 'color') {
						colorPath = nodes[command].querySelector('.sce-color');
					}
				}

				return nodes[command];
			},
			update: function (isSourceMode, currentNode) {
				if (colorPath) {
					var color = 'inherit';

					if (!isSourceMode && currentNode) {
						color = currentNode.ownerDocument
							.queryCommandValue('forecolor');
					}

					dom.css(colorPath, 'fill', color);
				}
			},
			rtl: function (isRtl) {
				var gripNode = nodes.grip;

				if (gripNode) {
					var transform = isRtl ? 'scaleX(-1)' : '';

					dom.css(gripNode, 'transform', transform);
					dom.css(gripNode, 'msTransform', transform);
					dom.css(gripNode, 'webkitTransform', transform);
				}
			}
		};
	};

	sceditor.icons.monocons.icons = icons;
})(document, sceditor);
