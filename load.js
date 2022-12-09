let data_arr = []

window.onload = function() {
    fetch('https://raw.githubusercontent.com/ZutJoe/Koala_hacker_news/main/data.json')
        .then(response => response.json())
        .then(data => {
            let data_json = JSON.parse(JSON.stringify(data))
            data_arr = processData(data_json)
            // console.log(data_json.length)
            // console.log(data_json[0].hn_items.introduces[0])
            // console.log(data_arr)
            
        })
        .catch(error => console.log(error));
}


function processData(data) {
    let contents = [];
    for (let i = 0; i < data.length; i++) {
        contents.push({
            aid: data[i].aid,
            introduces: data[i].hn_items.introduces
        });
    }
    return contents;
}
