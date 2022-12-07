let arrs = ['a', 'aa', 'bbbb', 'aaaa', 'cccc', 'dddd', 'aavv', '你好', '你']

let search_input = document.getElementById('fact_search_input')

function createUlNode () {
    const node = document.createElement('ul')
    node.className = 'list-group'
    node.id = 'search_result'

    let modal_body = document.getElementById('modal-body')
    modal_body.appendChild(node)
}

function createLiNode (content) {
    const node = document.createElement("li")
    node.className = 'list-group-item'
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
    createUlNode()
    for (let i = 0; i < arrs.length; i++) {
        if (arrs[i].indexOf(search_input.value) !== -1) {
            createLiNode(arrs[i])
        }
    }
})

function clear() {
    // for (let i = 0; i < search_result.childNodes.length; i++) {
    //     search_result.removeChild(search_result.childNodes[i]);
    // }
    let search_result = document.getElementById('search_result')
    if (search_result !== null) {
        search_result.remove()
    }
}

