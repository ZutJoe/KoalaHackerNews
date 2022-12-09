let search_input = document.getElementById('fact_search_input')

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
            
            if (introduces[j].indexOf(msg) !== -1) {
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

