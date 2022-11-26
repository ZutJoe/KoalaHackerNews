// import docsearch from '@docsearch/js';


docsearch({
    container: "#docsearch",
    appId: "WDAJNKS3QQ",
    apiKey: "b09e16fe7d2c25524997c82d657a3ec3",
    indexName: "koala hacker news",
    resultsFooterComponent({ state }) {
        return {
            type: "a",
            ref: undefined,
            constructor: undefined,
            key: undefined,
            props: {
                href: "https://docsearch.algolia.com/apply",
                target: "_blank",
                onClick: (event) => {
                    console.log(event);
                },
                children: `${state.context.nbHits} hits found!`
            },
            __v: null
        };
    },
    transformItems(items) {
        return items.map(item => {
            const liveUrl = 'https://getbootstrap.com/'

            item.url = window.location.origin.startsWith(liveUrl) ?
                // On production, return the result as is
                item.url :
                // On development or Netlify, replace `item.url` with a trailing slash,
                // so that the result link is relative to the server root
                item.url.replace(liveUrl, '/')

            // Prevent jumping to first header
            if (item.anchor === 'content') {
                item.url = item.url.replace(/#content$/, '')
                item.anchor = null
            }

            return item
        })
    },
});

