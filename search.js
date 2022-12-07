let arrs = ['a', 'aa', 'bbbb', 'aaaa', 'cccc', 'dddd', 'aavv', '你好', '你']

let search_input = document.getElementById('fact_search_input')

function createDivNode () {
    const node = document.createElement('div')
    node.className = 'list-group'
    node.id = 'search_result'

    let modal_body = document.getElementById('modal-body')
    modal_body.appendChild(node)
}

function createANode (content) {
    const node = document.createElement("a")
    node.className = 'list-group-item list-group-item-action'
    node.href = '#'
    const textnode = document.createTextNode(content)
    node.appendChild(textnode)
    search_result.appendChild(node)
}

search_input.addEventListener('input', (e) => {

    if (search_input.value === '') {
        clear()
        return
    }

    clear()
    createDivNode()
    for (let i = 0; i < arrs.length; i++) {
        if (arrs[i].indexOf(search_input.value) !== -1) {
            createANode(arrs[i])
        }
    }
})

function clear() {
    let search_result = document.getElementById('search_result')
    if (search_result !== null) {
        search_result.remove()
    }
}

