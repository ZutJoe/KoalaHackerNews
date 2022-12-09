let choice = document.getElementById('choice');
let widget = document.querySelector('.widget');
let body = document.getElementById('body');
let content = document.getElementById('content');
let tables = document.getElementsByTagName('table')
let temp = 1;

widget.addEventListener('click', () => {
    if (temp == 1) {
        choice.className = 'dark';
        temp = 0;
        widget.style.border = '2px solid rgb(11, 243, 81)';
        body.style.backgroundColor = 'rgb(7, 7, 29)';
        body.style.color = 'white';
        content.className = 'shadow p-3 mt-1 bg-dark rounded mx-auto'
        for (let i = 0; i < tables.length; i++) {
            tables[i].className = 'table table-dark table-hover text-center align-middle'
        }
    } 
    else {
        choice.className = 'light';
        temp = 1;
        widget.style.border = '2px solid black';
        body.style.backgroundColor = 'white';
        body.style.color = 'black';
        content.className = 'shadow p-3 mt-1 bg-body rounded mx-auto'
        for (let i = 0; i < tables.length; i++) {
            tables[i].className = 'table table-hover text-center align-middle'
        }
    }
})

let search_modal_el = document.getElementById('search_modal')
let search_modal = new bootstrap.Modal(search_modal_el, {
    keyboard: true,
    focus: true,
    backdrop: true
})

function show_modal() {
    search_modal.show()
    let search_input = document.getElementById('fact_search_input')
    search_modal_el.addEventListener('shown.bs.modal', () => {
        search_input.focus()
    })

    search_modal_el.addEventListener('hidden.bs.modal', () => {
        search_input.value = ''
        let search_result = document.getElementById('search_result')
        if (search_result !== null) {
            search_result.remove()
        }
    })
}


function createDivNode () {
    let node = document.createElement('div')
    node.className = 'list-group'
    node.id = 'search_result'
    let modal_body = document.getElementById('modal-body')
    modal_body.appendChild(node)
}

function createANode (aid, content) {
    let node = document.createElement("a")
    node.className = 'list-group-item list-group-item-action'
    node.id = '#' + aid
    node.href = '#' + aid
    let textnode = document.createTextNode(content)
    node.appendChild(textnode)
    search_result.appendChild(node)

    node.addEventListener("click", () => {
        search_modal.hide()
    })
}

let search_input = document.getElementById('fact_search_input')
search_input.addEventListener('input', (e) => {

    if (search_input.value === '') {
        clear()
        return
    }

    clear()
    createDivNode()
    searchAndCreateResultEl(search_input.value)
})

function searchAndCreateResultEl (msg) {
    for (let i = 0; i < data_arr.length; i++) {
        let introduces = data_arr[i].introduces
        for (let j = 0; j < introduces.length; j ++) {
            if (introduces[j].toLowerCase().indexOf(msg) !== -1) {
                createANode(data_arr[i].aid, introduces[j])
            }
        }
    }
}

function clear() {
    let search_result = document.getElementById('search_result')
    if (search_result !== null) {
        search_result.remove()
    }
}
