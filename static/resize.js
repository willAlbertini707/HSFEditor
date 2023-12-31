// setup ace editor
var editor = ace.edit("editor");
editor.setTheme("ace/theme/vibrant_ink");
editor.session.setMode("ace/mode/python");
editor.session.getValue();

// submit code and file name on button click
document.getElementById('submitCode').onsubmit = function() {
    let fileName = document.getElementById("save_file_name");
    let codeVar = document.getElementById("code");
    fileName.innerText = document.getElementById("input_file_name").value
    codeVar.innerText = JSON.stringify(editor.session.getValue());
};

// listen for file submit
document.getElementById("codeFile").onchange = () => {
    document.getElementById("fileSubmit").removeAttribute("disabled");
}

// same as above but for xml file upload
// listen for file submit
document.getElementById("xmlFile").onchange = () => {
    document.getElementById("xmlFileSubmit").removeAttribute("disabled");
}

// do not allow user to open/test/delete without selecting file
document.getElementById("dirXmlFile").onchange = () => {
    document.getElementById("deleteXml").removeAttribute("disabled");
}


document.getElementById("subsystemFile").onchange = () => {
    document.getElementById("open").removeAttribute("disabled");
    document.getElementById("delete").removeAttribute("disabled");
}

// dynamically resize all the windows
const resizable = function (resizer) {
    const direction = resizer.getAttribute('data-direction') || 'horizontal';
    const prevSibling = resizer.previousElementSibling;
    const nextSibling = resizer.nextElementSibling;


    // The current position of mouse
    let x = 0;
    let y = 0;
    let prevSiblingHeight = 0;
    let prevSiblingWidth = 0;

    // Handle the mousedown event
    // that's triggered when user drags the resizer
    const mouseDownHandler = function (e) {
        // Get the current mouse position
        x = e.clientX;
        y = e.clientY;
        const rect = prevSibling.getBoundingClientRect();
        prevSiblingHeight = rect.height;
        prevSiblingWidth = rect.width;

        // Attach the listeners to `document`
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    };

    const mouseMoveHandler = function (e) {
        // How far the mouse has been moved
        const dx = e.clientX - x;
        const dy = e.clientY - y;

        switch (direction) {
            case 'vertical':
                const h =
                    ((prevSiblingHeight + dy) * 100) /
                    resizer.parentNode.getBoundingClientRect().height;
                prevSibling.style.height = `${h}%`;

                break;
            case 'horizontal':
            default:
                const w =
                    ((prevSiblingWidth + dx) * 100) / resizer.parentNode.getBoundingClientRect().width;
                prevSibling.style.width = `${w}%`;

                break;
        }

        const cursor = direction === 'horizontal' ? 'col-resize' : 'row-resize';
        resizer.style.cursor = cursor;
        document.body.style.cursor = cursor;

        prevSibling.style.userSelect = 'none';
        prevSibling.style.pointerEvents = 'none';

        nextSibling.style.userSelect = 'none';
        nextSibling.style.pointerEvents = 'none';
        editorContainer.height = editorContainer.parentElement.height;
    };

    const mouseUpHandler = function () {
        resizer.style.removeProperty('cursor');
        document.body.style.removeProperty('cursor');

        prevSibling.style.removeProperty('user-select');
        prevSibling.style.removeProperty('pointer-events');

        nextSibling.style.removeProperty('user-select');
        nextSibling.style.removeProperty('pointer-events');

        // Remove the handlers of `mousemove` and `mouseup`
        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
    };

    // Attach the handler
    resizer.addEventListener('mousedown', mouseDownHandler);
};

// Query all resizers
document.querySelectorAll('.resizer').forEach(function (ele) {
    resizable(ele);
});